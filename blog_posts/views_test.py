import os

from playwright.sync_api import Browser

from .factories import BlogPostFactory

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


def test_list(live_server, browser: Browser):
    page = browser.new_page(base_url=str(live_server))
    post1, post2, post3 = BlogPostFactory.create_batch(3)

    page.goto("/")

    assert page.locator("h2").all_inner_texts() == [post3.name, post2.name, post1.name]
