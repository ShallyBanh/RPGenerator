import unittest
import os
import sys
sys.path.append('../')
from Account.AccountManager import AccountManager

class TestAccountManager(unittest.TestCase):

    def setUp(self):
        self.account_manager = AccountManager("test.db")
        self.credentials = ("user1", "password1", "email@1")
        self.credentials_same_username = ("user1", "password2", "email@2")
        self.credentials_new = ("user1", "password2", "email@2")
    
    def tearDown(self):
        if os.path.exists("test.db"):
            os.remove("test.db")

    def test_username_available(self):
        self.assertEqual(self.account_manager.username_available("user1"), 0)
        self.account_manager.create_account(*self.credentials)
        self.assertEqual(self.account_manager.username_available("user1"), -1)

    def test_create_account(self):
        self.assertEqual(self.account_manager.create_account(*self.credentials), 0)
        self.account_manager.create_account(*self.credentials)
        self.assertEqual(self.account_manager.username_available("user1"), -1)

    def test_login(self):
        self.assertEqual(self.account_manager.login("user1", "password1"), -1)
        self.account_manager.create_account(*self.credentials)
        self.assertEqual(self.account_manager.login("user1", "password1"), 0)

    def test_get_credentials(self):
        self.account_manager.create_account(*self.credentials)
        self.assertEqual(self.account_manager.get_credentials("user1"), self.credentials)

    def test_set_credentials(self):
        self.account_manager.create_account(*self.credentials)
        self.account_manager.set_credentials(*self.credentials_new)
        self.assertEqual(self.account_manager.get_credentials("user1"), self.credentials_new)
    
    def test_send_recovery(self):
        self.assertEqual(self.account_manager.send_recovery("email@1"), -1)
        self.account_manager.create_account(*self.credentials)
        self.assertEqual(self.account_manager.send_recovery("email@1"), 0)
    
    def test_recover_user(self):
        return
    

if __name__ == "__main__":
    unittest.main()