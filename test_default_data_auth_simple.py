import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


target = "http://testfire.net/index.jsp"
next = "http://testfire.net/login.jsp"


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.mark.parametrize("login, password",
                         [
                             ("root", "root"),
                             ("root", "password"),
                             ("admin", "admin"),
                             ("admin", "password"),
                             ("test", "test"),
                             ("system", "system")
                         ])
def test_sql_injection_simple(driver, login, password):
    driver.get(target)
    assert driver.current_url == target, "Главная страница не открылась"
    print("Главная страница открыта")
    driver.implicitly_wait(2)
    driver.find_element(By.ID, "LoginLink").click()
    assert driver.current_url == next, "Переход не осуществлен"
    print("Переход осуществлен успешно")
    driver.implicitly_wait(2)

    driver.find_element(By.ID, "uid").send_keys(login)
    driver.find_element(By.ID, "passw").send_keys(password)
    driver.find_element(By.NAME, "btnSubmit").click()

    assert driver.current_url == next, f"Для данных учетной записи с данными по умолчанию {
        login}/{password} аутентификация прошла успешно"
    print(
        f"Данные по умолчанию не используются. Аутентификация не произошла.")
