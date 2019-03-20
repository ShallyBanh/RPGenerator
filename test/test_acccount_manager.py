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
        self.credentials_real = ("thomas", "password", "thomas.tetz@gmail.com")
        self.credentials_real2 = ("thomas2", "password", "thomas.tetz@gmail.com")
    
    def tearDown(self):
        if os.path.exists("test.db"):
            os.remove("test.db")

    def test_01_username_available(self):
        self.assertEqual(self.account_manager.username_available("user1"), 0)
        self.account_manager.create_account(*self.credentials)
        self.assertEqual(self.account_manager.username_available("user1"), -1)

    def test_02_create_account(self):
        self.assertEqual(self.account_manager.create_account(*self.credentials), 0)
        self.account_manager.create_account(*self.credentials)
        self.assertEqual(self.account_manager.username_available("user1"), -1)

    def test_03_login(self):
        self.assertEqual(self.account_manager.login("user1", "password1"), None)
        self.account_manager.create_account(*self.credentials)
        self.assertNotEqual(self.account_manager.login("user1", "password1"), None)

    def test_04_get_credentials(self):
        self.account_manager.create_account(*self.credentials)
        self.assertEqual(self.account_manager.get_credentials("user1"), ("user1", self.account_manager.generate_hash("password1", "user1"), "email@1"))

    def test_05_set_credentials(self):
        self.account_manager.create_account(*self.credentials)
        self.account_manager.set_credentials(self.credentials_new[0], self.credentials_new[1])
        self.assertEqual(self.account_manager.get_credentials("user1"), ("user1", self.account_manager.generate_hash("password2", "user1"), "email@1"))
    
    # def test_send_recovery(self):
    #     self.assertEqual(self.account_manager.send_recovery("thomas.tetz@gmail.com"), -1)
    #     self.account_manager.create_account(*self.credentials_real)
    #     self.assertEqual(self.account_manager.send_recovery("thomas.tetz@gmail.com"), 0)
    #     self.account_manager.create_account(*self.credentials_real2)
    #     self.assertEqual(self.account_manager.send_recovery("thomas.tetz@gmail.com"), 0)
    
    # def test_recover_account(self):
    #     self.account_manager.create_account(*self.credentials_real)
    #     self.assertEqual(self.account_manager.login("thomas", "password"), 0)
    #     self.assertEqual(self.account_manager.send_recovery("thomas.tetz@gmail.com"), 0)
    #     received_code = input("the received code was: ")
    #     self.assertEqual(self.account_manager.recover_account("thomas", received_code, "newpassword", "typopassword"), -1)
    #     self.assertEqual(self.account_manager.recover_account("thomas", received_code, "newpassword", "newpassword"), 0)
    #     self.assertEqual(self.account_manager.recover_account("thomas", received_code, "code_removed", "code_removed"), -1)
    #     self.assertEqual(self.account_manager.login("thomas", "code_removed"), -1)
    #     self.assertEqual(self.account_manager.login("thomas", "newpassword"), 0)
    #     self.assertEqual(self.account_manager.send_recovery("thomas.tetz@gmail.com"), 0)
    #     received_code1 = input("the first received code was: ")
    #     self.assertEqual(self.account_manager.send_recovery("thomas.tetz@gmail.com"), 0)
    #     received_code2 = input("the second received code was: ")
    #     self.assertEqual(self.account_manager.recover_account("thomas", received_code1, "overwritten_password", "overwritten_password"), -1)
    #     self.assertEqual(self.account_manager.recover_account("thomas", received_code2, "newerpassword", "newerpassword"), 0)
    #     self.assertEqual(self.account_manager.login("thomas", "newerpassword"), 0)

    #     self.account_manager.create_account(*self.credentials_real2)
    #     self.assertEqual(self.account_manager.login("thomas2", "password"), 0)
    #     self.assertEqual(self.account_manager.send_recovery("thomas.tetz@gmail.com"), 0)
    #     received_code1 = input("the received code for thomas was: ")
    #     received_code2 = input("the received code for thomas2 was: ")
    #     self.assertEqual(self.account_manager.recover_account("thomas", received_code2, "newestpassword", "newestpassword"), -1)
    #     self.assertEqual(self.account_manager.recover_account("thomas", received_code1, "newestpassword", "newestpassword"), 0)
    #     self.assertEqual(self.account_manager.recover_account("thomas2", received_code2, "newestpassword2", "newestpassword2"), 0)
    #     self.assertEqual(self.account_manager.login("thomas", "newerpassword"), 0)
    #     self.assertEqual(self.account_manager.login("thomas2", "newerpassword2"), 0)

    # def test_add_asset(self):
        


        
    

if __name__ == "__main__":
    unittest.main()