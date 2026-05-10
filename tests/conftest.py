import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright
from utils.config_loader import ConfigLoader

brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
PROJECT_ROOT = Path(__file__).parent.parent
DOWNLOAD_DIR = PROJECT_ROOT / "downloads"

@pytest.fixture(scope="session")
def config():
    return ConfigLoader.load()

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser(playwright_instance, config):
    if config["browser"] == "brave":
        browser = getattr(playwright_instance, "chromium").launch(executable_path=brave_path,
            headless=config["headless"],
            slow_mo=300
        )
    elif config["browser"] == "chrome":
        browser = getattr(playwright_instance, "chromium").launch(
            channel="chrome",  # pake channel, bukan executable_path
            headless=config["headless"],
            slow_mo=300
        )
    elif config["browser"] == "edge":
        browser = getattr(playwright_instance, "chromium").launch(
            channel="msedge",  # sama, chromium engine
            headless=config["headless"],
            slow_mo=300
        )
    else:
        browser = getattr(playwright_instance, config["browser"]).launch(
            headless=config["headless"],
            slow_mo=300
        )
    yield browser
    browser.close()

@pytest.fixture
def context(browser, config):
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(
        base_url=config["base_url"],
        viewport={"width": 2560, "height": 1440},
        # viewport=None,
        java_script_enabled=True,
        ignore_https_errors=True,
        accept_downloads=True,
    )
    context.set_default_timeout(30_000)
    context.set_default_navigation_timeout(60_000)  # khusus navigasi
    yield context
    context.close()

@pytest.fixture
def page(context, config):
    page = context.new_page()

    def handle_download(download):
        save_path = DOWNLOAD_DIR / download.suggested_filename
        download.save_as(save_path)

    page.on("download", handle_download)
    
    page.goto("/", wait_until="domcontentloaded")
    # page.set_default_timeout(config["timeout"])
    yield page
    page.close()