import unittest
import g_compiler
import os
import subprocess

class TestCompilerMethods(unittest.TestCase):

    SUCCESS_RET_CODE = 0

    def test_lexer(self):
        BASE_PATH = "inputs"
        test_files = [os.path.join(BASE_PATH, file) for file in os.listdir() if file.endswith(".txt")]

        return_codes = []
        for file in test_files:
            sp = subprocess.Popen(['python', 'g_compiler.py', file], stdout=subprocess.PIPE)
            streamdata = sp.communicate()[0]
            return_codes.append(sp.returncode)

        expected_status_code = [self.SUCCESS_RET_CODE for i in range(0, len(test_files))]
        self.assertEqual(return_codes, [self.SUCCESS_RET_CODE for i in range(0, len(test_files))])

if __name__ == '__main__':
    unittest.main()
