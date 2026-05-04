from playwright.sync_api import Page, expect

class UIActions:
    def __init__(self, page: Page):
        self.page = page

    # ---------- Navigation ----------
    def open(self, url: str = "/"):
        self.page.goto(url)

    # ---------- Input ----------
    def fill(self, locator, value: str):
        element = locator
        element.wait_for(state="visible")
        element.fill(value)

    def clear_and_fill(self, locator, value: str):
        element = locator
        element.wait_for(state="visible")
        element.fill("")
        element.fill(value)

    # ---------- Click ----------
    def click(self, locator):
        element = locator
        element.wait_for(state="visible")
        element.click()

    def click_force(self, locator):
        locator.click(force=True)

    def javascript_click(self, locator):
        element = locator
        element.wait_for(state="visible")
        element.evaluate("el => el.click()")

    def smooth_scroll(self, locator):
        element = locator
        element.wait_for(state="visible")
        self.page.evaluate("element => element.scrollIntoView({ behavior: 'smooth', block: 'center' })", element)

    # ---------- Text / State ----------
    def get_text(self, locator) -> str:
        element = locator
        element.wait_for(state="visible")
        return element.inner_text()

    def is_visible(self, locator) -> bool:
        return locator.is_visible()

    # ---------- Assertions ----------
    def should_have_text(self, locator, text: str):
        expect(locator).to_have_text(text)

    def should_be_visible(self, locator):
        expect(locator).to_be_visible()

    # ---------- Utilities ----------
    def wait_for_url(self, partial_url: str):
        self.page.wait_for_url(f"**{partial_url}**")

    def save_screenshot(self, path: str, full_page: bool = False):
        self.page.screenshot(path=path, full_page=full_page)

    def select_option(self, locator, value: str):
        element = locator
        element.wait_for(state="visible")
        element.select_option(value)