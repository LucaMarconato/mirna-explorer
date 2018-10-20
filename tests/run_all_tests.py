import sys
import unittest


def scan_dir() -> bool:
    is_from_root = 'tests/' in sys.argv[0]
    return './tests/' if is_from_root else '.'


if __name__ == '__main__':
    loader = unittest.TestLoader()
    tests = loader.discover(scan_dir())
    test_runner = unittest.runner.TextTestRunner()
    test_runner.run(tests)
