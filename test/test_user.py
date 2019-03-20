import unittest
import os
import sys
sys.path.append('../')
from Account.User import User

class TestUser(unittest.TestCase):

    def setUp(self):
        self.username = "my_name"
        self.email = "my_email"
        self.assets = {}
        self.password = None
        self.user = User(self.username, self.email, self.assets, self.password)
        self.different_username = "different_username"
        

    def test_01_set_username(self):
        print("======================================================================\ntest_01_set_username (__main__.TestUser)\n----------------------------------------------------------------------")
        self.user.set_username(self.different_username)
        self.assertEqual(self.different_username, self.user._username)

    def test_02_get_username(self):
        print("======================================================================\ntest_01_get_username (__main__.TestUser)\n----------------------------------------------------------------------")
        self.user.set_username(self.different_username)
        self.assertEqual(self.different_username, self.user._username)
    # def test_03_set_password(self):
    # def test_04_get_password(self):
    # def test_05_set_email(self):
    # def test_06_get_email(self):
    # def test_07_add_asset(self):
    # def test_08_update_asset(self):
    # def test_09_delete_asset(self):
    # def test_10_get_asset(self):
    # def test_11_set_assets(self):
    # def test_12_get_assets(self):
    
    #     self.assertEqual(self.account_manager.username_available("user1"), 0)
    #     self.account_manager.create_account(*self.credentials)
    #     self.assertEqual(self.account_manager.username_available("user1"), -1)

    # def test_02_create_account(self):
    #     self.assertEqual(self.account_manager.create_account(*self.credentials), 0)
    #     self.account_manager.create_account(*self.credentials)
    #     self.assertEqual(self.account_manager.username_available("user1"), -1)

    # def test_03_login(self):
    #     self.assertEqual(self.account_manager.login("user1", "password1"), -1)
    #     self.account_manager.create_account(*self.credentials)
    #     self.assertEqual(self.account_manager.login("user1", "password1"), 0)

    # def test_04_get_credentials(self):
    #     self.account_manager.create_account(*self.credentials)
    #     self.assertEqual(self.account_manager.get_credentials("user1"), ("user1", self.account_manager.generate_hash("password1", "user1"), "email@1"))

    # def test_05_set_credentials(self):
    #     self.account_manager.create_account(*self.credentials)
    #     self.account_manager.set_credentials(*self.credentials_new)
    #     self.assertEqual(self.account_manager.get_credentials("user1"), ("user1", self.account_manager.generate_hash("password2", "user1"), "email@2"))
    


        
    

if __name__ == "__main__":
    unittest.main()