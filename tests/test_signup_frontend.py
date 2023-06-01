from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import app, db
from app.models import Message
from secret.secret import GECKO_PATH

# USE IN-MEMORY DATABASE TO SAVE CLEANING UP FILES.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# Set up Firefox options
firefox_options = Options()
firefox_options.headless = True

# Set up Firefox webdriver with the specified executable path
browser = webdriver.Firefox(
    executable_path=GECKO_PATH,
    options=firefox_options
)
browser.get("http://localhost:5000/signup")
try:
    # Find the input fields and signup button
    email_input = browser.find_element(By.ID, "email")
    username_input = browser.find_element(By.ID, "username")
    password_input = browser.find_element(By.ID, "password")
    signup_button = browser.find_element(By.ID, "signup-btn")

    print("Title: %s" % browser.title)

    # Attempt to create user
    email_input.send_keys("signup@example.com")
    username_input.send_keys("signupuser")
    password_input.send_keys("signuppassword")
    signup_button.click()

    # Redirect to login
    wait = WebDriverWait(browser, 2)
    login_form = wait.until(EC.presence_of_element_located((By.ID, "login-form")))

    # Go back to signup
    browser.get("http://localhost:5000/signup")

    # Find the input fields and signup button
    email_input = browser.find_element(By.ID, "email")
    username_input = browser.find_element(By.ID, "username")
    password_input = browser.find_element(By.ID, "password")
    signup_button = browser.find_element(By.ID, "signup-btn")

    # attempt to create same user
    email_input.send_keys("signup@example.com")
    username_input.send_keys("signupuser")
    password_input.send_keys("signuppassword")
    signup_button.click()

    # Ensure there is text in #email-error and #username-error
    email_error = browser.find_element(By.ID, "email-error")
    username_error = browser.find_element(By.ID, "username-error")
    assert email_error.text != "" and username_error.text != ""

    # Go back to signup
    browser.get("http://localhost:5000/login")
    browser.get("http://localhost:5000/signup")
    wait = WebDriverWait(browser, 2)

    # Attempt signup with a different signup email, username, and password.
    email_input = browser.find_element(By.ID, "email")
    username_input = browser.find_element(By.ID, "username")
    password_input = browser.find_element(By.ID, "password")
    signup_button = browser.find_element(By.ID, "signup-btn")

    email_input.send_keys("signup2@example.com")
    username_input.send_keys("signupuser2")
    password_input.send_keys("signuppassword2")
    signup_button.click()

    wait = WebDriverWait(browser, 2)
    # Should redirect to login
    login_form = wait.until(EC.presence_of_element_located((By.ID, "login-form")))

    # Test Passed
    if login_form:
        print("Button click redirected to login page successfully. SUCCESS DONE")
    else:
        print("Button click did not redirect to login page.")
        raise Exception("e")
finally:
    browser.quit()