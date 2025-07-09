from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # options.add_argument("--disable-backgrounding-occluded-windows")
    # options.add_argument("--disable-renderer-backgrounding")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--dns-prefetch-disable")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(5)
    return driver


def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes


def minutes_to_time(number):
    hours = number // 60
    minutes = number - hours * 60
    ans = '{}:{}'.format(hours, minutes)
    if minutes == 0:
        ans += '0'
    elif minutes < 10:
        ans = ans[:-1] + '0' + ans[-1]
    return ans


def get_time(driver, empty_slots, date_text):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    empty_time = soup.find_all('span', class_='ui-text ui-text_subtitle-1 ui-kit-color-bg-gray-0')
    empty_slots[date_text] = []
    for item in empty_time:
        empty_val = item.text.strip()
        cur_time = time_to_minutes(empty_val)
        empty_slots[date_text].append(cur_time)
    return


def click_date_tab_and_parse(driver, date_val, time_val, confirming, max_clicks=10):
    need_time = time_to_minutes(time_val)
    clicked_dates = set()
    empty_slots = dict()

    for _ in range(max_clicks):
        try:
            date_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 
                ".slider-group__item:not(.selectable-tab_disabled)"))
            )
            
            button_to_click = None
            for button in date_buttons:
                date_text = button.find_element(By.CSS_SELECTOR, '.ui-text_subtitle-1').text.split()[0]
                if date_text not in clicked_dates:
                    button_to_click = button
                    clicked_dates.add(date_text)
                    break
            if not button_to_click:
                print("Все доступные даты уже были обработаны")
                return 
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_to_click)
            time.sleep(2)
            button_to_click.click()
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 
                ".selectable-tab_active .ui-text_subtitle-1"))
            )
            time.sleep(2)
            
            print(f"Обработана дата: {date_text}")

            get_time(driver, empty_slots, date_text)

            if date_val == date_text:
                print("Нашли нужную дату")
                button_to_click = button
                break

        except Exception as e:
            print(f"Ошибка при обработке: {str(e)}")
            break
    answer = {
        'slots': []
        }
    for value in sorted(empty_slots, key=lambda x: abs(int(date_val) - int(x))):
        for item in sorted(empty_slots[value], key=lambda x: abs(need_time - x)):
            appointment_time = minutes_to_time(item)
            if confirming == '0':
                temp_val = {
                    'date': '',
                    'time': ''
                }
                temp_val['date'] = str(value)
                temp_val['time'] = appointment_time
                answer['slots'].append(temp_val)
                print(temp_val)
                if len(answer['slots']) > 4:
                    return answer
            else:
                answer = {
                    'url': ''
                }
                button = driver.find_element(By.XPATH, '//button[contains(@class, "slot-buttons__button") and contains(., "{}")]'.format(appointment_time))
                button.click()
                new_url = driver.current_url
                print("Новый URL:", new_url)
                answer['url'] = new_url
                return answer
    return None



def main():
    driver = setup_driver()
    try:
        # tesing data
        date_val = "10"
        date_val = date_val.strip()
        time_val = "12:30"
        time_val = time_val.strip()
        confirming = "0"
        doctor_url = "https://prodoctorov.ru/spb/vrach/259119-smirnov/"

        driver.get(doctor_url)
        time.sleep(3)
        
        get_slot = click_date_tab_and_parse(driver, date_val, time_val, confirming, max_clicks=15)
        if get_slot:
            pass
        else:
            print("Произошла ошибка, попробуйте еще раз")
            
    finally:
        driver.quit()


# def write_to_file(name, data):
#     filename = "doctors_{}.json".format(name)
#     try:
#         with open(filename, 'w', encoding='utf-8') as file:
#             json.dump(data, file, ensure_ascii=False, indent=4)
#         print(f"Данные успешно сохранены в файл {filename}")
#     except Exception as e:
#         print(f"Ошибка при создании файла: {e}")


if __name__ == '__main__':
    main()