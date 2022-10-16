import os

import pytest
from django.urls import reverse
from playwright.sync_api import Browser, Page
from pytest_factoryboy import register

from . import factories

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
PLAYWRIGHT_TIMEOUT = float(os.getenv("PLAYWRIGHT_TIMEOUT", "3000"))


@pytest.fixture
def assert_login_redirect(db, client, settings):
    def inner(*args, **kwargs):
        url = reverse(*args, **kwargs)
        response = client.get(url, follow=True)
        assert response.redirect_chain == [(f"{settings.LOGIN_URL}?next={url}", 302)]

    return inner


@pytest.fixture
def page(db, browser: Browser, live_server, client, user_factory) -> Page:
    """Start a Playwright page with a Django session already attached"""
    user = user_factory()
    client.force_login(user)
    cookies = [
        {
            "name": k,
            "value": v.value,
            "path": "/",
            "domain": "localhost",
            "sameSite": "Lax",
            "httpOnly": False,
            "secure": False,
        }
        for k, v in client.cookies.items()
    ]
    page = browser.new_page(
        storage_state={"cookies": cookies}, base_url=str(live_server)
    )
    page.user = user
    page.set_default_timeout(PLAYWRIGHT_TIMEOUT)
    page.set_default_navigation_timeout(PLAYWRIGHT_TIMEOUT)
    yield page
    page.close()


# Adds `user` and `user_factory` fixtures
register(factories.UserFactory)
# Adds `blog_post` and `blog_post_factory` fixtures
register(factories.BlogPostFactory)
