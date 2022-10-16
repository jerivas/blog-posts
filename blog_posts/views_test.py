import pytest
from django.urls import reverse
from playwright.sync_api import Page

from .models import BlogPost


class TestList:
    def test_ok(self, page: Page, blog_post_factory):
        post1, post2, post3 = blog_post_factory.create_batch(3)

        page.goto("/")

        assert page.locator("h2").all_inner_texts() == [
            post3.name,
            post2.name,
            post1.name,
        ]

    def test_filter(self, page: Page, blog_post_factory):
        posts = blog_post_factory.create_batch(3)

        page.goto("/")
        assert page.locator("h2").count() == 3

        with page.expect_navigation():
            page.select_option("text=Author", label=str(posts[0].author))
        assert page.locator("h2").all_inner_texts() == [posts[0].name]


class TestDetail:
    def test_anon(self, page: Page, blog_post):
        page.context.clear_cookies()  # Log out

        page.goto("/")
        page.click(f"text={blog_post.name}")

        assert page.locator("h1").inner_text() == blog_post.name
        assert not page.locator("text=Update").is_visible()
        assert not page.locator("text=Delete").is_visible()

    def test_non_author(self, page: Page, blog_post):
        page.goto("/")
        page.click(f"text={blog_post.name}")

        assert page.locator("h1").inner_text() == blog_post.name
        assert not page.locator("text=Update").is_visible()
        assert not page.locator("text=Delete").is_visible()

    def test_ok(self, page: Page, blog_post_factory):
        blog_post = blog_post_factory(author=page.user)

        page.goto("/")
        page.click(f"text={blog_post.name}")

        assert page.locator("h1").inner_text() == blog_post.name
        assert page.locator("text=Update").is_visible()
        assert page.locator("text=Delete").is_visible()


class TestCreate:
    def test_ok(self, page: Page):
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

    def test_login_redirect(self, assert_login_redirect):
        assert_login_redirect("blog_post_create")


class TestUpdate:
    def test_ok(self, page: Page, blog_post_factory):
        blog_post = blog_post_factory(author=page.user)

        page.goto(blog_post.get_absolute_url())
        page.click("text=Update")
        page.fill("text=Name", "New name")
        page.fill("text=Text", "New text")
        with page.expect_navigation():
            page.click("text=Save")

        blog_post.refresh_from_db()
        assert blog_post.name == "New name"
        assert blog_post.text == "New text"
        assert page.locator("h1").inner_text() == "New name"

    def test_login_redirect(self, assert_login_redirect, blog_post):
        assert_login_redirect("blog_post_update", args=(blog_post.pk,))

    @pytest.mark.django_db
    def test_non_author(self, client, user_factory, blog_post):
        client.force_login(user_factory())

        response = client.get(reverse("blog_post_update", args=(blog_post.pk,)))

        assert response.status_code == 403


class TestDelete:
    def test_ok(self, page: Page, blog_post_factory):
        blog_post = blog_post_factory(author=page.user)

        page.goto(blog_post.get_absolute_url())
        page.click("text=Delete")
        with page.expect_navigation():
            page.click("input:text('Delete')")

        with pytest.raises(BlogPost.DoesNotExist):
            blog_post.refresh_from_db()
        assert page.locator("h1").inner_text() == "Blog Posts"

    def test_login_redirect(self, assert_login_redirect, blog_post):
        assert_login_redirect("blog_post_delete", args=(blog_post.pk,))

    @pytest.mark.django_db
    def test_non_author(self, client, user_factory, blog_post):
        client.force_login(user_factory())

        response = client.get(reverse("blog_post_delete", args=(blog_post.pk,)))

        assert response.status_code == 403
