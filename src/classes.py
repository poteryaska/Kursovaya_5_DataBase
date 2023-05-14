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
        '''Создание таблиц companies и vacancies в созданной базе данных'''
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
                    INSERT INTO vacancies (id_vacancy, id_company, name_vacancy, url_vacancy, salary_from, salary_to)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy)
                )
        conn.commit()
        conn.close()


    def get_companies_and_vacancies_count(self):
        '''получает список всех компаний и количество вакансий у каждой компании'''
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        with conn.cursor() as cur:
            cur.execute("SELECT name_company, COUNT(*) "
                        "FROM companies "
                        "JOIN vacancies USING(id_company) "
                        "GROUP BY name_company "
                        "ORDER BY name_company")
            conn.commit()
            companies = cur.fetchall()
            for company in companies:
                print(company)
        conn.close()


    def get_all_vacancies(self):
        '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию'''
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        with conn.cursor() as cur:
            cur.execute("SELECT name_company, name_vacancy, "
                        "salary_from, salary_to, url_vacancy "
                        "FROM vacancies "
                        "LEFT JOIN companies using(id_company) "
                        "ORDER BY name_company")
            conn.commit()
            vacancies = cur.fetchall()
            for vacancy in vacancies:
                print(vacancy)
        conn.close()

    def get_avg_salary(self):
        '''получает среднюю зарплату по вакансиям'''
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        with conn.cursor() as cur:
            cur.execute("SELECT ROUND (AVG(salary_from)) "
                        "FROM vacancies ")
            conn.commit()
            avg_salary = cur.fetchall()
            print(avg_salary)
        conn.close()

    def get_vacancies_with_higher_salary(self):
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям'''
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vacancies "
                        "WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies) "
                        "ORDER BY salary_from DESC")
            conn.commit()
            vacancies = cur.fetchall()
            for vacancy in vacancies:
                print(vacancy)
        conn.close()

    def get_vacancies_with_keyword(self, keyword):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”'''
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM vacancies 
                        WHERE name_vacancy LIKE '%{keyword}%'
                        """)
            conn.commit()
            vacancies = cur.fetchall()
            for vacancy in vacancies:
                print(vacancy)
        conn.close()


params = config()
HH = DBManager('hh', params)
# HH.create_database()
# HH.create_tables()
# companies = get_companies('мегафон, мтс')
# ids_companies = []
# for id in companies:
#     ids_companies.append(id[0])
# vacancies = get_vacancies_companies(ids_companies)
# HH.save_data_to_database(companies, vacancies)
HH.get_vacancies_with_keyword('менедж')


