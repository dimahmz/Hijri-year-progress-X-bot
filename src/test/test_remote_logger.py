import unittest
from db.remote_tweets_db import TweetsDB
from db.models.log import Log
import sys
from dotenv import load_dotenv
import os
from logger import *
from remote_logger import RemoteLogger
from datetime import datetime
from datetime import datetime, timezone

sys.path.insert(0, '..')


load_dotenv(".env.test")
# db credentials for testing env
url = os.getenv("TEST_SUPABASE_URL")
key = os.getenv("TEST_SUPABASE_KEY")
tweetsDB = TweetsDB(url, key)


class TestRemoteLogger(unittest.TestCase):

    def test_remote_loggers(self):
        # instanciate a db client with the remote database
        tweetsDB = TweetsDB(url=url, key=key)
        # posting 
        logged_at = datetime.now(timezone.utc).isoformat()
        # create logs object
        info_log = Log(message="info message", pathname="/", lineno=1, logged_at=logged_at)
        error_log = Log(message="error message", pathname="/", lineno=1, logged_at=logged_at)
        warning_log = Log(message="warning message", pathname="/", lineno=1, logged_at=logged_at)
        debug_log = Log(message="bug message", pathname="/", lineno=1, logged_at=logged_at)
        # store the logs in the database
        stored_info_log = tweetsDB.log_to_remote_db(type="info", log=info_log)
        stored_error_log = tweetsDB.log_to_remote_db(type="error", log=error_log)
        stored_warning_log = tweetsDB.log_to_remote_db(type="warning", log=warning_log)
        stored_debug_log = tweetsDB.log_to_remote_db(type="debug", log=debug_log)
        
        # format the stored logs to test them
        format_stored_info_log = Log.format_str_to_test(stored_info_log)
        format_stored_error_log = Log.format_str_to_test(stored_error_log)
        format_stored_warning_log = Log.format_str_to_test(stored_warning_log)
        format_stored_debug_log = Log.format_str_to_test(stored_debug_log)

        # format the creted logs to test it 
        format_created_info_log = info_log.format_to_test()
        format_created_error_log = error_log.format_to_test()
        format_created_warning_log = warning_log.format_to_test()
        format_created_debug_log = debug_log.format_to_test()

        # test equality
        self.assertEqual(format_stored_info_log, format_created_info_log)
        self.assertEqual(format_created_error_log, format_stored_error_log)
        self.assertEqual(format_stored_warning_log, format_created_warning_log)
        self.assertEqual(format_stored_debug_log, format_created_debug_log)
        
        # close connection
        tweetsDB.close_db_connection()

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestRemoteLogger('test_remote_loggers'))
    # Run only the selected tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
