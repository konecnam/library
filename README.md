# library
## django app
## tests

all tests: `python manage.py test`

selenium one class: `python manage.py test library.tests.MyUserIn`

selenium one class one test: `python manage.py test library.tests.MyUserIn.test_add_book_none`

rest API one class: `python manage.py test library.tests.RestApiTest`

### App
library/mylibrary - must be
server: `python manage.py runserver`

### Playwright - 
library - must be
server: `npx playwright test --workers=1`

`cd ..` back from mylibrary on library
 