from selenium import webdrive
from django.utils import unittest


class FunctionalTestCase(unittest.TestCase):
    ROOT_URL = 'http://127.0.0.1:8000'

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.close()