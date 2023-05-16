from config import config
from classes import DBManager
from utils import get_companies, get_vacancies_companies


def main():
    params = config()
    HH = DBManager('hh', params)
    HH.create_database()
    HH.create_tables()
    user_request = input('Введите через запятую наименования компаний, по которым нужно получить вакансии\n')
    companies = get_companies(user_request)
    ids_companies = []
    for id in companies:
        ids_companies.append(id[0])
    vacancies = get_vacancies_companies(ids_companies)
    HH.save_data_to_database(companies, vacancies)
    while True:
        request = input(f'Какие данные вывести, введите цифру:\n'
                        f'1 - список компаний и количество вакансий у каждой компании\n'
                        f'2 - список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию\n'
                        f'3 - среднюю зарплату по вакансиям\n'
                        f'4 - список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
                        f'5 - список всех вакансий, в названии которых содержатся слово, которое вы укажете\n'
                        f'6 - этого достаточно, завершить сессию\n')
        if request.strip() == '1':
            HH.get_companies_and_vacancies_count()
        elif request.strip() == '2':
            HH.get_all_vacancies()
        elif request.strip() == '3':
            HH.get_avg_salary()
        elif request.strip() == '4':
            HH.get_vacancies_with_higher_salary()
        elif request.strip() == '5':
            keyword = input('Введите ключевое слово для поиска\n')
            HH.get_vacancies_with_keyword(keyword)
        elif request.strip() == '6':
            break
        else:
            print('Введите только цифру от 1 до 6')


if __name__ == '__main__':
    main()
