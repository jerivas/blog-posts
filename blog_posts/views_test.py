from playwright.sync_api import Page

from .models import BlogPost


def test_list(page: Page, blog_post_factory):
    post1, post2, post3 = blog_post_factory.create_batch(3)

    page.goto("/")

    assert page.locator("h2").all_inner_texts() == [post3.name, post2.name, post1.name]


def test_detail(page: Page, blog_post):
    page.goto("/")
    page.click(f"text={blog_post.name}")

    assert page.locator("h1").inner_text() == blog_post.name


def test_create(page: Page):
    page.goto("/")
    page.click("text=Publish")
    page.fill("text=Name", "Hello world!")
    page.fill("text=Text", "I wrote some text")
    with page.expect_navigation():
        page.click("text=Save")

    blog_post = BlogPost.objects.get()
    assert blog_post.author == page.user
    assert blog_post.name == "Hello world!"
    assert blog_post.text == "I wrote some text"
    assert page.locator("h1").inner_text() == "Hello world!"
