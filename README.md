Cards app.

Backend

Installation

1. git clone https://github.com/a-dubrovin/cards_app.git
2. cd ./cards_app/
3. virtualenv ./env
4. source ./env/bin/activate
5. pip install -r ./backend/requirements.txt
6. cd ./backend/
7. ./manage.py migrate

Run

1. ./manage.py runserver

Tests

1. ./manage.py test

Use

1. Register user

curl --location --request POST 'http://127.0.0.1:8000/api/v1/account/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "testuser1",
    "password": "test_pretty_user"
}'

2. Get token(authorization)

curl --location --request POST 'http://127.0.0.1:8000/api/v1/account/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "testuser",
    "password": "test_pretty_user"
}'

3. Get cards list 

curl --location --request GET 'http://127.0.0.1:8000/api/v1/cards/' \
--header 'Authorization: Token <user_token>'

4. Get series info

curl --location --request GET 'http://127.0.0.1:8000/api/v1/series/<series_number>' \
--header 'Authorization: Token <user_token>'

5. Create new cards

curl --location --request POST 'http://127.0.0.1:8000/api/v1/cards/' \
--header 'Authorization: Token <user_token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "series": "<series_number>",
    "cards_quantity": "<int>",
    "validity": "<int>"
}'


Frontend

Installation

 1. cd ./frontend/
 2. npm install

Run

 1. cd ./frontend/
 2. npm run serve

Build

 1. cd ./frontend/
 2. npm run build
