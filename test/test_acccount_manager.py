import unittest
import os
import sys
from shutil import copyfile, rmtree
import base64
sys.path.append('../')
from account.account_manager import AccountManager

class TestAccountManager(unittest.TestCase):

    def setUp(self):
        self.account_manager = AccountManager(database_file="test.db")
        self.credentials = ("user1", "password1", "email@1")
        self.credentials_same_username = ("user1", "password2", "email@2")
        self.credentials_new = ("user1", "password2", "email@2")
        self.credentials_real = ("thomas", "password", "thomas.tetz@gmail.com")
        self.credentials_real2 = ("thomas2", "password", "thomas.tetz@gmail.com")
        self.asset_circle = "circle_0900x0900.jpg"
        self.asset_sudoku = "Sudoku-900x900.jpg"
        if not os.path.exists("testtmp"):
            os.mkdir("testtmp")

    def tearDown(self):
        if os.path.exists("test.db"):
            os.remove("test.db")
        if os.path.exists("testtmp"):
            rmtree("testtmp")

    def test_01_username_available(self):
        print("======================================================================\ntest_01_username_available (__main__.AccountManager)\n----------------------------------------------------------------------")
        self.assertEqual(self.account_manager.username_available("user1"), 0)
        self.account_manager.create_account(*self.credentials)
        self.assertEqual(self.account_manager.username_available("user1"), -1)

    def test_02_create_account(self):
        print("======================================================================\ntest_02_create_account (__main__.AccountManager)\n----------------------------------------------------------------------")        
        self.assertEqual(self.account_manager.create_account(*self.credentials), 0)
        self.account_manager.create_account(*self.credentials)
        self.assertEqual(self.account_manager.username_available("user1"), -1)

    def test_03_login(self):
        print("======================================================================\ntest_03_login (__main__.AccountManager)\n----------------------------------------------------------------------")        
        self.assertEqual(self.account_manager.login("user1", "password1"), None)
        self.account_manager.create_account(*self.credentials)
        self.assertNotEqual(self.account_manager.login("user1", "password1"), None)

    def test_04_get_credentials(self):
        print("======================================================================\ntest_04_get_credentials (__main__.AccountManager)\n----------------------------------------------------------------------")        
        self.account_manager.create_account(*self.credentials)
        self.assertEqual(self.account_manager.get_credentials("user1"), ("user1", self.account_manager.generate_hash("password1", "user1"), "email@1"))

    def test_05_set_credentials(self):
        print("======================================================================\ntest_05_set_credentials (__main__.AccountManager)\n----------------------------------------------------------------------")        
        self.account_manager.create_account(*self.credentials)
        self.account_manager.set_credentials(self.credentials_new[0], self.credentials_new[1])
        self.assertEqual(self.account_manager.get_credentials("user1"), ("user1", self.account_manager.generate_hash("password2", "user1"), "email@1"))
    
    # def test_send_recovery(self):
        # print("======================================================================\ntest_06_send_recovery (__main__.AccountManager)\n----------------------------------------------------------------------")    
    #     self.assertEqual(self.account_manager.send_recovery("thomas.tetz@gmail.com"), -1)
    #     self.account_manager.create_account(*self.credentials_real)
    #     self.assertEqual(self.account_manager.send_recovery("thomas.tetz@gmail.com"), 0)
    #     self.account_manager.create_account(*self.credentials_real2)
    #     self.assertEqual(self.account_manager.send_recovery("thomas.tetz@gmail.com"), 0)
    
    # def test_recover_account(self):
        # print("======================================================================\ntest_07_recover_account (__main__.AccountManager)\n----------------------------------------------------------------------")    
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
    def test_08_assets(self):
        print("======================================================================\ntest_08_assets (__main__.AccountManager)\n----------------------------------------------------------------------")
        self.account_manager.create_account(*self.credentials)
        self.assertNotEqual(self.account_manager.login("user1", "password1"), None)
        # add asset
        # insert into database

        with open(self.asset_circle, 'rb') as f:
            photo = f.read()
        encoded_image = base64.b64encode(photo)
        self.assertEqual(self.account_manager.add_asset(self.credentials[0], self.asset_circle, encoded_image), 0)
        # get and put in tmptest
        asset = self.account_manager.get_asset(self.credentials[0], self.asset_circle)[0]
        print("got the asset: {}".format(asset))
        self.assertNotEqual(asset, None)
        decoded_image = base64.b64decode(asset)        
        with open('testtmp/{}'.format(self.asset_circle), 'wb') as recreated:
            recreated.write(bytearray(decoded_image))

        self.assertEqual(os.path.exists('testtmp/{}'.format(self.asset_circle)), 1)
        # update asset
        # get asset
        # get assets
        p = input("wait to check file")
        # self.assertEqual(self.account_manager.create_account(*self.credentials), 0)
        # self.account_manager.create_account(*self.credentials)
        # self.assertEqual(self.account_manager.username_available("user1"), -1)



        
    

if __name__ == "__main__":
    unittest.main()