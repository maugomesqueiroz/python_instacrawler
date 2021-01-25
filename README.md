# Instacrawler: Simple crawler for Instagram using Python

Instacrawler is a simple library designed to fetch information from Instagram website.

Key characteristics:
* Can obtain follower, following and posts count
* Scrape comments from posts
* Simple to use or modify
* Written using Selenium

## Quick Start
### Getting the Source Code and Requirements
```bash
git clone https://github.com/maugomesqueiroz/python_instacrawler.git
cd python_instacrawler
pip install -r requirements.txt
```

### Performing Login
If we wish to provide login information:

```python
from src.crawler_pageobjects import InstagramLoginPage

login_info = {'username': 'MyUser', 'password': '12345'}

crawler = InstagramLoginPage()
crawler.perform_login(login_info)
```

Alternatively, if we don't pass any arguments to the perform_login method, it will ask for input from user.

### Fetching account info
```python

from src.crawler_pageobjects import (
    InstagramLoginPage,
    InstagramAccountPage,
    InstagramPostPage
)

login_info = {'username': 'MyUser', 'password': '12345'}

crawler = InstagramLoginPage()
crawler.perform_login(login_info)

bill_gates_account = InstagramAccountPage(account_name='thisisbillgates', driver=crawler.driver)
print('Account Info: ', bill_gates_account.get_account_info())
```
### Fetching posts info
```python
posts = bill_gates_account.get_posts_info(max_count=3)
print('Posts \n', posts)
```

### Fetching comments from post
```python
link = 'https://www.instagram.com/p/B6JfheogQWK/'

post_page = InstagramPostPage(post_link=link, driver=bill_gates_account.driver)
comments = post_page.get_comments(verbose=True)

print(comments)
```
For additional information see [API Example](docs/API-EXAMPLE.md).

## Documentation
- [Features](docs/API-FEATURES.md)
- [API Example](docs/API-EXAMPLE.md)

## Contributing
You are free to contribute and make this project better!
