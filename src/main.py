from config import config
from classes import DBManager
from utils import get_companies, get_vacancies_companies


def main():
    params = config()
    HH = DBManager('hh', params)
    # HH.create_database()
    HH.create_tables()
    companies = get_companies('мегафон, мтс')
    ids_companies = []
    for id in companies:
        ids_companies.append(id[0])
    vacancies = get_vacancies_companies(ids_companies)
    HH.save_data_to_database(companies, vacancies)


if __name__ == '__main__':
    main()
