import unittest
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_DIR = "/mnt/c/Workspaces/EOS/contracts/hello"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)


    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Build and deploy a contract in the given folder
        {}.
        '''.format(CONTRACT_DIR))
        reset()
        create_master_account("master")

        COMMENT('''
        Create test accounts:
        ''')
        create_account("alice", master)
        create_account("carol", master)
        create_account("bob", master)


    def setUp(self):
        pass


    def test_01(self):
        COMMENT('''
        Create, build and deploy the contract:
        ''')
        create_account("host", master)
        contract = Contract(host, CONTRACT_DIR)
        contract.build()
        contract.deploy()

        COMMENT('''
        Test an action for Alice, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":alice}, permission=(alice, Permission.ACTIVE))
        self.assertTrue("alice" in DEBUG())

        COMMENT('''
        Test an action for Carol, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":carol}, permission=(carol, Permission.ACTIVE))
        self.assertTrue("carol" in DEBUG())

        COMMENT('''
        WARNING: This action should fail due to authority mismatch!
        ''')
        with self.assertRaises(MissingRequiredAuthorityError):
            host.push_action(
                "hi", {"user":carol}, permission=(bob, Permission.ACTIVE))
 

    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
