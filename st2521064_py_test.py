import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Fixture: launches Chrome before each test and closes it after execution
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/index.html")
    yield driver
    driver.quit()


# Helper function for logging into the system with valid credentials
def login(driver):
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    username.send_keys("admin")
    password.send_keys("@Dm1n")

    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    time.sleep(1)


# Positive test: verify successful login
# Expected result: user is logged in and main application (#app) is displayed
def test_login(driver):
    login(driver)

    time.sleep(1)

    app = driver.find_element(By.ID, "app")
    assert app.is_displayed()


# Negative test: login with incorrect password
# Expected result: login fails and main application is not displayed
def test_login_invalid_password(driver):
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")

    username.send_keys("admin")
    password.send_keys("wrong_password")

    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    time.sleep(1)

    app = driver.find_elements(By.ID, "app")

    assert len(app) == 0 or not app[0].is_displayed()


# Negative test: login with empty fields
# Expected result: login fails and main application is not displayed
def test_login_empty_fields(driver):
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    time.sleep(1)

    username = driver.find_element(By.ID, "username")
    assert username.is_displayed()


# Test navigation between tabs (Cameras, Lenses, Contact)
# Expected result: only the selected tab content is visible at a time
def test_navigation_tabs(driver):
    wait = WebDriverWait(driver, 10)

    login(driver)
    wait.until(EC.visibility_of_element_located((By.ID, "app")))

    cameras_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Cameras']")))
    lenses_btn = driver.find_element(By.XPATH, "//button[text()='Lenses']")
    contact_btn = driver.find_element(By.XPATH, "//button[text()='Contact']")

    cameras_section = driver.find_element(By.ID, "cameras")
    lenses_section = driver.find_element(By.ID, "lenses")
    contact_section = driver.find_element(By.ID, "contact")

    # Cameras tab
    cameras_btn.click()
    assert "hidden" not in cameras_section.get_attribute("class")
    assert "hidden" in lenses_section.get_attribute("class")
    assert "hidden" in contact_section.get_attribute("class")

    time.sleep(1)

    # Lenses tab
    lenses_btn.click()
    assert "hidden" in cameras_section.get_attribute("class")
    assert "hidden" not in lenses_section.get_attribute("class")
    assert "hidden" in contact_section.get_attribute("class")

    time.sleep(1)

    # Contact tab
    contact_btn.click()
    assert "hidden" in cameras_section.get_attribute("class")
    assert "hidden" in lenses_section.get_attribute("class")
    assert "hidden" not in contact_section.get_attribute("class")

    time.sleep(1)


# Test filling the Contact form
# Expected result: input fields accept and store the entered values correctly
def test_contact_form(driver):
    login(driver)

    time.sleep(1)
    driver.find_element(By.XPATH, "//button[text()='Contact']").click()

    name = driver.find_element(By.ID, "name")
    email = driver.find_element(By.ID, "email")
    phone = driver.find_element(By.ID, "phone")
    message = driver.find_element(By.ID, "message")

    name.send_keys("Test User")
    email.send_keys("test@mail.com")
    phone.send_keys("0987654321")
    message.send_keys("123456")

    time.sleep(2)

    assert name.get_attribute("value") == "Test User"
    assert email.get_attribute("value") == "test@mail.com"
    assert phone.get_attribute("value") == "0987654321"
    assert message.get_attribute("value") == "123456"


# Test Send Message button functionality
# Expected result: success message is displayed after submitting the form
def test_send_message_button(driver):
    login(driver)

    driver.find_element(By.XPATH, "//button[text()='Contact']").click()

    name = driver.find_element(By.ID, "name")
    email = driver.find_element(By.ID, "email")
    phone = driver.find_element(By.ID, "phone")
    message = driver.find_element(By.ID, "message")

    name.send_keys("Test User")
    email.send_keys("test@mail.com")
    phone.send_keys("0987654321")
    message.send_keys("123456")

    send_btn = driver.find_element(By.XPATH, "//button[text()='Send Message']")
    send_btn.click()

    time.sleep(2)

    success_message = driver.find_element(By.ID, "formSuccess")

    assert success_message.is_displayed()
    assert success_message.text == "Message sent successfully!"


# Test Logout functionality
# Expected result: user is logged out and login form is displayed again
def test_logout(driver):
    login(driver)

    time.sleep(2)

    logout = driver.find_element(By.CLASS_NAME, "logout")
    logout.click()

    time.sleep(2)

    username = driver.find_element(By.ID, "username")
    assert username.is_displayed()
