import logging
from utils.ui_actions import UIActions
from utils.word_generator import WordGenerator
logging = logging.getLogger(__name__)

class PaymentPage:

    def __init__(self, page):
        self.ui = UIActions(page)
        self.page = page

        self.CC_NAME_FIELD = page.locator("[name='name_on_card']")
        self.CC_NUMBER_FIELD = page.locator("[name='card_number']")
        self.CC_CVV_FIELD = page.get_by_role("textbox", name="ex. 311")
        self.CC_EXP_MONTH_FIELD = page.get_by_role("textbox", name="MM")
        self.CC_EXP_YEAR_FIELD = page.get_by_role("textbox", name="YYYY")
        self.PAY_AND_CONFIRM_BTN = page.get_by_role("button", name="Pay and Confirm Order")

        self.ORDER_SUCCESS_MSG = page.get_by_text("Congratulations! Your order has been confirmed!", exact=True)
        self.DOWNLOAD_INVOICE_BTN = page.get_by_role("link", name="Download Invoice")
        self.CONTINUE_BTN = page.get_by_role("link", name="Continue")


    def pay_and_confirm(self, document, cc_name, cc_number, cc_cvv, cc_exp_month, cc_exp_year):
        try:
            self.ui.fill(self.CC_NAME_FIELD, cc_name)
            logging.info(f"Fill name on card field with {cc_name}")
            self.ui.fill(self.CC_NUMBER_FIELD, cc_number)
            logging.info(f"Fill card number field with {cc_number}")
            self.ui.fill(self.CC_CVV_FIELD, cc_cvv)
            logging.info(f"Fill CVV field with {cc_cvv}")
            self.ui.fill(self.CC_EXP_MONTH_FIELD, cc_exp_month)
            logging.info(f"Fill expiration month field with {cc_exp_month}")
            self.ui.fill(self.CC_EXP_YEAR_FIELD, cc_exp_year)
            logging.info(f"Fill expiration year field with {cc_exp_year}")
            WordGenerator.add_screenshot_only(self, document, "payment_filled.png", True)
            self.ui.click(self.PAY_AND_CONFIRM_BTN)
            logging.info("Click on pay and confirm button")
            self.ui.should_be_visible(self.ORDER_SUCCESS_MSG)
            WordGenerator.add_screenshot_only(self, document, "order_confirmed.png", True)
            self.ui.click(self.DOWNLOAD_INVOICE_BTN)
            logging.info("Click on download invoice button")
        except Exception as e:
            logging.error(e)
            WordGenerator.add_heading_fail(self, document, "Failed to pay and confirm order", level=2)
            WordGenerator.add_screenshot_only(self, document, "payment_failed.png", True)
            raise e