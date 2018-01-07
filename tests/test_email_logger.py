from unittest import TestCase
from logger.logger import KiteLogger


class TestEmailLogger(TestCase):
    """
    This is unit testing and required to be checked manually as this test is going to send email.
    """

    def test_email_logging(self):
        log = KiteLogger()
        log.add_handler(email_to='kunalprompt@gmail.com',
                        email_subject='Hello')
        try:
            log.logger.debug("DEBUG: Hello World")
            log.logger.info("DEBUG: Hello Sansaar")
            log.logger.error("ERROR: Hello Duniya")
            log.logger.critical("CRITICAL: Hello People")
        except:
            assert False