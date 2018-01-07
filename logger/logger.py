import os
import logging
from .log_buffer import KiteErrorsBufferEmailHandler


class KiteLogger:
    """
    Class to manage logs
    """

    def __init__(self, log_directory='/tmp', log_file='kite-logger.log',
                 log_level=logging.DEBUG):

        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        log_location = '{}/{}'.format(log_directory, log_file)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self.format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # adding file handler
        fh = logging.FileHandler(log_location, mode='a')
        fh.setFormatter(self.format)
        fh.setLevel(log_level)
        self.logger.addHandler(fh)

    def add_handler(self, **kwargs):
        """
        Additional handler to handle emails
        """
        kebeh = KiteErrorsBufferEmailHandler(capacity=2,
                                             toaddrs=kwargs['email_to'],
                                             subject=kwargs['email_subject'])
        kebeh.setFormatter(self.format)
        kebeh.setLevel(logging.ERROR)
        self.logger.addHandler(kebeh)
