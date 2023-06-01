from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import app, db
from app.models import Message
from secret.secret import GECKO_PATH

# USE IN-MEMORY DATABASE TO SAVE CLEANING UP FILES.
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

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
    email_input.send_keys("login@example.com")
    username_input.send_keys("loginuser")
    password_input.send_keys("loginpassword")
    signup_button.click()

    # Redirect to login
    wait = WebDriverWait(browser, 2)
    login_form = wait.until(EC.presence_of_element_located((By.ID, "login-form")))

    # Test Passed
    if login_form:
        print("Button click redirected to login page successfully.")
    else:
        print("Button click did not redirect to login page.")
        raise Exception("failed login redirect")
    # Find the input fields and login button
    email_input = browser.find_element(By.ID, "email")
    password_input = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.ID, "login-btn")
    
    email_input.send_keys("login@example.com")
    password_input.send_keys("wrongpass")
    login_button.click()

    wait = WebDriverWait(browser, 2)
    login_form = wait.until(EC.presence_of_element_located((By.ID, "login-form")))

    if login_form:
        print("Login with wrong password failed successfully.")
    else:
        print("Login with wrong password failed.")
        raise Exception("failed index redirect")

    browser.get("http://localhost:5000/login")
    email_input = browser.find_element(By.ID, "email")
    password_input = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.ID, "login-btn")
    
    email_input.send_keys("login@example.com")
    password_input.send_keys("loginpassword")
    login_button.click()
    # Redirect to index
    wait = WebDriverWait(browser, 2)
    history_form = wait.until(EC.presence_of_element_located((By.ID, "history")))

    # Test Passed
    if history_form:
        print("Button click redirected to index page successfully.")
    else:
        print("Button click did not redirect to index page.")
        raise Exception("failed index redirect")




finally:
    browser.quit()