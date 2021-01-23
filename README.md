# Istacrawler: Simple crawler for instagram using Python

Instacrawler is a simple library designed to fetch information from Intagram website.

Key characteristics:
* Can obtain follower, following and posts count
* Scrape comments from posts
* Simple to use or modify
* Written using Selenium

## Quick Start
### Getting the sources
```bash
git clone https://github.com/maugomesqueiroz/python_instacrawler.git
cd python_instacrawler 
```

### Performing Login
Asking for input from user:

```python
from src.crawler_pageobjects import InstagramLoginPage

crawler = InstagramLoginPage()
crawler.perform_login()
```

If we wish to provide login information:

```python
from src.crawler_pageobjects import InstagramLoginPage

login_info = {'username': 'MyUser', 'password': '12345'}

crawler = InstagramLoginPage()
crawler.perform_login(login_info)
```

For additional information see [API Example](docs/API-EXAMPLE.md).

## Documentation
- [Features](docs/API-FEATURES.md)
- [API Example](docs/API-EXAMPLE.md)

## Contributing
You are free to contribute and make this project better!
