from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import app, db
from secret.secret import GECKO_PATH
import time
# from app.models import Message

# # USE IN-MEMORY DATABASE TO SAVE CLEANING UP FILES.
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# Set Firefox options
options = Options()
options.headless = False  # fails if set to true.

# Create a new instance of the Firefox driver
browser = webdriver.Firefox(executable_path=GECKO_PATH, options=options)

# Open the web application
browser.get("http://localhost:5000/signup")

try:
    email_input = browser.find_element(By.ID, "email")
    username_input = browser.find_element(By.ID, "username")
    password_input = browser.find_element(By.ID, "password")
    signup_button = browser.find_element(By.ID, "signup-btn")

    print("Title: %s" % browser.title)

    email_input.send_keys("index@example.com")
    username_input.send_keys("indexuser")
    password_input.send_keys("indexpassword")
    signup_button.click()

    wait = WebDriverWait(browser, 2)
    login_form = wait.until(EC.presence_of_element_located((By.ID, "login-form")))

    if login_form:
        print("Button click redirected to login page successfully.")
    else:
        print("Button click did not redirect to login page.")
        raise Exception("failed login redirect")

    # Open the web application
    browser.get("http://localhost:5000/login")

    email_input = browser.find_element(By.ID, "email")
    password_input = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.ID, "login-btn")

    print("Title: %s" % browser.title)

    email_input.send_keys("index@example.com")
    password_input.send_keys("indexpassword")
    login_button.click()

    time.sleep(2)
    history = wait.until(EC.presence_of_element_located((By.ID, "history")))

    if history:
        print("Button click redirected to index page successfully.")
    else:
        print("Button click did not redirect to index page.")
        pass

    # Test create channel.
    channel_name = "Channel 1"
    new_channel_button = browser.find_element(By.ID, "new_channel")
    new_channel_button.click()
    channel_name_input = browser.find_element(By.ID, "channel_name")
    channel_name_input.send_keys(channel_name)
    submit_channel_button = browser.find_element(By.ID, "submit_channel")
    submit_channel_button.click()
    browser.find_element(By.ID, "submit_channel")
    # Test create second channel
    channel_name = "Channel 2"
    channel_name_input = browser.find_element(By.ID, "submit_channel")
    channel_name_input.send_keys(channel_name)

    submit_channel_button = browser.find_element(By.ID, "submit_channel")
    submit_channel_button.click()

    time.sleep(1)
    submit_channel_button = browser.find_element(By.ID, "closeChannelPopUp")
    submit_channel_button.click()

    # Test changing to every channel created
    channel_buttons = browser.find_elements(By.CLASS_NAME, "channel_button")
    for channel_button in channel_buttons:
        channel_name = channel_button.get_attribute("data-channel-name")
        channel_button.click()

        # ensure change is successful by making sure header changes everytime
        # this is a change that is started by the server,
        # by telling the client that they joined the server
        # successfully.
        channel_header = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "channel_header"))
        )
        assert channel_name in channel_header.text

    time.sleep(1)

    # Test sending messages

    message_input = browser.find_element(By.ID, "tx_data_field")
    send_message_button = browser.find_element(By.ID, "send_message")

    time.sleep(5)
    message = "Hello, World!"
    message_input.send_keys(message)
    send_message_button.click()

    message_input.clear()

    message2 = "testmessage#2"
    message_input.send_keys(message2)
    send_message_button.click()

    # assert that message has been sent
    history = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "history"))
    )
    assert message in history.text
    assert message2 in history.text
    

    # Test reloading page
    browser.refresh()
    time.sleep(2)

    # wait for init anitmations and such.

    # Check the current channel and message
    channel_header = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "channel_header"))
    )
    assert channel_name in channel_header.text

    # make sure that messages are in the db -- that they stick around after a reload
    history = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "history"))
    )
    assert message in history.text
    assert message2 in history.text

    #ensure messages show up in search
    browser.find_element(By.ID, "searchBtn").click()
    # input part of Hello, World! into search query
    browser.find_element(By.ID, "search-query").send_keys(message[2:7])

    # wait for server to search and return
    time.sleep(2)
    assert message in browser.find_element(By.ID, "search_results").text
    browser.find_element(By.ID, "close-search-popup").click()


    # Test leaving channel -- should remove message history.
    leave_channel_button = browser.find_element(By.ID, "leave_channel")
    leave_channel_button.click()

    channel_name_attribute = leave_channel_button.get_attribute("data-channel-name")
    assert channel_name_attribute is None
    channel_header = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "channel_header"))
    )
    # assert leaving channel was successful
    assert "Join a channel to start talking!" in channel_header.text
    
    print("Index working perfectly. Search, send, make channel, database fetching and more.")
finally:
    # Close the browser
    browser.quit()
