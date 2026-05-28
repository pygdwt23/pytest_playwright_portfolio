import email
import logging
from utils.ui_actions import UIActions
from utils.word_generator import WordGenerator
logging = logging.getLogger(__name__)

class AuthPage:

    def __init__(self, page):
        self.ui = UIActions(page)
        self.page = page
        self.LOGIN_LINK = page.get_by_role('link', name='Signup / Login')
        self.NAME_FIELD = page.locator('[data-qa="signup-name"]')
        self.EMAIL_FIELD = page.locator('[data-qa="signup-email"]')
        self.SIGNUP_BUTTON = page.locator('[data-qa="signup-button"]')
        self.MR_TITLE = page.get_by_role('radio', name='Mr.', checked=False)
        self.MRS_TITLE = page.get_by_role('radio', name='Mrs.', checked=False)
        self.PASSWORD_FIELD = page.locator('[data-qa="password"]')
        self.BIRTH_DATE_DROPDOWN = page.locator('[data-qa="days"]')
        self.BIRTH_MONTH_DROPDOWN = page.locator('[data-qa="months"]')
        self.BIRTH_YEAR_DROPDOWN = page.locator('[data-qa="years"]')
        self.NEWSLETTER_CHECKBOX = page.get_by_role('checkbox', name='Sign up for our newsletter!', checked=False)
        self.OFFERS_CHECKBOX = page.get_by_role('checkbox', name='Receive special offers from our partners!', checked=False)
        self.FIRSTNAME_FIELD = page.locator('[data-qa="first_name"]')
        self.LASTNAME_FIELD = page.locator('[data-qa="last_name"]')
        self.COMPANY_FIELD = page.locator('[data-qa="company"]')
        self.ADDRESS_FIELD = page.locator('[data-qa="address"]')
        self.COUNTRY_DROPDOWN = page.locator('[data-qa="country"]')
        self.STATE_FIELD = page.locator('[data-qa="state"]')
        self.CITY_FIELD = page.locator('[data-qa="city"]')
        self.ZIPCODE_FIELD = page.locator('[data-qa="zipcode"]')
        self.MOBILE_FIELD = page.locator('[data-qa="mobile_number"]')
        self.CREATE_ACCOUNT_BUTTON = page.locator('[data-qa="create-account"]')
        self.ACCOUNT_CREATED_MSG = page.locator('[data-qa="account-created"]')
        self.LOGGED_IN_ACCOUNT = page.locator('a:has-text("Logged in as")')
        self.DELETE_ACCOUNT_BTN = page.locator('//a[normalize-space()="Delete Account"]')
        self.ACCOUNT_DELETED_MSG = page.locator('//b[normalize-space()="Account Deleted!"]')
        self.LOGOUT_BTN = page.locator('//a[normalize-space()="Logout"]')
        self.EMAIL_LOGIN_FIELD = page.locator('[data-qa="login-email"]')
        self.PASSWORD_LOGIN_FIELD = page.locator('[data-qa="login-password"]')
        self.LOGIN_BTN = page.locator('[data-qa="login-button"]')
        self.ERROR_LOGIN_MSG = page.locator('//p[normalize-space()="Your email or password is incorrect!"]')


    def signup(self, name, email, document):
        WordGenerator.add_heading(self, document, "Signup Process", 2)
        try:
            self.ui.click(self.LOGIN_LINK)
            logging.info("Clicking Signup / Login link")
            self.ui.fill(self.NAME_FIELD, name)
            logging.info(f"Filling name: {name}")
            self.ui.fill(self.EMAIL_FIELD, email)
            logging.info(f"Filling email: {email}")
            self.ui.wait_for_url("/login")
            # self.ui.save_screenshot("screenshots/signup_page.png", full_page=True)
            WordGenerator.add_screenshot_with_description(self, document, "Sign Up Data", "signup.png", True)
            self.ui.click(self.SIGNUP_BUTTON)
            logging.info("Clicking Signup / Login link")
        except Exception as e:
            logging.error(f"Error during signup: {e}")
            raise e

    def login_alt(self, name, email, password, document):
        WordGenerator.add_heading(self, document, "Login Process", 2)

        try:
            self.ui.click(self.LOGIN_LINK)
            logging.info("Clicking Signup / Login link")

            # ── Blank data cases ──────────────────────────────
            blank_cases = [
                ("Login Blank Data", "", "", "login-email"),
                ("Login Blank Email", "", password, "login-email"),
                ("Login Blank Password", email, "", "login-password"),
            ]

            for label, em, pw, field in blank_cases:
                self.ui.fill(self.EMAIL_LOGIN_FIELD, em)
                self.ui.fill(self.PASSWORD_LOGIN_FIELD, pw)
                self.ui.click(self.LOGIN_BTN)

                is_valid = self.page.evaluate(
                    f"document.querySelector('input[data-qa=\"{field}\"]').validity.valueMissing"
                )
                assert is_valid, f"[{label}] Expected valueMissing=True"
                logging.info(f"{label}: validation passed")
                WordGenerator.add_screenshot_with_description(self, document, label, "login.png", True)

            # ── Invalid data cases ────────────────────────────
            expected_error = "Your email or password is incorrect!"

            invalid_cases = [
                ("Login Invalid Data", f"{email}123", f"{password}123"),
                ("Login Invalid Email", f"{email}123", password),
                ("Login Invalid Password", email, f"{password}123"),
            ]

            for label, em, pw in invalid_cases:
                self.ui.fill(self.EMAIL_LOGIN_FIELD, em)
                self.ui.fill(self.PASSWORD_LOGIN_FIELD, pw)
                self.ui.click(self.LOGIN_BTN)

                actual_error = self.ui.get_text(self.ERROR_LOGIN_MSG)
                assert actual_error == expected_error, \
                    f"[{label}] Expected: '{expected_error}', Got: '{actual_error}'"
                logging.info(f"{label}: error message validated")
                WordGenerator.add_screenshot_with_description(self, document, label, "login.png", True)

            # ── Valid login ───────────────────────────────────
            self.ui.fill(self.EMAIL_LOGIN_FIELD, email)
            self.ui.fill(self.PASSWORD_LOGIN_FIELD, password)
            WordGenerator.add_screenshot_with_description(self, document, "Login Data", "login.png", True)
            self.ui.click(self.LOGIN_BTN)
            logging.info("Clicking Login button")

            user_text = self.ui.get_text(self.LOGGED_IN_ACCOUNT)
            assert name in user_text, f"Expected '{name}' in '{user_text}'"
            WordGenerator.add_screenshot_with_description(self, document, user_text, "login.png", True)

        except Exception as e:
            logging.error(f"Error during login: {e}")
            WordGenerator.add_heading_fail(self, document, "FAIL", 3)
            WordGenerator.add_screenshot_only(self, document, "login_error.png", True)
            raise e

    def app_form(self, password, title, birth_date, birth_month, birth_year, newsletter, offers, firstname, lastname, company, address, country, state, zipcode, mobile, email, document):
        WordGenerator.add_heading(self, document, "Account Creation Form", 2)
        try:
            if title == "Mr":
                self.ui.click(self.MR_TITLE)
            elif title == "Mrs":
                self.ui.click(self.MRS_TITLE)
            logging.info(f"Selecting title: {title}")
            self.ui.fill(self.PASSWORD_FIELD, password)
            logging.info(f"Filling password: ********")
            self.ui.select_option(self.BIRTH_DATE_DROPDOWN, birth_date)
            logging.info(f"Filling birth date: {birth_date}")
            logging.info(f"Filling birth month: {birth_month}")
            self.ui.select_option(self.BIRTH_MONTH_DROPDOWN, birth_month)
            self.ui.select_option(self.BIRTH_YEAR_DROPDOWN, birth_year)
            logging.info(f"Filling birth year: {birth_year}")
            logging.info(f"Sign up newsletter? ==> {newsletter}")
            # self.ui.smooth_scroll(self.NEWSLETTER_CHECKBOX)
            if newsletter:
                self.ui.click(self.NEWSLETTER_CHECKBOX)
            logging.info(f"Receive special offers? ==> {offers}")
            if offers:
                self.ui.click(self.OFFERS_CHECKBOX)
            logging.info(f"Filling first name: {firstname}")
            self.ui.fill(self.FIRSTNAME_FIELD, firstname)
            logging.info(f"Filling last name: {lastname}")
            self.ui.fill(self.LASTNAME_FIELD, lastname)
            logging.info(f"Filling company: {company}")
            self.ui.fill(self.COMPANY_FIELD, company)
            logging.info(f"Filling address: {address}")
            self.ui.fill(self.ADDRESS_FIELD, address)
            logging.info(f"Selected country: {country}")
            self.ui.select_option(self.COUNTRY_DROPDOWN, country)
            logging.info(f"Filling state: {country}")
            self.ui.fill(self.STATE_FIELD, country)
            logging.info(f"Filling city: {state}")
            self.ui.fill(self.CITY_FIELD, state)
            logging.info(f"Filling zipcode: {zipcode}")
            self.ui.fill(self.ZIPCODE_FIELD, zipcode)
            logging.info(f"Filling mobile: {mobile}")
            self.ui.fill(self.MOBILE_FIELD, mobile)
            WordGenerator.add_screenshot_with_description(self, document, "Form Data", "form_app.png", True)
            WordGenerator.add_heading(self, document, "Registration Data", 3)
            WordGenerator.add_text(self, document, f"Title: {title}")
            WordGenerator.add_text(self, document, f"Name: {firstname} {lastname}")
            WordGenerator.add_text(self, document, f"Date of Birth: {birth_date} {birth_month} {birth_year}")
            WordGenerator.add_text(self, document, f"Email: {email}")
            WordGenerator.add_text(self, document, f"Mobile: {mobile}")
            WordGenerator.add_text(self, document, f"Company: {company}")
            WordGenerator.add_text(self, document, f"Address: {address}")
            WordGenerator.add_text(self, document, f"Country: {country}")
            WordGenerator.add_text(self, document, f"State: {state}")
            WordGenerator.add_text(self, document, f"Zipcode: {zipcode}")

            self.ui.click(self.CREATE_ACCOUNT_BUTTON)
            logging.info("Clicking Create Account")

            account_created_text = self.ui.get_text(self.ACCOUNT_CREATED_MSG)
            assert "ACCOUNT CREATED!" == account_created_text
            logging.info("Clicking Create Account")
            WordGenerator.add_screenshot_with_description(self, document, "Account Created", "account_created.png", True)

            return firstname, lastname, company, address, state, zipcode, mobile
        except Exception as e:
            logging.error(f"Error selecting title: {e}")
            WordGenerator.add_heading_fail(self, document, f"FAIL", 3)
            WordGenerator.add_screenshot_with_description(self, document,f"{e}", "account_creation_error.png", True)
            raise e

    def delete_account(self, document):
        WordGenerator.add_heading(self, document, "Account Deletion", 2)
        try:
            self.ui.click(self.DELETE_ACCOUNT_BTN)
            logging.info("Clicking Delete Account button")
            account_deleted_text = self.ui.get_text(self.ACCOUNT_DELETED_MSG)
            assert "ACCOUNT DELETED!" == account_deleted_text
            logging.info("Account deleted successfully")
            WordGenerator.add_screenshot_with_description(self, document, "Account Deleted", "account_deleted.png", True)
        except Exception as e:
            logging.error(f"Error during account deletion: {e}")
            WordGenerator.add_heading_fail(self, document, f"FAIL", 3)
            WordGenerator.add_screenshot_with_description(self, document,f"{e}", "account_deletion_error.png", True)
            raise e

    def log_out(self, document):
        WordGenerator.add_heading(self, document, "Logout Process", 2)
        try:
            self.ui.click(self.LOGOUT_BTN)
            logging.info("Clicking Logout button")
            WordGenerator.add_screenshot_with_description(self, document, "Logged Out", "logout.png", True)
        except Exception as e:
            logging.error(f"Error during logout: {e}")
            WordGenerator.add_heading_fail(self, document, f"FAIL", 3)
            WordGenerator.add_screenshot_with_description(self, document,f"{e}", "logout_error.png", True)
            raise e