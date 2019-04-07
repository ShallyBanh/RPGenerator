import unittest
import os
import sys
sys.path.append('../')
from account.account_manager import AccountManager
from client import Client

client = Client()

class TestClient(unittest.TestCase):

    def setUp(self):
        # self.server = Server()
        # client = Client()
        
        self.credentials = ("user1", "password1", "email@1")
        self.credentials_same_username = ("user1", "password2", "email@2")
        self.credentials_change_wrong = ("user1", "password_wrong", "password2")
        self.credentials_change = ("user1", "password1", "password2")
        self.credentials_new = ("user1", "password2", "email@2")
        self.credentials_real = ("thomas", "password", "thomas.tetz@gmail.com")
        self.credentials_real2 = ("thomas2", "password", "thomas.tetz@gmail.com")
        print("\n\n")
    
    # def tearDown(self):
    #     client.reset_database()
    #     print("\n\n")

    def test_01_create_account(self):
        print("======================================================================\ntest_01_create_account (__main__.TestClient)\n----------------------------------------------------------------------")
        self.assertEqual(client.create_account(*self.credentials), 0)

    def test_02_login(self):
        print("======================================================================\ntest_02_login (__main__.TestClient)\n----------------------------------------------------------------------")        
        # self.assertEqual(client.login("user1", "password1"), -1)
        # client.create_account(*self.credentials)
        self.assertEqual(client.login("user1", "password1"), 0)

    def test_03_change_credentials(self):
        print("======================================================================\ntest_03_change_credentials (__main__.TestClient)\n----------------------------------------------------------------------")
        self.assertEqual(client.change_credentials(*self.credentials_change_wrong), -1)
        self.assertEqual(client.login(*self.credentials_change_wrong[:2]), -1)
        self.assertEqual(client.change_credentials(*self.credentials_change), 0)
        self.assertEqual(client.login(self.credentials_change[0], self.credentials_change[2]), 0)
    
    def test_04_send_recovery(self):
        print("======================================================================\ntest_04_send_recovery (__main__.TestClient)\n----------------------------------------------------------------------")
        self.assertEqual(client.send_recovery("thomas.tetz@gmail.com"), -1)
        client.create_account(*self.credentials_real)
        self.assertEqual(client.send_recovery("thomas.tetz@gmail.com"), 0)
    
    # def test_recover_account(self):
    #     client.create_account(*self.credentials_real)
    #     self.assertEqual(client.login("thomas", "password"), 0)
    #     self.assertEqual(client.send_recovery("thomas.tetz@gmail.com"), 0)
    #     received_code = input("the received code was: ")
    #     self.assertEqual(client.recover_account("thomas", received_code, "newpassword", "typopassword"), -1)
    #     self.assertEqual(client.recover_account("thomas", received_code, "newpassword", "newpassword"), 0)
    #     self.assertEqual(client.recover_account("thomas", received_code, "code_removed", "code_removed"), -1)
    #     self.assertEqual(client.login("thomas", "code_removed"), -1)
    #     self.assertEqual(client.login("thomas", "newpassword"), 0)
    #     self.assertEqual(client.send_recovery("thomas.tetz@gmail.com"), 0)
    #     received_code1 = input("the first received code was: ")
    #     self.assertEqual(client.send_recovery("thomas.tetz@gmail.com"), 0)
    #     received_code2 = input("the second received code was: ")
    #     self.assertEqual(client.recover_account("thomas", received_code1, "overwritten_password", "overwritten_password"), -1)
    #     self.assertEqual(client.recover_account("thomas", received_code2, "newerpassword", "newerpassword"), 0)
    #     self.assertEqual(client.login("thomas", "newerpassword"), 0)

    #     client.create_account(*self.credentials_real2)
    #     self.assertEqual(client.login("thomas2", "password"), 0)
    #     self.assertEqual(client.send_recovery("thomas.tetz@gmail.com"), 0)
    #     received_code1 = input("the received code for thomas was: ")
    #     received_code2 = input("the received code for thomas2 was: ")
    #     self.assertEqual(client.recover_account("thomas", received_code2, "newestpassword", "newestpassword"), -1)
    #     self.assertEqual(client.recover_account("thomas", received_code1, "newestpassword", "newestpassword"), 0)
    #     self.assertEqual(client.recover_account("thomas2", received_code2, "newestpassword2", "newestpassword2"), 0)
    #     self.assertEqual(client.login("thomas", "newerpassword"), 0)
    #     self.assertEqual(client.login("thomas2", "newerpassword2"), 0)

if __name__ == "__main__":
    unittest.main()