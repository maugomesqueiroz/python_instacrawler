# -*- coding: utf-8 -*-
# this module contains the XPATH locators
# for the elements in each page
 
from selenium.webdriver.common.by import By

class LoginPage(object):
    USERNAME_FIELD = (By.XPATH, '//input[@name="username"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@name="password"]')
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    ALERT_PARAGRAPH = (By.XPATH, '//form[@id="loginForm"]//p[@role="alert"]')


class PopUps(object):
    DIALOG_WINDOW = (By.XPATH, '//div[@role="dialog"]')
    TURN_ON_NOTIFICATIONS = (By.XPATH, '//h2[contains(text(),"Notifications")]')
    NOT_NOW_BUTTON = (By.XPATH, '//button[contains(text(),"Not Now")]')


class ToolBar(object):
    HOME = (By.XPATH, '//a[@href="/"]')
    SEARCH = (By.XPATH, '//input[@placeholder="Search"]')
    DIRECT_MESSAGES = (By.XPATH, '//a[@href="/direct/inbox/"]')


class AccountPage(object):
    NAME = (By.XPATH, '//header//section//h2')
    FOLLOWERS = (By.XPATH, '//a[contains(@href, "followers")]')
    FOLLOWING = (By.XPATH, '//a[contains(@href, "following")]')
    POSTS = (By.XPATH, '//article//a[contains(@href, "p/")]')
    LIKES_COMMENTS_FROM_POSTS = './/li[contains(text(), "")]'


class PostPage(object):
    CLOSE = (By.XPATH, '//*[@aria-label="Close"]')
    COMMENT = (By.XPATH, '//article[@role="presentation"]//div/ul//span[@class="" and text()]')
    NAME_FROM_COMMENT = (By.XPATH,'../h3//a[contains(text(),"")]')
    MORE_COMMENTS_BUTTON = (By.XPATH, '//span[@aria-label="Load more comments"]')