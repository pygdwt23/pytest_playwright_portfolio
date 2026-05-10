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
        self.WOMEN_CATEGORY_OPT = page.locator("//a[normalize-space()='Women']//i[@class='fa fa-plus']")
        self.MEN_CATEGORY_OPT = page.get_by_role('heading', name='Men', level=4)
        self.KIDS_CATEGORY_OPT = page.get_by_role('heading', name='Kids', level=4)
        self.DRESS_LINK = page.get_by_role('link', name='Dress')
        self.KIDS_TOPS_LINK = page.get_by_role('link', name='Tops & Shirts')
        self.WOMEN_TOPS_LINK = page.get_by_role('link', name='Tops')
        self.WOMEN_SAREE_LINK = page.get_by_role('link', name='Saree')
        self.MEN_TSHIRT_LINK = page.get_by_role('link', name='Tshirts')
        self.MEN_JEANS_LINK = page.get_by_role('link', name='Jeans')
        self.POLO_LINK = page.get_by_role('link', name='Polo')
        self.H_AND_M_LINK = page.get_by_role('link', name='H&M')
        self.MADAME_LINK = page.get_by_role('link', name='Madame')
        self.MAST_HARBOUR_LINK = page.get_by_role('link', name='Mast & Harbour')
        self.BABYHUG_LINK = page.get_by_role('link', name='Babyhug')
        self.ALLEN_SOLLY_LINK = page.get_by_role('link', name='Allen Solly Junior')
        self.KOOKIE_LINK = page.get_by_role('link', name='Kookie Kids')
        self.BIBA_LINK = page.get_by_role('link', name='Biba')
        self.SLEEVELESS_DRESS_LINK = page.locator('//div[@class="overlay-content"]//p[.="Sleeveless Dress"]/following::a[.="Add to cart"][1]')
        self.PREMIUM_POLO_TSHIRTS = page.locator('//div[@class="overlay-content"]//p[.="Premium Polo T-Shirts"]/following::a[.="Add to cart"][1]')
        self.DELETE_CART_LINK = page.locator("//i[@class='fa fa-times']")
        self.EMPTY_CART_MSG = page.locator('//b[normalize-space()="Cart is empty!"]')



    def click_product_link(self, document):
        try:
            self.ui.click(self.PRODUCT_LINK)
            logging.info("Click on product link")
        except Exception as e:
            logging.error(e)
            WordGenerator.add_heading_fail(self, document, "Failed to click product link", level=2)
            WordGenerator.add_screenshot_only(self, document, "product_link_error.png")
            raise e

    def buy_product_by_search(self, product_name, document):
        WordGenerator.add_heading(self, document, "Buying Product by Search", level=2)
        try:
            self.click_product_link(document)
            logging.info("Click on product link")
            self.ui.fill(self.SEARCH_FIELD, product_name)
            logging.info(f"Fill search field with {product_name}")
            WordGenerator.add_screenshot_only(self, document, "search_filled.png")
            self.ui.click(self.SEARCH_BTN)
            logging.info("Click on search button")
            self.ui.javascript_click(self.ADD_TO_CART_BTN)
            logging.info("Click on cart button")
        except Exception as e:
            logging.error(e)
            WordGenerator.add_heading_fail(self, document, "Failed to buy product by search", level=2)
            WordGenerator.add_screenshot_only(self, document, "product_page_error.png")
            raise e

    def verify_added_to_cart(self, document):
        WordGenerator.add_heading(self, document, "Add to cart", level=2)
        try:
            self.ui.should_be_visible(self.ADD_TO_CART_SUCCESS_MSG)
            WordGenerator.add_screenshot_only(self, document, "add_to_cart.png")
            self.ui.click(self.VIEW_CART_LINK)
            logging.info("Click on view cart link")
            WordGenerator.add_screenshot_with_description(self, document, "Product added to cart successfully", "cart_page.png")
        except Exception as e:
            logging.error(e)
            WordGenerator.add_heading_fail(self, document, "Failed to view cart link", level=2)
            WordGenerator.add_screenshot_only(self, document, "view_cart.png")
            raise e

    def proceed_to_checkout(self, document, comment):
        WordGenerator.add_heading(self, document, "Proceed to checkout", level=2)
        try:
            self.ui.should_be_visible(self.PROCEED_TO_CHECKOUT_BTN)
            WordGenerator.add_screenshot_only(self, document, "proceed_to_checkout.png")
            self.ui.click(self.PROCEED_TO_CHECKOUT_BTN)
            logging.info("Click on proceed button")
            self.ui.fill(self.COMMENT_BOX, comment)
            logging.info(f"Fill comment with {comment}")
            WordGenerator.add_screenshot_only(self, document, "comment.png")
            self.ui.click(self.PLACE_ORDER_BTN)
            logging.info("Click on place order button")
            WordGenerator.add_screenshot_with_description(self, document,
                                                          "Product added to cart and proceeded to checkout",
                                                          "product_page.png")
        except Exception as e:
            logging.error(e)
            WordGenerator.add_heading_fail(self, document, "Failed to place order button", level=2)
            WordGenerator.add_screenshot_only(self, document, "place_order.png")
            raise e

    def buy_product_by_category(self, category, subcategory, document):
        WordGenerator.add_heading(self, document, "Buying Product by Category", level=2)
        try:
            self.click_product_link(document)
            if category == "women":
                self.ui.javascript_click(self.WOMEN_CATEGORY_OPT)
                logging.info(f"Click on {category} category option")
                if subcategory == "dress":
                    self.ui.click(self.DRESS_LINK)
                    logging.info(f"Click on {subcategory} subcategory option")
                    self.ui.javascript_click(self.SLEEVELESS_DRESS_LINK)
                    logging.info(f"Added Sleeveless Dress to cart")
                elif subcategory == "tops":
                    self.ui.click(self.WOMEN_TOPS_LINK)
                    logging.info(f"Click on {subcategory} subcategory option")
                elif subcategory == "saree":
                    self.ui.click(self.WOMEN_SAREE_LINK)
                    logging.info(f"Click on {subcategory} subcategory option")
                else:
                    logging.warning(f"{subcategory} subcategory option not found")
            elif category == "men":
                self.ui.click(self.MEN_CATEGORY_OPT)
                logging.info(f"Click on {category} category option")
                if subcategory == "tshirt":
                    self.ui.click(self.MEN_TSHIRT_LINK)
                    logging.info(f"Click on {subcategory} subcategory option")
                elif subcategory == "jeans":
                    self.ui.click(self.MEN_JEANS_LINK)
                    logging.info(f"Click on {subcategory} subcategory option")
                else:
                    logging.warning(f"{subcategory} subcategory option not found")
            elif category == "kids":
                self.ui.click(self.KIDS_CATEGORY_OPT)
                logging.info(f"Click on {category} category option")
                if subcategory == "tops":
                    self.ui.click(self.KIDS_TOPS_LINK)
                    logging.info(f"Click on {subcategory} subcategory option")
                elif subcategory == "dress":
                    self.ui.click(self.DRESS_LINK)
                    logging.info(f"Click on {subcategory} subcategory option")
                else:
                    logging.warning(f"{subcategory} subcategory option not found")
        except Exception as e:
            logging.error(e)
            WordGenerator.add_heading_fail(self, document, "Failed to buy product by category", level=2)
            WordGenerator.add_screenshot_only(self, document, "product_page_error.png")
            raise e

    def buy_product_by_brand(self, brand, document):
        WordGenerator.add_heading(self, document, "Buying Product by Brand", level=2)
        try:
            self.click_product_link(document)
            if brand == "h&m":
                self.ui.click(self.H_AND_M_LINK)
                logging.info(f"Click on {brand} brand option")
            elif brand == "polo":
                self.ui.click(self.POLO_LINK)
                logging.info(f"Click on {brand} brand option")
                self.ui.javascript_click(self.PREMIUM_POLO_TSHIRTS)
                logging.info(f"Added Premium Polo T-Shirts to cart")
            elif brand == "madame":
                self.ui.click(self.MADAME_LINK)
                logging.info(f"Click on {brand} brand option")
            elif brand == "mast & harbour":
                self.ui.click(self.MAST_HARBOUR_LINK)
                logging.info(f"Click on {brand} brand option")
            elif brand == "babyhug":
                self.ui.click(self.BABYHUG_LINK)
                logging.info(f"Click on {brand} brand option")
            elif brand == "allen solly junior":
                self.ui.click(self.ALLEN_SOLLY_LINK)
                logging.info(f"Click on {brand} brand option")
            elif brand == "kookie kids":
                self.ui.click(self.KOOKIE_LINK)
                logging.info(f"Click on {brand} brand option")
            elif brand == "biba":
                self.ui.click(self.BIBA_LINK)
                logging.info(f"Click on {brand} brand option")
            else:
                logging.warning(f"{brand} brand option not found")
        except Exception as e:
            logging.error(e)
            WordGenerator.add_heading_fail(self, document, "Failed to buy product by brand", level=2)
            WordGenerator.add_screenshot_only(self, document, "product_page_error.png")
            raise e

    def delete_from_cart(self, document):
        try:
            WordGenerator.add_heading(self, document, "Deleting from cart", level=2)
            self.ui.javascript_click(self.DELETE_CART_LINK)
            logging.info(f"Click on delete cart button")
            self.ui.should_be_visible(self.EMPTY_CART_MSG)
            empty_cart_msg = self.ui.get_text(self.EMPTY_CART_MSG)
            WordGenerator.add_screenshot_with_description(self, document, f"{empty_cart_msg}", "delete_from_cart.png")
        except Exception as e:
            logging.error(e)
            WordGenerator.add_heading_fail(self, document, "Failed to delete from cart", level=2)
            WordGenerator.add_screenshot_only(self, document, "product_page_error.png")
            raise e
