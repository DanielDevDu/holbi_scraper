# WEB SCRAPING

This project use requests and beautifull Soup libraries to automatize the process to make a readme with content of the Holberton School pages projects 

### Requeriment
- Have credential in Holberton School
- Install [Requests](https://requests.readthedocs.io/en/latest/user/install/) and [Beutifull Soup](https://beautiful-soup-4.readthedocs.io/en/latest/#installing-beautiful-soup)

#### Optional:
Put your password and your UserName like a enviroment variable in your workspace or CLI named "HOLBERTON_PASSWD" ex:
```bash
export HOLBERTON_PASSWD="Your password"
export HOLBERTON_EMAIL="Your Holberton email"
```

### Usage: 

If you put your user and password like enviroment variable
```bash
./make_readme URL 0/1
```
or
```bash
HOLBERTON_PASSWD="Your password" HOLBERTON_EMAIL="Your Holberton email" ./make_readme URL 0/1
```

##### Options

- URL: Page of the project
- 0: Create a new README
- 1: Append to the end of the README