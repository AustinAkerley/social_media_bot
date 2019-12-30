import unittest
import social_media_bot

class Test(unittest.TestCase):

    def test_switch_1(self):
        my_bot = social_media_bot.facebook_bot("./facebook_login.txt", 2)
        email, password = my_bot.switch_account();
        self.assertEqual((email, password), ("8172297818","aa212692"))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()