# -*- coding: utf-8 -*-
# this module contains the "main" crawling process

from src.crawler_pageobjects import (
    InstagramLoginPage,
    InstagramAccountPage,
    InstagramPostPage
)

crawler = InstagramLoginPage()
crawler.perform_login()
 
bill_gates_account = InstagramAccountPage(account_name='thisisbillgates',
                                          driver=crawler.driver)

print('Account Info: ', bill_gates_account.get_account_info())

# Get the first three posts
posts = bill_gates_account.get_posts_info(max_count=3)
print('Posts \n', posts)

links = [link for link, like_count, comment_count in posts]

first_post_link = links[0]

post_page = InstagramPostPage(post_link=first_post_link,
                              driver=bill_gates_account.driver)

comments = post_page.get_comments(verbose=True)
print(comments)
