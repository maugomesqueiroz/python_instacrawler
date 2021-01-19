# -*- coding: utf-8 -*-
# this module contains the POM (Page Object Model) classes
# for the each page we want to crawl in
import os
import re 
import time
import pickle
import getpass 
import chromedriver_autoinstaller

from abc import ABC
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.wrappers import retry_this_if_error

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    ElementNotInteractableException,
    ElementClickInterceptedException
)

from src.crawler_locators import (
    LoginPage,
    PopUps,
    ToolBar,
    AccountPage,
    PostPage
)

from src.crawler_exceptions import (
    LoginError
    )
    

INSTAGRAM_HOME_PAGE = 'https://www.instagram.com/'

class WebPage(ABC):
    """Abstract WebPage class. Deals with Selenium API.

    Keyword arguments:
    webdriver -- Needs input driver that is being used.
    """

    def __init__(self, driver=None, network_conditions: tuple = None):
        if not driver:
            self.path = chromedriver_autoinstaller.install()
            self.chromeOptions = webdriver.ChromeOptions()
            self.chromeOptions.add_argument('--hide-scrollbars')
            self.chromeOptions.add_argument('--disable-gpu')
            self.chromeOptions.add_argument("--log-level=3")
            self.chromeOptions.add_argument("--incognito")
            self.chromeOptions.add_argument("--disable-plugins-discovery")
            self.chromeOptions.add_argument("--start-maximized")

            self.driver = webdriver.Chrome(self.path, options=self.chromeOptions)
            self.driver.delete_all_cookies()
        else:
            self.driver = driver


        if network_conditions:
            off, lat, dw_thr, up_thr = network_conditions
            self.driver.set_network_conditions(
                offline = off,
                latency = lat,
                download_throughput = dw_thr, 
                upload_throughput = up_thr
                )

    def start(self, url: str=''):
        """Starts a Chrome driver for this WebPage, fetches url provided,
        switches to window and maximizes it.
        """
        self.driver.get(url)
        self.main_window = self.driver.current_window_handle
        time.sleep(1)
        self.driver.switch_to.window(self.main_window)
        self.driver.maximize_window()    


    def save_cookies(self, filename: str = 'cookies.pkl'):
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open("cookies.pkl","wb"))

    def load_cookies(self, filename: str = 'cookies.pkl') -> bool:
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            return True
        except:
            return False


    def find_element(self, locator: tuple):
        return self.driver.find_element(*locator)

    def find_elements(self, locator: tuple):
        return self.driver.find_elements(*locator)

    def write_text(self, locator: tuple, text: str, clear_field_before: bool = False):
        '''
        #TODO:doc
        '''
        element = self.driver.find_element(*locator)
        if clear_field_before:
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)

        element.send_keys(text)
        return element

    def get_text(self, locator: tuple):
        try:
            return self.driver.find_element(*locator).text
        except:
            return None


    def scroll_to_element(self, locator: tuple = None, element: WebElement = None) -> WebElement:
        ''' Scroll to element using selenium Action Chains.
        Moves mouse to element, causing the page to scroll to it.

        Keyword arguments:
        locator -- locator of element to scroll to
        '''

        if locator:
            source = self.driver.find_element(*locator)
        elif element:
            source = element
        else:
            raise ValueError("Please provide locator/element as input.")

        action = ActionChains(self.driver)
        action.move_to_element(source).perform()

        return source


    def wait_locator(self, locator: tuple, max_time: int = 10):
        return WebDriverWait(self.driver, max_time).until(
                EC.presence_of_element_located(locator)  
            )

    def wait_to_be_clickable(self, locator: tuple, max_time: int = 10):
        return WebDriverWait(self.driver, max_time).until(
                EC.element_to_be_clickable(locator)  
            )

    def wait_text(self, locator: tuple, text, max_time: int = 10):
        return WebDriverWait(self.driver, max_time).until(
                EC.text_to_be_present_in_element(locator, text)  
            )


class InstagramLoginPage(WebPage):
    """ Instagram Login Page methods.
    """

    def __init__(self, driver=None, network_conditions: tuple = None):
        super(InstagramLoginPage, self).__init__(driver, network_conditions)
        if self.driver.current_url != INSTAGRAM_HOME_PAGE:
            self.driver.get(INSTAGRAM_HOME_PAGE)


    @retry_this_if_error(max_attempts=3)
    def perform_login(self, login_info: dict = None):
        ''' Performs Login into Instagram Account
        
        Keyword arguments:
        login_info -- dict with login_info, defaults to None. If not provided,
        user will be propted to insert info instead.
        The dict must be like: {'username': 'MyUser', 'password': '12345'}
        '''

        if not login_info:
            self.username = input('Instagram Username: ') 
            password = getpass.getpass(prompt='Instagram Password: ') 
        else:
            try:
                self.username = login_info['username']
                password = login_info['password']
            except KeyError:
                print("Login Info dict must be like: {'username': 'MyUser', 'password': '12345'}")
                raise('Login Info dict in bad format')

        self.write_text(LoginPage.USERNAME_FIELD, self.username , clear_field_before=True)
        self.write_text(LoginPage.PASSWORD_FIELD, password, clear_field_before=True)
        password = None

        try:
            self.find_element(LoginPage.SUBMIT_BUTTON).click()
        except ElementClickInterceptedException:
            print('Login form not filled properly')
            raise

        time.sleep(2)

        if self.driver.current_url == INSTAGRAM_HOME_PAGE:
            try:
                login_error_message = self.get_text(LoginPage.ALERT_PARAGRAPH)
                if login_error_message:
                    raise LoginError(login_error_message)
            except LoginError:
                print(login_error_message)
                raise

        time.sleep(2)

        self.driver.get(INSTAGRAM_HOME_PAGE)

        try:
            self.wait_locator(PopUps.DIALOG_WINDOW, max_time= 5)
            self.find_element(PopUps.NOT_NOW_BUTTON).click()
        except TimeoutException:
            pass


