#!/usr/bin/env python2

import os
import itertools
from time import sleep
from Queue import Queue
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CONST_PASS = "P@55word!"

class Unmask_Meta(object):

    def __init__(self, known_list, wordlist, maxsize=12):
        self.known_list = known_list
        self.wordlist = wordlist
        self.maxsize = maxsize
        self.chrome_driver = None
        self.chrome_options = None
        self.chrome_execpath = None
        self.guesses = Queue(maxsize=0)

        self._load_chrome_data()
        self._generate_custom_list(self.wordlist)

    def _string_to_list(self, string):
        stub_list = string.split(",")
        return [x.strip(' ') for x in stub_list]


    def _get_needed_number(self, known_list):
        return (self.maxsize - len(self._string_to_list(known_list)))


    def _load_chrome_data(self):
        self.chrome_execpath = "/usr/bin/chromedriver"
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_extension("nkbihfbeogaeaoehlefnkodbefgpgknn.crx")
        self.chrome_driver = webdriver.Chrome(
            executable_path=self.chrome_execpath,
            chrome_options=self.chrome_options,
        )


    def _generate_custom_list(self, wordlist):
        stub_list = None

        if os.path.isfile(wordlist):
            with open(filename) as f:
                stub_list = f.read().splitlines()

            #Generate
            for x in list(itertools.combinations(stub_list, self._get_needed_number(self.known_list))):
                master = list(x) + self._string_to_list(self.known_list)
                self.guesses.put(master)


    def _clear_field(self, element):
        length = len(element.get_attribute('value'))
        if length != 0:
            element.send_keys(length * Keys.BACKSPACE)
            return

    def start_process(self):
        while True:
            self.chrome_driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/popup.html")

            sleep(0.15)
            buttons = self.chrome_driver.find_elements_by_xpath("//*[contains(text(), 'Accept')]")
            for btn in buttons:
                btn.click()

            sleep(0.15)
            eula = self.chrome_driver.find_element_by_class_name("markdown")
            self.chrome_driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', eula)
            buttons = self.chrome_driver.find_elements_by_xpath("//*[contains(text(), 'Accept')]")
            for btn in buttons:
                btn.click()

            sleep(0.15)
            den = self.chrome_driver.find_elements_by_xpath("//*[contains(text(), 'Import Existing DEN')]")
            for d in den:
                d.click()

            textarea = self.chrome_driver.find_element_by_class_name("twelve-word-phrase")
            password1 = self.chrome_driver.find_element_by_id("password-box")
            password2 = self.chrome_driver.find_element_by_id("password-box-confirm")

            while not self.guesses.empty():
                #Make sure form is clear
                self._clear_field(textarea)
                self._clear_field(password1)
                self._clear_field(password2)
                sleep(0.25)

                textarea.send_keys(' '.join(self.guesses.get()))
                password1.send_keys(CONST_PASS)
                password2.send_keys(CONST_PASS)

                ok_button = self.chrome_driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/button[2]')
                sleep(0.5)
                ok_button.click()

                self.guesses.task_done()

            print "Done. Exiting."
            return



if __name__ == "__main__":

    filename = "english.txt"
    known_list =     words = "test, dash, armed, best, egg, milk, kind, luggage, endorse, lamp, nephew"


    umm = Unmask_Meta(known_list, filename)
    umm.start_process()
