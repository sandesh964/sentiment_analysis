"""
Wrapper class to manage pubsub emulator
"""

import os
import signal
import subprocess


class PubSubRunner(object):
    """
    Wrapper class to manage pubsub emulator
    """
    def __init__(self):
        self.process = None

    def start(self, port='8538'):
        """
        Start Pubsub Emulator on the specified port
        :param port: pubsub port
        :return: None
        """
        port_args = '--host-port=127.0.0.1:{0}'.format(port)
        self.process = subprocess.Popen(
            " ".join(['gcloud', 'beta', 'emulators', 'pubsub', 'start', port_args]),
            shell=True,
            preexec_fn=os.setsid,
        )
        os.environ['PUBSUB_EMULATOR_HOST'] = 'localhost:{0}'.format(port)
        print self.process

    def kill(self):
        """
        Terminate Pubsub emulator after finishing the test
        :return: None
        """
        del os.environ['PUBSUB_EMULATOR_HOST']
        print 'Inside Kill', self.process
        os.killpg(self.process.pid, signal.SIGTERM)
