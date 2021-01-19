# -*- coding: utf-8 -*-
# this module contains the "main" crawling process

import time
import pandas as pd
import pickle

from src.crawler_pageobjects import (
    InstagramLoginPage,
    InstagramAccountPage,
    InstagramPostPage
)
from src.crawler_locators import (
PopUps
)


crawler = InstagramLoginPage()

try:
    crawler.load_cookies()
    try:
        crawler.wait_locator(PopUps.DIALOG_WINDOW, max_time= 5)
        crawler.find_element(PopUps.NOT_NOW_BUTTON).click()
    except:
        pass

except Exception:
    print('could not load cookies')
    crawler.perform_login()
    crawler.save_cookies()

nubank = InstagramAccountPage(account_name='nubank', driver=crawler.driver)
print('Account Info: ', nubank.get_account_info() )


posts = nubank.get_posts_info(max_count=3)
print('Posts \n', posts)

links = [link for link,*_ in posts]

link_comments = []
for link in links[:1]:
    post_page = InstagramPostPage(post_link=link, driver=nubank.driver)
    comments = post_page.get_comments(max_load_more_tries = 4, verbose=True)

    link_comments.append((link, comments))

with open("new_output.txt", "w", encoding='utf-8') as f:
    for link, comments in link_comments:
        for user,comment in comments:
            f.write(f'"{link}"\t"{user}"\t"{comment}"\n')
print('end')


