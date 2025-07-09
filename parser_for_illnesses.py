from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import json
from selenium.common.exceptions import TimeoutException


def setup_driver():
    options = webdriver.ChromeOptions()
    
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # options.add_argument("--disable-backgrounding-occluded-windows")
    # options.add_argument("--disable-renderer-backgrounding")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--dns-prefetch-disable")
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=options)
    # driver.set_page_load_timeout(60)  # Установите таймаут 60 сек
    # driver.implicitly_wait(5)  # Глобальный таймаут элементов
    return driver


def get_symptoms(data):
    result = []
    symptoms = data.find_all('li')
    for val in symptoms:
        result.append(val.text.strip())
    return result


def get_doctors(data):
    result = []
    specs = data.find_all('li')
    for val in specs:
        result.append(val.text.strip())
    return result


def safe_get(driver, url, retries=3, timeout=30):
    for attempt in range(retries):
        try:
            driver.set_page_load_timeout(timeout)
            driver.get(url)
            return True
        except TimeoutException:
            print(f"Attempt {attempt+1} failed. Retrying...")
    return False


def parse_illness(driver, link, name):
    # time.sleep(2)
    answer = {
        'name': name,
        'symptoms': [],
        'doctors': []
    }
    current_url = driver.current_url
    full_url = urljoin(current_url, link)
    if not safe_get(driver, full_url):
        print("Не удалось загрузить страницу")
        return None, True
    # driver.get(full_url)
    if "Симптом" not in driver.page_source:
        return None, True
    if "Какие врачи лечат" not in driver.page_source:
        return None, True
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    sections = soup.find_all('section', {'data-test-id': 'bottom_content'})
    flag_symps = True
    flag_doctors = True
    for item in sections[::-1]:
        if flag_symps and ("Симптом" in str(item)):
            flag_symps = False
            symptoms = get_symptoms(item)
            answer['symptoms'] = symptoms
        elif flag_doctors and "Какие врачи лечат" in str(item):
            flag_doctors = False
            doctors = get_doctors(item)
            answer['doctors'] = doctors
    return answer, None


def write_to_file(data):
    filename = "illnesses.json"
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в файл {filename}")
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")


def click_date_tab_and_parse(driver):
    diseases = {
        'illnesses': []
        }
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    illnesses = soup.find_all('ul', class_='library__letter-list js-library-letter')
    all_counter = 0
    for i in illnesses:
        items = i.find_all('a')
        # print(len(items))
        counter = 0
        for j in items:
            all_counter += 1
            counter += 1
            print(all_counter, counter)
            name = j.text.strip()
            link = j.get('href')
            new_illness, lack = parse_illness(driver, link, name)
            if lack:
                continue
            diseases['illnesses'].append(new_illness)
            if counter > 50:
                break
    write_to_file(diseases)
    return 



def main():
    driver = setup_driver()
    try:
        if not safe_get(driver, "https://docdoc.ru/doctor/illness"):
            print("Не удалось загрузить страницу")
        time.sleep(3)
        click_date_tab_and_parse(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
