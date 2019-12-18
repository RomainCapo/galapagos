import unittest
import g_compiler
import os
import subprocess

class TestCompilerMethods(unittest.TestCase):

    SUCCESS_RET_CODE = 0

    def test_lexer(self):
        sp = subprocess.Popen(['python', 'g_compiler.py', 'inputs/input.galapagos'], stdout=subprocess.PIPE)
        streamdata = sp.communicate()[0]
        rc = sp.returncode
        print("Return code : ", rc)
        self.assertEqual(rc, self.SUCCESS_RET_CODE)

if __name__ == '__main__':
    unittest.main()
