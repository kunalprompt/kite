from unittest import TestCase
from logger.logger import KiteLogger


class TestEmailLogger(TestCase):
    """
    This is unit testing and required to be checked manually as this test is going to send email.
    """

    def test_email_logging(self):
        log = KiteLogger()
        log.add_email_handler(capacity=3,
                              email_to='kunalprompt@gmail.com',
                              email_subject='Buffer Capacity 3 | But errors recorded are only 2')
        try:
            log.logger.debug("Hello World")
            log.logger.info("Hello Sansaar")
            log.logger.error("Hello Duniya")
            log.logger.critical("Hello People")
        except:
            assert False
