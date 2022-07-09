#!/usr/bin/python3

from app.make_readme import make_readme
from sys import argv


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