# https://api.hh.ru/employers/{employer_id}
# https://api.hh.ru/vacancies?employer_id=5974128
#
# url = "https://api.hh.ru/vacancies"
#         all_pages = 5
#         page = 0
#         all_vacancies = []
#         while page < all_pages:
#             params = {
#                 "text": keyword,
#                 "page": page,
#                 "per_page": 100
#             }
#             response = requests.get(url, params=params)
#             if response.status_code == 200:
#                 vacancies = response.json()["items"]
#                 for vacancy in vacancies:
#                     if vacancy["salary"] is not None:
#                         salary_from = vacancy["salary"]["from"]
#                         if salary_from is None:
#                             salary_from = 0
#                         salary_to = vacancy["salary"]["to"]
#                         if salary_to is None:
#                             salary_to = 0
#                     else:
#                         salary_from = 0
#                         salary_to = 0
#                     all_vacancies.append({
#                         "name_vacancy": (vacancy["name"]).lower(),
#                         "url_vacancy": (vacancy["apply_alternate_url"]).lower(),
#                         "salary_from": (str(salary_from)).lower(),
#                         "salary_to": (str(salary_to)).lower(),
#                         "town": (vacancy["area"]["name"]).lower(),
#                     })
#             else:
#                 print("Error:", response.status_code)
#             page += 1
#         return all_vacancies
