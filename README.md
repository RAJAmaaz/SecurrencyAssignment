# API Test Assignment

API test of gorest.co.in website. API tests are written by only using python3, pytest, jsonpath and requests.

## Test Cases

API test cases are  written for gorest.co.in/public-api/users endpoint

	1 -  GET /public-api/users
	2 -  POST /public-api/users
	3 -  GET /public-api/users/{user_id}
	4 -  PUT /public-api/users/{user_id}
	5 -  PUT /public-api/users/{user_id} wrong gender and status
	6 -  PUT /public-api/users/{user_id} wrong gender
	7 -  PUT /public-api/users/{user_id} wrong status
	8 -  PUT /public-api/users/{user_id} wrong email
	9 -  DELETE /public-api/users/123
	10 - DELETE /public-api/users/123 wrong url
	11 - POST /public-api/users verify Authentication by passing wrong access-token
	12 - POST /public-api/users verify with empty body
	13 - POST /public-api/users verify with wrong body


### Prerequisites

Install prequisites with;

	pip install -r requirements.txt
	
### How to run

Test Cases are placed in GoRest_TestCases package in users_test.py file.You can run pytest cases using following commands;

	pytest .
	or
	pytest . -vv


