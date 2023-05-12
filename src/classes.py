import psycopg2
import requests

class DBManager:
    def __init__(self):
        pass

    def get_companies_and_vacancies_count(self, company_name):
        '''получает список всех компаний и количество вакансий у каждой компании'''

        url = 'https://api.hh.ru/employers'
        id_companies = []

        params = {
            "text": company_name,
            "only_with_vacancies": 'true',
            "page": 0
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            companies = response.json()["items"]
            for company in companies:
                id_companies.append({company["id"]: company["open_vacancies"]})
        return id_companies



    def get_all_vacancies(self):
        '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию'''
        pass

    def get_avg_salary(self):
        '''получает среднюю зарплату по вакансиям'''
        pass

    def get_vacancies_with_higher_salary(self):
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям'''
        pass

    def get_vacancies_with_keyword(self):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”'''