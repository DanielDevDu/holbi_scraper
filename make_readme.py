#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
from sys import argv
from os import getenv


def make_readme(URL_PAGE, option):
    URL = "https://intranet.hbtn.io/auth/sign_in"

    with requests.session() as session:

        """
        ------------------------------------------
        GET request to the main pega of Holberton
        ------------------------------------------
        """
        response = session.get(URL)
        if response.status_code != 200:
            print("Some failed with GET")
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
            if login.status_code != 200:
                print("Some failed Login")
                return False
        except Exception as err:
            print(err)
            return False

        """
        ------------------------------------------
        Parse with beautiful soup to obtain
        student page (my special case)
        ------------------------------------------
        """
        soup_login = BeautifulSoup(login.text, "html.parser")
        student_staff = soup_login.find(
            "div", id="viewing_as_permission_group")
        link_student = student_staff.find_all(
            "div")[1].a["href"]  # link to user session

        try:
            """
            -------------------------------------------------
            GET request to the page project
            Here, thank to session, we dont need login again
            -------------------------------------------------
            """
            project_page = session.get(URL_PAGE, allow_redirects=False)
            if project_page.status_code != 200:
                print("""Some failed with Project page\
                         \nAre you sure that this is the URL: {} ?
                       """.format(URL_PAGE)
                      )
                return False
        except Exception as err:
            print(err)
            return False

        """
        ------------------------------------------
        Parse with beautiful soup to obtain:
            - Project name
            - Project Description
        ------------------------------------------
        """
        project_page = BeautifulSoup(project_page.text, "html.parser")

        project_name = project_page.find("h1", class_="gap")
        project_name = project_name.get_text()

        project_description = project_page.find(
            "div", id="project-description")

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
            file.write("# {}\n\n".format(project_name))
            file.write("<html>\n{}\n[--LINK PROJECT--]({})\n</html>".format(string_description, URL_PAGE))

        return True


if __name__ == "__main__":
    if len(argv) != 3:
        print(
            """
            USAGE: {} URL 0/1
                0: New file or Rewrite README
                1: Append to the end of README
            """.format(argv[0]))
    else:
        URL_PAGE = argv[1]
        option = argv[2]

        status = make_readme(URL_PAGE, option)

        if status:
            print("-----README Created succesfully-----")
        else:
            print("-----REAME Cannot be created-----")
