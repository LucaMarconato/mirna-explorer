import sys
import unittest

TEST_DIR = 'tests/'


def scan_dir() -> bool:
    is_from_root = TEST_DIR in sys.argv[0]
    return f'./{TEST_DIR}' if is_from_root else '.'


if __name__ == '__main__':
    loader = unittest.TestLoader()
    tests = loader.discover(scan_dir())
    test_runner = unittest.runner.TextTestRunner()
    test_runner.run(tests)
