"""
Example BASH kernel built on top of Callysto, emulating a BASH
terminal; users can also connect to a remote server through SSH
"""

__all__ = (
    "BashKernel",)

import getpass
import logging
import os
import re
import signal

import paramiko
import pexpect.replwrap
from pexpect import EOF

import callysto

_logger = logging.getLogger(__name__)

class BashKernel (callysto.BaseKernel):
    implementation_name = "Bash Kernel"
    implementation_version = "0.1"

    language_name = "bash"
    language_mimetype = "text/x-sh"
    language_file_extension = ".sh"

    def do_startup_ (self, **kwargs):
        # we set the signal handler for SIGNIT to SIG_DFL (default function)
        # for the underlying BASH child process to be interruptible; we need
        # to do it now since we won't be able to do it from the child process
        previous_handler = signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            self._bash_repl = pexpect.replwrap.bash()
        finally:
            # then we set it back to its original value
            signal.signal(signal.SIGINT, previous_handler)

        # we declare a couple of magic commands to
        # log in and out of a remote server with SSH
        self.declare_pre_flight_command(
            "ssh-login", self.ssh_connect)

        self.declare_pre_flight_command(
            "ssh-logout", self.ssh_disconnect)

        self._ssh_repl = None

    def do_execute_ (self, code):
        code = code.strip()

        if (self._ssh_repl is None):
            frames = self.bash_execute(code)
        else:
            frames = self.ssh_execute(code)

        for frame in frames:
            yield frame

    def bash_execute (self, code):
        try:
            # send any command to the underlying BASH process,
            # then send the output strings to the Jupyter notebook
            yield self._bash_repl.run_command(code.strip(), timeout = None)

            # retrieve the exit code of the last executed command
            try:
                exit_code = int(self._bash_repl.run_command("echo $?").strip())
            except:
                exit_code = 1

            # if different from zero,
            if (exit_code != 0):
                # send whatever text the process sent
                # so far to the Jupyter notebook
                content = self._bash_repl.child.before
                if (content.strip() != str(exit_code)):
                    yield content

                # then raise an exception
                raise Exception(
                    "Process returned a non-zero exit code: %d" % exit_code)

        except KeyboardInterrupt as exception:
            # if the user used a keyboard interrupt, we
            # propagate it to the underlying BASH process
            self._bash_repl.child.sendintr()
            self._bash_repl._expect_prompt()

            yield self._bash_repl.child.before
            raise exception

        except EOF:
            yield self._bash_repl.child.before
            self.do_startup_()

    def ssh_connect (self, code, **kwargs):
        """ usage: ssh-login <hostname> [options]

                <hostname>          hostname
                --user STRING       username
                --password STRING   password
                --port NUMBER       port
        """
        if (self._ssh_repl is not None):
            raise Exception("A SSH connection is already up")

        hostname = kwargs["<hostname>"]
        username = kwargs.get("--user", getpass.getuser())
        password = kwargs.get("--password", '')

        try:
            port = int(kwargs.get("--port", 22))
        except:
            raise Exception("Invalid value for port")

        _logger.debug("SSH logging to %s@%s:%d" % (username, hostname, port))

        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())

        # load ~/.ssh/config, if available
        ssh_config_fn = os.path.join(
            os.path.expanduser("~"), ".ssh", "config")

        if (os.path.isfile(ssh_config_fn)):
            try:
                ssh_config = paramiko.SSHConfig()
                ssh_config.parse(open(ssh_config_fn, "rU"))

            except Exception as exception:
                _logger.error(
                    "Unable to parse %s: %s" % (ssh_config_fn, exception))
            else:
                host = ssh_config.lookup(hostname)
                _logger.debug("ssh-config entry for %s: %s" % (hostname, host))
                hostname = host["hostname"]
        else:
            host = {}

        try:
            ssh_client.connect(hostname,
                port = host.get("port", port),
                username = host.get("user", username),
                password = password,
                key_filename = host.get("identityfile"))

        except Exception as exception:
            raise Exception("Unable to log to %s: %s" % (hostname, exception))

        _logger.debug("SSH logging: done")
        self._ssh_repl = ssh_client

    def ssh_disconnect (self, code, **kwargs):
        """ usage: ssh-logout
        """
        if (self._ssh_repl is not None):
            _logger.debug("SSH logging out")
            self._ssh_repl.close()
            _logger.debug("SSH logging out: done")
            self._ssh_repl = None

    def ssh_execute (self, code):
        try:
            stdin, stdout, stderr = self._ssh_repl.exec_command(code)
            exit_code = stdout.channel.recv_exit_status()

            stdout = stdout.read()
            stderr = stderr.read()

        except Exception as exception:
            raise Exception("Error while executing the command: %s" % exception)

        if (len(stdout.strip()) > 0):
            yield stdout
        if (len(stderr.strip()) > 0):
            yield stderr

        if (exit_code != 0):
            raise Exception(
                "Process returned a non-zero exit code: %d" % exit_code)

if (__name__ == "__main__"):
    BashKernel.launch(debug = True)
