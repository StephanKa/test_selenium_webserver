# -*- coding: utf-8 -*-
""" DESCRIPTIONS HERE

"""
##############################################################################
# TODO:
#
# command line call:    python test_selenium_webserver.py <Test_Case_Name>[.<Test_Method>] [<Test_Case_Name>.<Test_Method>]...
# Test_Case_Name:       class name
# Test_method:          optional argument
# Example:              python test_selenium_webserver.py Webserver.test_refresh_news

import time
import unittest
import sys
from selenium import webdriver
from selenium.webdriver.chrome import service
import random

class WebserverTemplate(unittest.TestCase):
    ''' Template class which has all the test inside, all needed browser are derived from this template class '''
    
    @classmethod  
    def setUpClass(self):
        self.address = 'http://127.0.0.1:8081'
        self.webdriver_service = service.Service('operadriver.exe')
        self.webdriver_service.start()
    
    # we skip this because we don't want to start the template class test which doesn't make sense.
    @unittest.skip('Template will not start any test')
    def setUp(self):
        self.browser = None
        if(self.browser == None):
            raise Exception('Please derive class and implement the class!')
        
    def tearDown(self):
        try:
            self.browser.quit()
        except:
            print('!!!browser could not be closed!!!')
        
    def test_refresh_news(self):
        ''' test functionality of start and stop buttons with the comparison of status texts'''
        self.browser.find_element_by_id('refresh-news-button').click()
        temp_before = self.browser.find_element_by_id('newsText').text
        self.assertEqual(temp_before, self.browser.find_element_by_id('newsText').text)
            
    def test_change_live_message(self):
        ''' test for redndered image content'''
        image_before =  self.browser.find_element_by_id('image').get_attribute('src')
        self.browser.find_element_by_id('ImageContent').send_keys('{0:.2f}'.format(random.random()))
        self.browser.find_element_by_id('RenderImage').click()
        time.sleep(0.5)
        image_after =  self.browser.find_element_by_id('image').get_attribute('src')
        self.assertNotEqual(image_after, image_before)
            
    def test_refresh_button_text(self):
        ''' test for checking the text on the refresh news button '''
        self.assertEqual(self.browser.find_element_by_id('refresh-news-button').text, u'Refresh News')
        
    def test_web_title(self):
        ''' test for checking the naming of the web title '''
        self.assertEqual(self.browser.title.lower(), u'News Headlines')

class WebserverChrome(WebserverTemplate):
    
    def setUp(self):
        self.browser = webdriver.Chrome('chromedriver.exe')
        self.browser.get(self.address)
        time.sleep(1)
        
class WebserverFirefox(WebserverTemplate):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(self.address)
        time.sleep(1)
        
class WebserverOpera(WebserverTemplate):
    
    def setUp(self):
        self.browser = webdriver.Remote(self.webdriver_service.service_url, webdriver.DesiredCapabilities.OPERA)
        self.browser.get(self.address)
        time.sleep(1)
        
class WebserverIE(WebserverTemplate):
    
    @classmethod  
    def setUpClass(self):
        self.address = 'http://127.0.0.1:8081'
        self.webdriver_service = service.Service('IEDriverServer.exe')
        self.webdriver_service.start()
    
    def setUp(self):
        self.browser = webdriver.Remote(self.webdriver_service.service_url, webdriver.DesiredCapabilities.INTERNETEXPLORER)
        self.browser.get(self.address)
        time.sleep(1)
        
if sys.version_info < (3, 0):
    # Note:
    # The loader that sorts the test by their order of definition doesn't
    # work on Python 3.
    #
    # TODO: 
    # - test environment for multiple suites
    if __name__ == '__main__':
        suite = unittest.TestSuite()
        if(len(sys.argv)) < 2:
            # removed the exception so it will execute the whole class
            unittest.main(verbosity=2)
        else:
            while(len(sys.argv) > 1):
                tmp_argument = sys.argv.pop(1)
                if(tmp_argument[0:2] == '--'):
                    # add optional parameter here
                    pass
                else:
                    # split the test method from test class
                    test_argument = tmp_argument.split('.')
                    if(len(test_argument) == 2):
                        test_case = test_argument[0]
                        test_method = test_argument[1]
                        suite.addTest((eval(test_case))(test_method))
                    elif(len(test_argument) == 1):
                        test_case = test_argument[0]
                        if(suite!=unittest.TestSuite()):
                            raise Exception('ERROR: Cannot have multiple test suites!')
                        suite = unittest.TestLoader().loadTestsFromTestCase(eval(test_case))
                    else:
                        raise Exception('ERROR: invalid test case specification!')

            runner = unittest.TextTestRunner(descriptions=False, verbosity = 2)
            test_res = runner.run(suite)
            # check for errors or failures and return 0 or 1
            if((test_res.errors != []) or (test_res.failures != [])):
                sys.exit(1)
            else:
                sys.exit(0)
