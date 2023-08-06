from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import psycopg2


firefox_driver_path = "C:/Users/maxil/Desktop/gecodriver"

firefox_service = FirefoxService(executable_path=firefox_driver_path)

firefox_options = FirefoxOptions()

driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

url = "https://жд-билеты.сайт/kupit-zhd-bilety/#/novosibirsk/krasnoyarsk"

driver.get(url)

driver.implicitly_wait(10)

train_elements = driver.find_elements(By.CSS_SELECTOR, ".wg-train-container")

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="practic",
    user="postgres",
    password="12345"
)

# Создание курсора
cur = conn.cursor()


# Пример данных для вставки
data = []

# Извлечение данных
for train_element in train_elements:
    train_number = train_element.find_element(By.CSS_SELECTOR, ".wg-train-info__number-link").text
    dates = train_element.find_elements(By.CSS_SELECTOR, ".wg-track-info__date")
    departure_date = dates[0].text
    arrival_date = dates[1].text
    travel_time = train_element.find_element(By.CSS_SELECTOR, ".wg-track-info__duration-time").text

    data.append((train_number, departure_date, travel_time, arrival_date))

# SQL-запрос для вставки данных в таблицу
insert_query = "INSERT INTO trains (train_number, departure_date, travel_time, arrival_date) VALUES (%s, %s, %s, %s)"

# Передача данных в таблицу
cur.executemany(insert_query, data)

# Фиксация изменений
conn.commit()

# Закрытие курсора и соединения
cur.close()
conn.close()

driver.quit()