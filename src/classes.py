import psycopg2
from config import config
from utils import get_companies, get_vacancies_companies


class DBManager:
    def __init__(self, db_name: str, params: dict):
        self.__db_name = db_name
        self.__params = params

    def create_database(self):
        '''Создание базы данных для хранения данных, полученных из HH'''
        conn = psycopg2.connect(dbname='postgres', **self.__params)
        conn.autocommit = True
        cur = conn.cursor()

        # cur.execute(f"DROP DATABASE {self.__db_name}")
        cur.execute(f"CREATE DATABASE {self.__db_name}")
        cur.close()
        conn.close()

    def create_tables(self):
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE companies (
                    id_company SERIAL PRIMARY KEY,
                    name_company VARCHAR(100) NOT NULL
                )
            """)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    id_vacancy SERIAL PRIMARY KEY,
                    id_company SERIAL REFERENCES companies (id_company) ON DELETE CASCADE,
                    name_vacancy VARCHAR(100) NOT NULL,
                    url_vacancy VARCHAR(300) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER
                )
            """)
        conn.commit()
        conn.close()

    def save_data_to_database(self, companies, vacancies):
        '''Сохраниение данных о полученных компаниях и вакансиях'''
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            for company in companies:
                cur.execute(
                    """
                    INSERT INTO companies (id_company, name_company)
                    VALUES (%s, %s)
                    """,
                    (company)
                )

        with conn.cursor() as cur:
            for vacancy in vacancies:
                cur.execute(
                    """
                    INSERT INTO vacancies (id_company, id_company, name_vacancy, url_vacancy, salary_from, salary_to)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy)
                )
        conn.commit()
        conn.close()


params = config()
HH = DBManager('hh', params)
# HH.create_database()
# HH.create_tables()
imp = get_companies('Woori, Мегафон')
all_imp = []
for i in imp:
    all_imp.append(i[0])
vac = get_vacancies_companies(all_imp)
HH.save_data_to_database(imp, vac)

#
#
#     def get_companies_and_vacancies_count(self, company_name):
#         '''получает список всех компаний и количество вакансий у каждой компании'''
#         pass
#
#     def get_all_vacancies(self):
#         '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию'''
#         pass
#
#     def get_avg_salary(self):
#         '''получает среднюю зарплату по вакансиям'''
#         pass
#
#     def get_vacancies_with_higher_salary(self):
#         '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям'''
#         pass
#
#     def get_vacancies_with_keyword(self):
#         '''получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”'''
#
#
#


