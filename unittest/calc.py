import requests


# simple function to unit test
def add(a, b):
    return a + b


# function to unit test that can raise an exception
def divide(a, b):
    if b == 0:
        raise ValueError('Cannot divide by zero.')
    return a / b


# class to unit test that calls an HTTP endpoint
class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b

    def process(self):
        # HTTP call that we will want to mock in the tests
        response = requests.get(f'http://calculator.com/process?a={self.a}&b={self.b}')
        if response.ok:
            return response.text
        else:
            return None
