import logging
from utils.ui_actions import UIActions
from utils.word_generator import WordGenerator
logging = logging.getLogger(__name__)

class ProductPage:

    def __init__(self, page):
        self.ui = UIActions(page)
        self.page = page

        self.PRODUCT_LINK = page.locator("//a[@href='/products']")
        self.SEARCH_FIELD = page.get_by_role("textbox", name="Search Product")
        self.SEARCH_BTN = page.locator("#submit_search")
        self.TSHIRT_CARD = page.get_by_role('img', name='ecommerce website products')
        self.ADD_TO_CART_BTN = page.locator("//div[@class='overlay-content']//a[@class='btn btn-default add-to-cart'][normalize-space()='Add to cart']")
        self.ADD_TO_CART_BTN_2 = page.get_by_role("button", name="Add to cart")
        self.VIEW_PRODUCT_BTN = page.get_by_role("link", name="View Product")
        self.ADD_TO_CART_SUCCESS_MSG = page.get_by_text("Your product has been added to cart.", exact=True)
        self.CONTINUE_SHOPPING_BTN = page.get_by_role("button", name="Continue Shopping")
        self.VIEW_CART_LINK = page.get_by_text("View Cart", exact=True)
        self.PROCEED_TO_CHECKOUT_BTN = page.get_by_text("Proceed To Checkout", exact=True)
        self.COMMENT_BOX = page.locator("[name='message']")
        self.PLACE_ORDER_BTN = page.get_by_role("link", name="Place Order")


    def buy_product_by_search(self, product_name, comment, document):
        WordGenerator.add_heading(self, document, "Buying Product by Search", level=2)
        try:
            self.ui.click(self.PRODUCT_LINK)
            logging.info("Click on product link")
            self.ui.fill(self.SEARCH_FIELD, product_name)
            logging.info(f"Fill search field with {product_name}")
            WordGenerator.add_screenshot_only(self, document, "search_filled.png")
            self.ui.click(self.SEARCH_BTN)
            logging.info("Click on search button")
            self.ui.javascript_click(self.ADD_TO_CART_BTN)
            logging.info("Click on cart button")
            self.ui.should_be_visible(self.ADD_TO_CART_SUCCESS_MSG)
            WordGenerator.add_screenshot_only(self, document, "add_to_cart.png")
            self.ui.click(self.VIEW_CART_LINK)
            logging.info("Click on cart button")
            self.ui.should_be_visible(self.PROCEED_TO_CHECKOUT_BTN)
            WordGenerator.add_screenshot_only(self, document, "proceed_to_checkout.png")
            self.ui.click(self.PROCEED_TO_CHECKOUT_BTN)
            logging.info("Click on proceed button")
            self.ui.fill(self.COMMENT_BOX, comment)
            logging.info(f"Fill comment with {comment}")
            WordGenerator.add_screenshot_only(self, document, "comment.png")
            self.ui.click(self.PLACE_ORDER_BTN)
            logging.info("Click on place order button")
            WordGenerator.add_screenshot_with_description(self,document, "Product added to cart and proceeded to checkout", "product_page.png")
        except Exception as e:
            logging.error(e)
            WordGenerator.add_heading_fail(self, document, "Failed to buy product by search", level=2)
            WordGenerator.add_screenshot_only(self, document, "product_page_error.png")
            raise e