class InstagramAccountPage(WebPage):
    '''Instagram Account Page methods
    '''
    def __init__(self, account_name, driver=None, network_conditions: tuple = None):
        super(InstagramAccountPage, self).__init__(driver, network_conditions)
        self.account_name = account_name
        self.target_account_url = INSTAGRAM_HOME_PAGE + account_name
        self.driver.get(self.target_account_url)

        time.sleep(2)

        if self.driver.current_url == 'https://www.instagram.com/accounts/login/':
            print(f'Driver tried to go to {self.target_account_url} but was redirected to Login page!')


    def get_account_info(self) -> dict:
        '''
        #TODO: This docstring
        '''

        name = self.find_element(AccountPage.NAME).text
        followers_text = self.find_element(AccountPage.FOLLOWERS).text
        following_text = self.find_element(AccountPage.FOLLOWING).text

        number_followers = followers_text.split(" ")[0]
        number_following = following_text.split(" ")[0]

        #TODO: Process numbers

        account_info = {
            'account_name': name,
            'followers': number_followers,
            'following': number_following
        }

        return account_info


    def get_posts_info(self, max_count: int = None) -> list:
        '''Fetches posts info that are available upon mouse hover and the href of the post.

        Keyword arguments:
            max_count -- maximum number of posts to fetch.
        '''

        visited_list = []
        post_info_list = []
        last_scroll_height = 0
        current_scroll_height = self.driver.execute_script("return document.body.scrollHeight")

        reached_max_count = False
        while current_scroll_height > last_scroll_height and not reached_max_count:

            posts_elements = self.driver.find_elements(*AccountPage.POSTS)

            for post in posts_elements:
                if post not in visited_list:
                    link = post.get_attribute('href')

                    focused_post = self.scroll_to_element(element=post)

                    likes_and_comments = focused_post.find_elements_by_xpath(AccountPage.LIKES_COMMENTS_FROM_POSTS)
                    likes, comments = [element.text for element in likes_and_comments]

                    post_info_list.append((link, likes, comments))
                    visited_list.append(post)

                    if max_count:
                        reached_max_count = len(post_info_list) >= max_count 
                        if reached_max_count:
                            return post_info_list

            last_scroll_height = current_scroll_height
            current_scroll_height = self.driver.execute_script("return document.body.scrollHeight")

        return post_info_list


class InstagramPostPage(WebPage):
    """ Instagram Post Page methods.
    """

    def __init__(self, post_link: str = None, driver=None, network_conditions: tuple = None):
        super(InstagramPostPage, self).__init__(driver, network_conditions)

        if post_link and self.driver.current_url != post_link:
            self.driver.get(post_link)
  
    def get_comments(self, load_wait_time: float = 1, max_load_more_tries: int = 3, verbose: bool = False):
        '''Fetches comments, clicking in "Load more comments", until no new comments are return after
        a maximum amount of tries.

        Keyword arguments:
            load_wait_time -- Time to wait after clicking in "Load more comments".
            max_load_more_tries -- Maximum amount of tries to load more comments.
            verbose -- Verbose level for this function, defaults to False.
        '''
        
        comments = self.find_elements(PostPage.COMMENT)
        
        no_new_comments = 0
        last_comment_count = len(comments)

        while no_new_comments < max_load_more_tries:
            if verbose:
                print('Comment count: ', last_comment_count, ' ...')
            try:
                self.scroll_to_element(PostPage.MORE_COMMENTS_BUTTON)
                self.find_element(PostPage.MORE_COMMENTS_BUTTON).click()
                time.sleep(load_wait_time)

                comments = self.find_elements(PostPage.COMMENT)
                current_comment_count = len(comments)

                if last_comment_count == current_comment_count:
                    no_new_comments += 1
                else: 
                    no_new_comments = 0

                last_comment_count = current_comment_count
                
            except NoSuchElementException:
                no_new_comments += 1

        user_comment_tuples = []
        for element in comments:
            comment = element.text
            comment = comment.strip().replace('\n', ' ')

            try:
                username = element.find_element_by_xpath(PostPage.NAME_FROM_COMMENT[1]).text
            except:
                #TODO: Get proper username in this case
                username = None
            user_comment_tuples.append((username, comment))

        return user_comment_tuples