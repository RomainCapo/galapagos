import unittest
import os
import subprocess

class TestCompilerMethods(unittest.TestCase):

    SUCCESS_RET_CODE = 0

    def test_lexer(self):
        BASE_PATH = "inputs"
        test_files = [BASE_PATH + "/" + file for file in os.listdir(BASE_PATH) if file.endswith(".galapagos")]

        return_codes = []
        for file in test_files:
            sp = subprocess.Popen(['python', 'g_compiler.py', "-f", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            streamdata = sp.communicate()[0]
            return_codes.append(sp.returncode)

        expected_status_code = [self.SUCCESS_RET_CODE for i in range(0, len(test_files))]
        self.assertEqual(return_codes, [self.SUCCESS_RET_CODE for i in range(0, len(test_files))])

if __name__ == '__main__':
    unittest.main()
