import requests
import csv
from time import sleep

field_names = ['URL', 'Price', 'Model', 'Mileage']

def clear_database():

    with open('data.csv', mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(field_names)

def cars_on_page(page, params):
    url = f'https://finder.porsche.com/api/ca/en-CA/search?page={page}'
    for key in params:
        if params[key] == '' or params[key] == None:
            continue
        else:
            url += f'&{key}={params[key]}'
    
    r = requests.get(url)

    if r.json()['pages']['activePage'] == 0:
        return []

    cars = []

    for car in r.json()['results']:
        record = []
        record.append(car['listingUrlSlug'])
        record.append(car['meta']['priceValue'])
        record.append(car['meta']['model'])
        record.append(car['meta']['mileage'])
        cars.append(record)

    return cars

def scan():
    page = 1
    while True:
        params = {
            'condition': 'classic'
            # There are a million and one parameters. For simplicity we focus on a small subset
        }
        results = cars_on_page(page=page, params=params)
        if results == []:
            break
        print(f'Scanning page {page}')
        with open('data.csv', mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(results)
        sleep(2.5)
        page += 1