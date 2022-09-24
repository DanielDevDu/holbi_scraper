#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
from sys import argv
from os import getenv
import logging

# logging.basicConfig(filename='./make_readme.log',
#                     format='%(asctime)s %(message)s', level=logging.WARNING)


def make_readme(URL_PAGE, option):
    URL = "https://intranet.hbtn.io/auth/sign_in"

    with requests.session() as session:

        """
        ------------------------------------------
        GET request to the main page of Holberton
                        Login page
        ------------------------------------------
        """
        try:
            response = session.get(URL)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            print("Error: GET request to the sing_in page:\n", err)
            logging.warning(err)
            return False

        """
        -----------------------------------------
        Parse with beautiful soup to obtain token
        -----------------------------------------
        """
        soup = BeautifulSoup(response.text, "html.parser")
        inputs = soup.find_all("input")
        for input in inputs:
            if input["name"] == "authenticity_token":
                token = input["value"]

        try:
            """
            ----------------------------------
            Params and POST request to login
            ----------------------------------
            """
            password = getenv("HOLBERTON_PASSWD")
            email = getenv("HOLBERTON_EMAIL")
            params = {
                "user[password]": password,
                "user[login]": email,
                "authenticity_token": token,
                "commit": "submit"}
            login = session.post(URL, data=params)
            login.raise_for_status()

            if login.status_code == 200:
                print("Login successful")

        except requests.exceptions.RequestException as err:
            print("Error: POST request to login:\n", err)
            logging.warning(err)
            return False

        """
        -----------------------------------------
        Special case for especializations
        We must choose the specialization in the
        main page
        -----------------------------------------
        """
        try:
            login_page = BeautifulSoup(login.text, "html.parser")

            curriculum = login_page.find("div", id="student-switch-curriculum")
            programs = curriculum.find_all("a")
            curriculum_names = curriculum.find_all(
                "span", class_="fs-4 fw-500")
            programs_urls = [{"name": "{}".format(name.get_text()), "url": 'https://intranet.hbtn.io/{}'.format(
                program["href"])} for program, name in zip(programs, curriculum_names)]

            # all programs of the current user. For example: Fundations and Machine Learning.
            # programs_urls = [
            #     'https://intranet.hbtn.io/{}'.format(program["href"]) for program in programs]
        except Exception as err:
            print("Error: parsing login page to obtain programs:\n", err)
            logging.warning(err)
            return False

        """
        ------------------------------------------
        Parse with beautiful soup to obtain
        student page (my special case)
        ------------------------------------------
        soup_login = BeautifulSoup(login.text, "html.parser")
        student_staff = soup_login.find(
            "div", id="viewing_as_permission_group")
        link_student = student_staff.find_all(
            "div")[1].a["href"]  # link to user session
        """
        try:
            """
            -------------------------------------------------
            GET request to the page project
            Here, thank to session, we dont need login again
            -------------------------------------------------
            """
            # Check if the problems is for the programs
            # for name, url in programs_urls[0].items():
            for url in programs_urls:
                # print(name, url)
                try:
                    response = session.get(url["url"])
                    curriculum_name = url["name"]  # name of the curriculum
                    response.raise_for_status()
                except requests.exceptions.RequestException as err:
                    print("Error: GET request to the curriculum page:\n", err)
                    logging.warning(err)
                    return False

                project_page = session.get(URL_PAGE, allow_redirects=False)
                project_page.raise_for_status()

                if project_page.status_code == 200:
                    print("Project page successful")
                    break
        except requests.exceptions.RequestException as err:
            print("Error: GET request to the project page:\n", err)
            logging.warning(err)
            return False

        """
        ------------------------------------------
        Check if the project page is exist
        ------------------------------------------
        """
        if project_page.status_code == 302:
            print("This project does not exist or you do not have access to it")
            return False

        """
        ------------------------------------------
        Parse with beautiful soup to obtain:
            - Name of curriculum
            - Project name
            - Project Description
        ------------------------------------------
        """
        print("Curriculum: {}".format(curriculum_name.strip())
              )  # name of the curriculum

        project_page = BeautifulSoup(project_page.text, "html.parser")

        project_name = project_page.find("h1", class_="gap")
        project_name = project_name.get_text()
        print("Project name: {}".format(project_name))

        project_description = project_page.find(
            "div", id="project-description")

        """
        ------------------------------------------
        Obtain FilesNames required for the project
        ------------------------------------------
        """
        list_group = project_page.find_all("div", class_="list-group-item")
        list_files = [group.find_all("li")[2].find("code").get_text().strip().split(",")
                      for group in list_group]
        list_files = [file.strip()
                      for sublist in list_files for file in sublist]
        print(list_files)
        print(len(list_files))

        """
        -----------------------------
        Solve problems with the links
        -----------------------------
        """

        all_links = project_description.find_all("a")
        for link in all_links:
            link1 = "https://intranet.hbtn.io/{}".format(link["href"])
            """
            ----------------------------------------------------------------
            Using allow_redirects to avoid redirections and obtain real page
            only redirect pages change the value of the url
            assign the new value of the url
            ----------------------------------------------------------------
            """
            page1 = session.get(link1, allow_redirects=False)
            if page1.status_code == 302:
                page_soup = BeautifulSoup(page1.text, "html.parser")
                real_url = page_soup.find("a")["href"]
                index = all_links.index(link)
                project_description.find_all("a")[index]["href"] = real_url

        string_description = str(project_description.prettify())

        """
        ------------------------------------------
        Write on the README file with options:
            0: New file or rewrite
            1: Append to end the file
        ------------------------------------------
        """
        if option == "1":
            mode = "+a"
        else:
            mode = "+w"

        with open("README.md", mode=mode, encoding="utf-8") as file:
            file.write("# [{}]({})\n\n".format(
                project_name.split(".")[1].strip(), URL_PAGE))
            file.write(
                "<html>\n{}\n[--LINK PROJECT--]({})\n</html>".format(string_description, URL_PAGE))

        with open("files.txt", mode="+w", encoding="utf-8") as file:
            write_files = ["{}\n".format(file) for file in list_files]
            file.writelines(write_files)

        return True


if __name__ == "__main__":
    if len(argv) != 3:
        print(
            """
            USAGE: make_readme NUMBER_OF_PROJECT 0/1
                0: New file or Rewrite README
                1: Append to the end of README
            """)
    else:
        URL_PAGE = "https://intranet.hbtn.io/projects/" + argv[1]
        option = argv[2]

        status = make_readme(URL_PAGE, option)

        if status:
            print("-----README Created succesfully-----")
        else:
            print("-----README Could not be created-----")
