from playwright.sync_api import Page


def test_list(page: Page, blog_post_factory):
    post1, post2, post3 = blog_post_factory.create_batch(3)

    page.goto("/")

    assert page.locator("h2").all_inner_texts() == [post3.name, post2.name, post1.name]


def test_detail(page: Page, blog_post):
    page.goto("/")
    page.click(f"text={blog_post.name}")

    assert page.locator("h1").inner_text() == blog_post.name
