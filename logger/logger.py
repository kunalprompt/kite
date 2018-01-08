import os
import logging
from .log_buffer import KiteErrorsBufferEmailHandler
from logging import NullHandler


class KiteLogger:
    """
    Class to manage logs
    """

    def __init__(self, log_level=logging.DEBUG):
        """
        Registers the logger

        :param log_level: the default log level for the logger
        """
        self.log_level = log_level
        self.logger = logging.getLogger(self.__class__.__name__)

        # adding Null Handler - https://docs.python.org/3/howto/logging.html#library-config
        self.logger.addHandler(NullHandler())

        self.logger.setLevel(self.log_level)
        self.format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    def add_file_handler(self, log_directory='/tmp', log_file='kite-logger.log'):
        """
        :param log_directory: folder location for the file
        :param log_file: file name
        :return: None
        """
        # adding file handler
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        log_location = '{}/{}'.format(log_directory, log_file)
        fh = logging.FileHandler(log_location, mode='a')
        fh.setFormatter(self.format)
        fh.setLevel(self.log_level)
        self.logger.addHandler(fh)

    def add_email_handler(self, **kwargs):
        """
        Additional handler to handle emails
        """
        kebeh = KiteErrorsBufferEmailHandler(capacity=kwargs.get('capacity', 1),
                                             toaddrs=kwargs['email_to'],
                                             subject=kwargs['email_subject'])
        kebeh.setFormatter(self.format)
        kebeh.setLevel(logging.ERROR)
        self.logger.addHandler(kebeh)
