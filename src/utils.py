import requests


def get_companies(companies_name: str) -> list:
    '''Получаем список ID на сайте hh.ru компании по API'''
    companies_list = companies_name.split(',')
    all_companies = []
    for company in companies_list:
        url = 'https://api.hh.ru/employers'
        params = {
            "text": company,
            "only_with_vacancies": 'true',
            "page": 0
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            companies = response.json()["items"]
            for company in companies:
                one_company = (company['id'], company['name'])
                all_companies.append(one_company)
        else:
            print("Error:", response.status_code)

    return all_companies


def get_vacancies_companies(id_companies: list):
    '''Получаем список ID компании на сайте hh.ru по API'''
    url = "https://api.hh.ru/vacancies"
    all_vacancies = []
    params = {
        "employer_id": id_companies,
        "per_page": 100
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        vacancies = response.json()["items"]
        for vacancy in vacancies:
            if vacancy["salary"] is not None:
                salary_from = vacancy["salary"]["from"]
                if salary_from is None:
                    salary_from = 0
                salary_to = vacancy["salary"]["to"]
                if salary_to is None:
                    salary_to = 0
            else:
                salary_from = 0
                salary_to = 0
            one_vacancy = (
                vacancy['id'],
                vacancy['employer']['id'],
                vacancy['name'],
                vacancy['alternate_url'],
                salary_from,
                salary_to
            )
            all_vacancies.append(one_vacancy)
    else:
        print("Error:", response.status_code)

    return all_vacancies
