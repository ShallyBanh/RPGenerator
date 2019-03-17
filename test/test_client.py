import unittest
import os
import sys
sys.path.append('../')
from Account.AccountManager import AccountManager
# from server import Server
from client import Client


class TestClient(unittest.TestCase):

    def setUp(self):
        # self.server = Server()
        self.client = Client()
        
        self.credentials = ("user1", "password1", "email@1")
        self.credentials_same_username = ("user1", "password2", "email@2")
        self.credentials_new = ("user1", "password2", "email@2")
        self.credentials_real = ("thomas", "password", "thomas.tetz@gmail.com")
        self.credentials_real2 = ("thomas2", "password", "thomas.tetz@gmail.com")
        print("\n\n")
    
    # def tearDown(self):
    #     self.client.reset_database()
    #     print("\n\n")

    def test_create_account(self):
        print("======================================================================\ntest_create_account (__main__.TestClient)\n----------------------------------------------------------------------")
        self.assertEqual(self.client.create_account(*self.credentials), 0)

    def test_login(self):
        print("======================================================================\ntest_login (__main__.TestClient)\n----------------------------------------------------------------------")        
        # self.assertEqual(self.client.login("user1", "password1"), -1)
        # self.client.create_account(*self.credentials)
        self.assertEqual(self.client.login("user1", "password1"), 0)
    
    def test_send_recovery(self):
        print("======================================================================\ntest_send_recovery (__main__.TestClient)\n----------------------------------------------------------------------")
        self.assertEqual(self.client.send_recovery("thomas.tetz@gmail.com"), -1)
        self.client.create_account(*self.credentials_real)
        self.assertEqual(self.client.send_recovery("thomas.tetz@gmail.com"), 0)
        # self.client.create_account(*self.credentials_real2)
        # self.assertEqual(self.client.send_recovery("thomas.tetz@gmail.com"), 0)
    
    # def test_recover_account(self):
    #     self.client.create_account(*self.credentials_real)
    #     self.assertEqual(self.client.login("thomas", "password"), 0)
    #     self.assertEqual(self.client.send_recovery("thomas.tetz@gmail.com"), 0)
    #     received_code = input("the received code was: ")
    #     self.assertEqual(self.client.recover_account("thomas", received_code, "newpassword", "typopassword"), -1)
    #     self.assertEqual(self.client.recover_account("thomas", received_code, "newpassword", "newpassword"), 0)
    #     self.assertEqual(self.client.recover_account("thomas", received_code, "code_removed", "code_removed"), -1)
    #     self.assertEqual(self.client.login("thomas", "code_removed"), -1)
    #     self.assertEqual(self.client.login("thomas", "newpassword"), 0)
    #     self.assertEqual(self.client.send_recovery("thomas.tetz@gmail.com"), 0)
    #     received_code1 = input("the first received code was: ")
    #     self.assertEqual(self.client.send_recovery("thomas.tetz@gmail.com"), 0)
    #     received_code2 = input("the second received code was: ")
    #     self.assertEqual(self.client.recover_account("thomas", received_code1, "overwritten_password", "overwritten_password"), -1)
    #     self.assertEqual(self.client.recover_account("thomas", received_code2, "newerpassword", "newerpassword"), 0)
    #     self.assertEqual(self.client.login("thomas", "newerpassword"), 0)

    #     self.client.create_account(*self.credentials_real2)
    #     self.assertEqual(self.client.login("thomas2", "password"), 0)
    #     self.assertEqual(self.client.send_recovery("thomas.tetz@gmail.com"), 0)
    #     received_code1 = input("the received code for thomas was: ")
    #     received_code2 = input("the received code for thomas2 was: ")
    #     self.assertEqual(self.client.recover_account("thomas", received_code2, "newestpassword", "newestpassword"), -1)
    #     self.assertEqual(self.client.recover_account("thomas", received_code1, "newestpassword", "newestpassword"), 0)
    #     self.assertEqual(self.client.recover_account("thomas2", received_code2, "newestpassword2", "newestpassword2"), 0)
    #     self.assertEqual(self.client.login("thomas", "newerpassword"), 0)
    #     self.assertEqual(self.client.login("thomas2", "newerpassword2"), 0)

if __name__ == "__main__":
    unittest.main()