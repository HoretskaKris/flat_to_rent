from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Налаштовуємо драйвер
options = webdriver.ChromeOptions()
options.add_argument("--headless") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
except Exception as e:
    print(f"Помилка запуску браузера: {e}")
    exit()

# URL пошуку квартир у Вроцлаві
base_url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/"
try:
    driver.get(base_url)
    time.sleep(3)  # Чекаємо завантаження сторінки
except Exception as e:
    print(f"Помилка при відкритті сайту: {e}")
    driver.quit()
    exit()

data = []
page = 1

while True:
    print(f"Збираю дані зі сторінки {page}...")

    # Збираємо всі оголошення
    try:
        apartments = driver.find_elements(By.CLASS_NAME, "css-qfzx1y")
    except Exception as e:
        print(f"Помилка при пошуку оголошень: {e}")
        break

    if not apartments:
        print("Оголошень більше немає. Завершую роботу.")
        break

    for apartment in apartments:
        try:
            title = apartment.find_element(By.CLASS_NAME, "css-1g61gc2").text
        except:
            title = "Немає назви"

        try:
            price = apartment.find_element(By.CLASS_NAME, "css-6j1qjp").text
        except:
            price = "Немає ціни"

        try:
            link = apartment.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            link = "Немає посилання"

        data.append({"title": title, "price": price, "link": link})

    # Переходимо на наступну сторінку
    try:
        next_button = driver.find_element(By.XPATH, "//a[@data-testid='pagination-forward']")
        next_button.click()
        time.sleep(3)  # Дати сторінці завантажитися
        page += 1
    except:
        print("Кінець сторінок або не знайдено кнопку 'Далі'.")
        break

driver.quit()

# Збереження у CSV
df = pd.DataFrame(data)
try:
    df.to_csv("flats_wroclaw.csv", index=False, encoding="utf-8")
    print("Дані збережено у 'flats_wroclaw.csv'")
except Exception as e:
    print(f"Помилка збереження у CSV: {e}")

# Виводимо перші 5 результатів
for d in data[:5]:
    print(d)
