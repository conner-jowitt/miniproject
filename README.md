# BrIW

BrIw is a web based coffee round controller written in Python, with webpages made in html, CSS, and a little JS. The main page includes the user web-view, and an API. Visiting the home directory ("/") you can see a list of the current pages available and their location. All api pages have an active and inactive view, as all entries can either be active or inactive in the database (currently only useful fr rounds).

### How to get it working

The repo includes almost everything you will need (and a lot of stuff you don't need which was useful in earlier stages of development). The main missing feature is a file called "connection.py", containing a single function which looks like this:

```sh
import pymysql


def create_db_connection():
    db = pymysql.connect(
        "xxxxxxxxxx", #host
        "xxxxxxxxxx", #username
        "xxxxxxxxxx", #password
        "xxxxxxxxxx", #database
        autocommit=True
    )
    return db
```

Other requirements are:

* Flask
* pymysql

### Main files

Most of he files in the repo are from a legacy version of the application. The only files which are still used are:

| File/Folder | Use |
| ------ | ------ |
| new_api_with_flask.py | main file, this starts the server |
| store.py | contains all the functions which interact with the database |
| static/ | contains the CSS file for the webpages |
| templates/ | Contains the main webpage templates |

### How you can help

The application needs a teting suite developing. It would also be good to get a synchronous connecton to the database on the "/rounds" page to improve load times. Finally, the main files are in need of refactoring to improve readability and remov code smell.

### Contact me

Please do. I need a friend :)
