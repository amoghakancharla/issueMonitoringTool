import requests


class IssueLurker:
    def __init__(self):
        self.auth_token = ''
        self.headers = {'Authorization': ''}
        self.api_end_points = list()

    def initialize_token(self, message):
        token = message
        self.auth_token = token
        self.headers['Authorization'] = f'token {token}'

    def validate_link(self, link):
        if 'https://github.com/' in link:
            return True
        else:
            return False

    def get_links_to_search(
            self, link):  # Пользователь может и ничего не ввести, так что список репозиториев может быть путсым
        link_to_cut = 'https://github.com/'
        if 'https://github.com/' in link:
            api_link = 'https://api.github.com/repos/' + link[len(link_to_cut)::] + '/issues'
            self.api_end_points.append(api_link)
            print(f'Ссылка {link} добавлена')
            return True
        else:
            print('Ссылка задана неправильно!')
            return False

    def get_number_of_pages(self, url):
        response = requests.get(url, headers=self.headers)
        link_header = response.headers.get("Link")

        if link_header:
            links = link_header.split(", ")
            last_link = links[-1]
            last_page_url = last_link.split("; ")[0][1:-1]
            last_page_number = int(last_page_url.split("page=")[-1])
            return last_page_number
        else:
            return 1

    def check_for_label(self, issue):
        if len(issue['labels']) > 0:
            for label in issue['labels']:
                if label['name'] == "good first issue":
                    return True
            return False
        else:
            return False

    def get_query(self):
        list_of_issues = []
        good_first_issue_number = 0
        for url in self.api_end_points:
            real_url = 'https://www.github.com' + url[28::]
            max_page = self.get_number_of_pages(url)
            for page in range(1, max_page):
                print(f"Найдено {good_first_issue_number} свободных проблем на {max_page} страницах")
                response = requests.get(url + f'?page={page}&q=is%3Aissue+is%3Aopen', headers=self.headers)
                if response.status_code == 200:
                    parsed_list = response.json()
                    for issue in parsed_list:
                        if self.check_for_label(issue) and issue['assignee'] is None:
                            good_first_issue_number += 1
                            list_of_issues.append(
                                f"""Описание: {issue['title']}, Ссылка {real_url + f"{issue['number']}"}""")
                        else:
                            continue
                else:
                    print("GET QUERY ERROR")
                    return list_of_issues.append("Ошибка")
        return list_of_issues
