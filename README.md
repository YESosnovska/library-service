# Library API Service

API service for local library service management written on DRF

## Features

- JWT authenticated
- Admin panel /admin/
- Documentation is located at /api/doc/swagger/
- Managing borrowings
- Creating books
- Filtering borrowings for admin users

## Components

- Book Service :
  - Managing books amount (CRUD for Books)
  - API:
    - POST:```books/``` - add new book
    - GET:```books/```  - get a list of books
    - GET:```books/<id>/``` - get book's detail info 
    - PUT/PATCH:```books/<id>/``` - update book (also manage inventory)
    - DELETE:```books/<id>/``` - delete book
  
- Users Service:
  - Managing authentication & user registration
  - API:
     - POST:```users/``` - register a new user 
     - POST:```users/token/``` - get JWT tokens 
     - POST:```users/token/refresh/``` - refresh JWT token 
     - GET:```users/me/``` - get my profile info 
     - PUT/PATCH:```users/me/``` - update profile info 

- Borrowings Service:
  - Managing users' borrowings of books
  - API:
    - POST:```borrowings/``` - add new borrowing (when borrow book - inventory should be made -= 1) 
    - GET:```borrowings/?user_id=...&is_active=...``` - get borrowings by user id and whether is borrowing still active or not.
    - GET:```borrowings/<id>/``` - get specific borrowing 
    - POST:```borrowings/<id>/return/``` - set actual return date (inventory should be made += 1)

## Installing using GitHub

1. Clone the repository
 ```shell
  git clone https://github.com/YESosnovska/library-service/
  cd library-service
```

2. Create a virtual environment and activate it
```shell
  python -m venv venv
  source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

3. Create .env file with SECRET_KEY using .env.sample

4. Install requirements
```shell
  pip install -r requirements.txt
```

5. Apply migrations
```shell
  python manage.py migrate
```

6. Create superuser
```shell
  python manage.py createsuperuser
```

7. Run server
```shell
  python manage.py runserver
```

You also can register new non-admin user using ```api/users/```

You also need to obtain token in ```api/users/token/``` page


