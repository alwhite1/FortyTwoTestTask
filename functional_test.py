from selenium import webdriver
import unittest

def check_contact(element):
    if element[1]:
        return True
    return False

def check_person_info(element):
    if element:
        return True
    return False

class MainPageTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(6)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_browser_and_see_content(self):

        self.browser.get('http://localhost:8000')
        self.assertIn(self.browser.find_element_by_id('title').text, '42 Coffee Cups Test Assignment')

        element = self.browser.find_element_by_id("name").text
        self.assertEqual(check_person_info(element), True)

        element = self.browser.find_element_by_id("last_name").text
        self.assertEqual(check_person_info(element), True)

        element = self.browser.find_element_by_id("date_of_birth").text
        self.assertEqual(check_person_info(element), True)

        element = self.browser.find_element_by_id("bio").text
        self.assertEqual(check_person_info(element), True)

        element = self.browser.find_element_by_id("email").text.split(':')
        self.assertEqual(check_contact(element), True)

        element = self.browser.find_element_by_id("jabber").text.split(':')
        self.assertEqual(check_contact(element), True)

        element = self.browser.find_element_by_id("skype").text.split(':')
        self.assertEqual(check_contact(element), True)

        element = self.browser.find_element_by_id("other_contacts").text.split(':')
        self.assertEqual(check_contact(element), True)

class RequestsPageTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(6)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_browser_and_see_link_to_request(self):
        self.browser.get('http://localhost:8000')
        element = self.browser.find_element_by_tag_name("a").text
        self.assertEqual(element, 'requests')
        element = self.browser.find_element_by_tag_name("a").get_attribute('href')
        self.assertEqual(element, 'http://localhost:8000/requests')

if __name__ == '__main__':
    unittest.main()