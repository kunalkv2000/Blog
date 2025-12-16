import pytest
from playwright.sync_api import expect
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

ADMIN_USER = {
    "email": os.getenv("ADMIN_USER_EMAIL"),
    "password": os.getenv("ADMIN_USER_PASSWORD")
}

REGULAR_USER = {
    "email": os.getenv("REGULAR_USER_EMAIL"),
    "password": os.getenv("REGULAR_USER_PASSWORD")
}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": BASE_URL,
    }


def login(page, email: str, password: str) -> None:
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    expect(page.get_by_role("heading", name="Blog Login")).to_be_visible(timeout=10000)
    page.get_by_placeholder("you@example.com").fill(email)
    page.get_by_placeholder("••••••••").fill(password)
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("networkidle")


def logout(page) -> None:
    logout_button = page.get_by_role("button", name="Logout")
    if logout_button.is_visible():
        logout_button.click()
        page.wait_for_load_state("networkidle")
