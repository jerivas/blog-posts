import os

import pytest
from playwright.sync_api import Browser, Page
from pytest_factoryboy import register

from . import factories

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
PLAYWRIGHT_TIMEOUT = float(os.getenv("PLAYWRIGHT_TIMEOUT", "3000"))


@pytest.fixture
def page(db, browser: Browser, live_server) -> Page:
    page = browser.new_page(base_url=str(live_server))
    page.set_default_timeout(PLAYWRIGHT_TIMEOUT)
    page.set_default_navigation_timeout(PLAYWRIGHT_TIMEOUT)
    yield page
    page.close()


# Adds `user` and `user_factory` fixtures
register(factories.UserFactory)
# Adds `blog_post` and `blog_post_factory` fixtures
register(factories.BlogPostFactory)
