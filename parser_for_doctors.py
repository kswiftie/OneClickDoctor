import requests
from bs4 import BeautifulSoup
import json
import time


BASE_URL = "https://prodoctorov.ru/spb/"

HEADERS = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'ru,en;q=0.9',
  'content-type': 'application/x-www-form-urlencoded',
  'priority': 'u=1, i',
  'referer': 'https://spb.docdoc.ru/clinic/mart',
  'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "YaBrowser";v="25.4", "Yowser";v="2.5"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'sentry-trace': '2d6cd29830ed424ca56712ec21d48afb-b04d5ece5dbac748-1',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 YaBrowser/25.4.0.0 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest',
  'Cookie': 'spid=1751635587049_ad57d09b22caad1592b951ca2e5b3a67_ah7wd9r2iabi1ajv; front_selected_city=%7B%22slug%22%3A%22spb%22%2C%22name%22%3A%22%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%22%7D; pid=33230; partner_traffic_source=cpc; origin_partner=33230; traffic_source_first_page=spb.docdoc.ru; _ym_uid=1751635592259139690; _ym_d=1751635592; advcake_track_id=0d2d58ed-2963-6d11-4250-1f15995b9bc8; advcake_session_id=a43b83f6-8873-7f03-e6e2-546175f8cfd4; advcake_utm_partner=zapis_spb_p33230_vrach_Pure_brand_search_yandex_d0224_107882795; advcake_utm_webmaster=ch_yandex_direct%7Ccid_107882795%7Cgid_5409222056%7Cad_15883733497%7Cph_50732460386%7Ccrt_0%7Cpst_premium%7Cps_2%7Csrct_search%7Csrc_none%7Cdevt_desktop%7Cret_50732460386%7Cgeo_2%7Ccf_0%7Cint_%7Ctgt_50732460386%7Cadd_no; advcake_click_id=; rand=80; iap.uid=4229951254b943588e158fc9f2ac2d44; _ct=300000001920858359; _ct_client_global_id=0fdef6d8-3274-5a66-b6ee-92a02acc798f; geo_alert_opened=1; deviceId=2593a50a-c223-4565-8510-8c8bbeba504c; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=359387ee-1f59-4468-ac18-5cef3a97a751; c_detCity=spb; _ym_isad=2; bucketssr=22; c_user_agent=Mozilla%2F5.0%20%28X11%3B%20Linux%20x86_64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F134.0.0.0%20YaBrowser%2F25.4.0.0%20Safari%2F537.36; PHPSESSID=nkr401kqso51qfp2f11hsel4n5; ddcsrftoken=N2ZhazcwY1FTOTRRTG5KRHkwZG9Nazc0QzhWODF3fjIfFaeHCEyHZneBmQyFsOpDn146J1IO2zgdO3nRNbw1uw%3D%3D; _sp_ses.f2e9=*; cted=modId%3D1d5124ef%3Bya_client_id%3D1751635592259139690; _ct_ids=1d5124ef%3A9628%3A3680761782; _ct_session_id=3680761782; _ct_site_id=9628; spsc=1751905321255_a059728085ce0cc41f0c270395c16423_dQQtwDz3Kg6Y2xjcOfDCvyn0gxrJsPbn0Jtxs6CB6JrQ4PxVQ4TUsaaDh45EM0WNZ; search_by_submit_fix=1; _ym_visorc=w; advcake_track_url=%3D20250113PB7oxnUSph87wRVjx8ha0nJO2WYE1nwuvPpiX%2BmYnoprVPZzSGx3G%2B4jOorqwU8nltsq35JrrsQKovJ4o7Bs%2BV543W7KzWFzw593pSsmfaxjd1oIOXgX00sXZAxzm83e3OtCOrjGF7I6TJLtFpPkUfUFKyPevvAd5xpOSq6ENa2QvSQr3MaztqQhMyolZSLxPLxSCN%2B83rpuSjLB3IltU8c%2FQOYuuQv%2FfayyRmOFubxsJjm0SRr3QAghqrix2zAru0Rm7q0ElnC7ltIT42lJXJ2P5fq%2F17HCwFiotcVn6X3UNM2n%2Buw8h8cxhvr3eo%2FWp2xcBSBk6RKlcVOPI77peTeSX8nfufTMjfjlAWqDg8E5HQJ8QsbQpxkveHv3DaS%2BAtzt8%2BIfrX20CxiWyuAE4GcajgKS9EAxQOz7BtMwWZUJ82k6Xa0E%2FJ895KeU5SfwTEkxpISQvltIbve%2Bp4HhsVnBblPvjEJs5bMQZBVR2Ft5m%2F3j3B0yVK%2BGLHV61DJD1wkRm3C9io%2Bz1Ja4z1HfU%2Fa2VQ8I3pTKzZgLlxOMOmEQf9bfk8hViwflXnB3Lsjf0Mp8gsoVbzNmCQj4xMY76a9QbeNdedhjFkC%2B%2B%2BhTtqcRUYaC1Q8fCAGjCIVVeQF1KKZXFOkbLuqcZXSnd5gho4eNaBIEKm%2FtL20Vs2x09gs7QN6ClHBfDdodSyetRulYtn0stph51zRjtLzBZwdEIlTZ%2FrA%2FtMJqlyTUAM7mqp4vrXPofpqiRCeK9V7MIB0ee%2FGxjN9%2BaEGiq%2BpzTBsrSJ7X%2FcUw4AcWgGvrrKeWhVlrKhHStHX%2BuD7HSDckN1FFI30DQuSWIuHc3U8MpEEt6rWRwY9KEwWd4le9wCJsQT71l6MFXZL0GLI7abTAb0ZQ5wKd4y3nJaVSQrJoOr302WqlSujDbnkSD3ZfM9Lzl1oRl0NM8IUgnaXWrpGNvQSuYqdXoPqM9zRSWM1bKGJ%2FK%2BJ69oJFIeEOP%2BeWt%2BxtPYi8hX83r1S8dEx53PnwxYvqBeKQgbdwmS%2Bj; call_s=___1d5124ef.1751909772.3680761782.375133:1056485|3___; _sp_id.f2e9=c74b6359-c957-489a-9aa1-6617ae18192f.1751635587.7.1751907975.1751907980.5a447555-bfd1-4531-aec2-ac7bd0dca0c1; csrftoken=f47Qw6vp7SyeLjkByHOiW5FdndzGVtE9; sessionid=v1pifal65lcoepbxe5s9uq1vmx50l4jy'
}


