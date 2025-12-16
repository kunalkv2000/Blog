import time
import pytest
from playwright.sync_api import expect
from conftest import login, logout, ADMIN_USER, REGULAR_USER


class TestBlogApplication:
    def test_admin_can_create_blog_post(self, page) -> None:
        login(page, ADMIN_USER["email"], ADMIN_USER["password"])
        
        expect(page.get_by_role("heading", name="Manage Post")).to_be_visible(timeout=10000)
        
        page.get_by_role("button", name="New Post").click()
        
        expect(page.get_by_role("heading", name="Create Post")).to_be_visible()
        
        post_title = f"Test Post {int(time.time() * 1000)}"
        post_content = "This is an automated test post created by Playwright Python."
        
        page.get_by_label("Title").fill(post_title)
        page.get_by_label("Content").fill(post_content)
        
        page.get_by_role("button", name="Create Post").click()
        
        page.wait_for_timeout(2000)
        
        expect(page.get_by_text(post_title)).to_be_visible(timeout=10000)

    def test_user_can_add_comment(self, page) -> None:
        login(page, REGULAR_USER["email"], REGULAR_USER["password"])
        
        expect(page.get_by_role("heading", name="Explore Blogs")).to_be_visible(timeout=10000)
        page.wait_for_timeout(2000)
        
        first_post = page.locator("article").first
        first_post.click()
        
        expect(page.get_by_placeholder("Write a comment...")).to_be_visible(timeout=5000)
        
        comment_text = f"Test comment from Playwright Python - {int(time.time() * 1000)}"
        page.get_by_placeholder("Write a comment...").fill(comment_text)
        page.get_by_role("button", name="Submit Comment").click()
        
        page.wait_for_timeout(2000)
        
        expect(page.get_by_text(comment_text)).to_be_visible(timeout=10000)