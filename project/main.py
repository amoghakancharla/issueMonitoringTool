import requests

api_end_points = [
    'https://api.github.com/repos/microsoft/vscode/issues']

auth_token = "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"

headers = {'Authorization': f'Token {auth_token}'}

params = {'page': 1, 'limit': 10}


def check_for_label(issue):  # Check one issue for good-first-issue label return type is bool
    if len(issue['labels']) > 0:
        for label in issue['labels']:
            if label['name'] == "good first issue":
                return True
        return False
    else:
        return False


def get_number_of_pages(url):  # Returns int number of total pages from an endpoint
    response = requests.get(url, headers=headers)
    link_header = response.headers.get("Link")

    if link_header:
        links = link_header.split(", ")
        last_link = links[-1]
        last_page_url = last_link.split("; ")[0][1:-1]
        last_page_number = int(last_page_url.split("page=")[-1])
        return last_page_number
    else:
        return 1


def get_query(urls):  # Void func. prints out number of found issue if some exist prints out the link and description.
    good_first_issue_number = 0
    for url in urls:
        real_url = 'https://www.github.com/' + url[28::]
        max_page = get_number_of_pages(url)
        for page in range(1, max_page):
            print(f"Найдено {good_first_issue_number} свободных проблем на странице {page - 1}")
            good_first_issue_number = 0
            response = requests.get(url + f'?page={page}&q=is%3Aissue+is%3Aopen', headers=headers)
            if response.status_code == 200:
                parsed_list = response.json()
                for issue in parsed_list:
                    if issue['assignee'] is None:
                        if check_for_label(issue):
                            good_first_issue_number += 1
                            print(f"""Описание: {issue['title']}, Ссылка {real_url + f"/{issue['number']}"}""")
                        else:
                            continue
            else:
                print("GET QUERY ERROR")
                break


get_query(api_end_points)
