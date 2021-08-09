import unittest
from unittest.mock import patch

from calc import add, divide, Calculator


class TestCalc(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Called once before starting to run the tests')

    @classmethod
    def tearDownClass(cls):
        print('Called once after finishing to run the tests')

    def setUp(self):
        print('Called before every single test')
        self.calculator = Calculator(0, 0)

    def tearDown(self):
        print('Called after every single test')

    def test_add(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(1, -2), -1)

    def test_divide(self):
        self.assertEqual(divide(1, 2), 0.5)
        self.assertEqual(divide(1, -1), -1)

        # Check that an exception is thrown
        self.assertRaises(ValueError, divide, 10, 0)

        # Alternative way to test thrown exceptions with a context manager
        with self.assertRaises(ValueError):
            divide(10, 0)

    def test_process(self):
        # Mock the call to requests.get() in the calculator class to simulate a success
        with patch('calc.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = '1234'

            self.calculator.a = 1
            self.calculator.b = 2
            self.assertEqual(self.calculator.process(), '1234')
            mocked_get.assert_called_with('http://calculator.com/process?a=1&b=2')

        # Mock the call to requests.get() in the calculator class to simulate a failure
        with patch('calc.requests.get') as mocked_get:
            mocked_get.return_value.ok = False

            self.calculator.a = 1
            self.calculator.b = 2
            self.assertEqual(self.calculator.process(), None)
            mocked_get.assert_called_with('http://calculator.com/process?a=1&b=2')


if __name__ == '__main__':
    unittest.main()
