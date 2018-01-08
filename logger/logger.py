import os
import logging
from .log_buffer import KiteErrorsBufferEmailHandler


class KiteLogger:
    """
    Class to manage logs
    """

    def __init__(self, **kwargs):
        """
        Registers the logger

        Options:
            default_log_level - indicates the default level for logging
            logger_name - customize the name of your logger
            msg_format_string - set the customized format for log messages
        """
        self.log_level = kwargs.get('default_log_level', logging.DEBUG)
        self.logger = logging.getLogger(kwargs.get('logger_name', self.__class__.__name__))

        # adding Null Handler - https://docs.python.org/3/howto/logging.html#library-config
        self.logger.addHandler(logging.NullHandler())

        self.logger.setLevel(self.log_level)

        msg_format_string = '%(asctime)s - %(levelname)s - %(message)s'
        self.format = logging.Formatter(kwargs.get('msg_format_string', msg_format_string))

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

        Options: (* means compulsory)
            *capacity - the capacity of messages buffer
            *email_to - message receivers {can be "a,b,c" or ("a", "b", "c") or ["a", "b", "c"]}
            *email_subject - the subject of email
             log_level - the level for which logging is required
        """
        kebeh = KiteErrorsBufferEmailHandler(capacity=kwargs['capacity'],
                                             toaddrs=kwargs['email_to'],
                                             subject=kwargs['email_subject'])
        kebeh.setFormatter(self.format)
        kebeh.setLevel(kwargs.get('log_level', logging.ERROR))
        self.logger.addHandler(kebeh)