CLINICS = {
    'mart': "lpu/36375-mart/vrachi/#tab-content", 
    'pirogova': 'lpu/33132-klinika-pirogova/vrachi/#tab-content'
}


def get_reviews(url):
    time.sleep(3)
    vals_of_reviews = []
    response = requests.get(url, headers=HEADERS)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    reviews = soup.find_all('div', class_=lambda x: x and 'b-review-card' in x.split())
    for i in reviews:
        rating = i.find('span', 'ui-text ui-text_subtitle-2 ui-kit-color-text ml-1')
        comment = i.find_all('div', class_='b-review-card__comment ui-text ui-text_body-1 ui-kit-color-text mt-2')
        temp_vals = {}
        if rating:
            # print(rating.text)
            temp_vals['rating'] = rating.text
        for j in range(len(comment)):
            # print(comment[j].text.strip())
            if j == 0:
                temp_vals['comment'] = comment[j].text.strip()
            elif j == 1:
                temp_vals['like'] = comment[j].text.strip()
            else:
                temp_vals['dislike'] = comment[j].text.strip()
        vals_of_reviews.append(temp_vals)
    return vals_of_reviews


def write_to_file(name, data):
    filename = "doctors_{}.json".format(name)
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в файл {filename}")
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")


def get_doctors(filename, url):
    response = requests.get(BASE_URL + url, headers=HEADERS)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    doctors = soup.find_all('div', class_=lambda x: x and 'b-doctor-card' in x.split())
    doctors_dict = {'doctors': []}
    for i in doctors:
        name = i.find('span', class_='b-doctor-card__name-surname')
        name = name.text
        # print(name)
        specs = i.find('div', class_='b-doctor-card__spec')
        specs = specs.text
        # print(specs)
        url_main_page = i.find('a', class_='b-doctor-card__name-link')
        url_main_page = "https://prodoctorov.ru" + url_main_page.get('href')
        # print(url_main_page)
        url_reviews = url_main_page + "otzivi/#otzivi"
        # print(url_reviews)
        specs_number = i.get('data-spec').replace('[', '').replace(']', '').replace(',', '')
        specs_number = specs_number.split()
        # print(specs_number)
        doctor_id = i.get('data-doctor-id')
        # print(doctor_id)
        lpu_id = i.get('data-wp-block-id')
        # print(lpu_id)
        data_json = json.loads(i.get('data-schedule-item-lpu-doctors', '{}'))    
        doctors_lpu = data_json.get('doctorsLpu', {})
        has_slots = doctors_lpu.get('hasSlots', 'Unknown')
        is_appointment_on = doctors_lpu.get('isAppointmentOn', 'Unknown')
        # print(f"hasSlots: {has_slots}")
        # print(f"isAppointmentOn: {is_appointment_on}")
        has_appointment = True
        if (has_slots == 'False') or (is_appointment_on == 'False'):
            has_appointment = False
        # print(has_appointment)
        reviews = get_reviews(url_reviews)
        # print()
        doctors_dict['doctors'].append(
            {
                'name': name,
                'url_main_page': url_main_page,
                'id': doctor_id,
                'lpu': lpu_id,
                'specs': specs,
                'specs_number': specs_number,
                'appointment': has_appointment,
                'reviews': reviews
            }
        )
    write_to_file(filename, doctors_dict)


def main():
    for name_clinic in CLINICS:
        get_doctors(name_clinic, CLINICS[name_clinic])



if __name__ == '__main__':
    main()