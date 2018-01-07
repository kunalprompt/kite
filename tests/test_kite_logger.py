import sys
import logging
from unittest import TestCase
from logger.logger import KiteLogger


class TestFileLogger(TestCase):

    def test_file_logging(self):
        log = KiteLogger()

        stream_handler = logging.StreamHandler(sys.stdout)
        log.logger.addHandler(stream_handler)
        try:
            log.logger.debug("DEBUG: Hello World")
            log.logger.info("DEBUG: Hello Sansaar")
            log.logger.error("ERROR: Hello Duniya")
            log.logger.critical("CRITICAL: Hello People")
        except:
            assert False
        finally:
            log.logger.removeHandler(stream_handler)
