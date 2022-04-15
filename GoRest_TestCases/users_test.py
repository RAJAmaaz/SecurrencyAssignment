import random
import string
import requests
import pytest
import json
from jsonpath_ng import jsonpath, parse
from GoRest_TestCases import ValueStorage


class TestSet_Users(object):

    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    test_url = "https://gorest.co.in/public-api/users?"
    name = "Securrency User"
    gender = "male"
    email = "user_" + str(ran) + "@securrency.com"
    status = "active"
    my_header = {"Authorization": "Bearer a04bff50ce15f3106a23df3f6966a1c96c07e81e30d4ee1a5e3414728c2d605e"}

    def __parse_json(self,json_string,json_path):
        my_value = ""
        try:
            json_string = json_string.replace("\'", "\"")
            json_string = json_string.replace("can\"t", "can\'t")
            json_string = json_string.replace("None", "\"None\"")
            json_data = json.loads(json_string)
            jsonpath_expression = parse(json_path)
            match = jsonpath_expression.find(json_data)
            my_value = match[0].value
        except:
            print("Parsing exception occurred")

        return my_value

    def __find_string_in_response(self, fullResponse, searchFor):
        check = True
        rawResponse = fullResponse
        if "result" not in rawResponse.text:
            check = False
        else:
            responseJSON = rawResponse.json()
            length_responseJSON = len(responseJSON["result"])
            for i in range(0, length_responseJSON, 1):
                check = searchFor in responseJSON["result"][i]["first_name"]
                if check == False:
                    return check
        return check


    # Test # 1 - GET /public-api/users
    @pytest.mark.order(1)
    def test_get_all_users(self):
        response = requests.get(self.test_url, headers=self.my_header)
        assert response.status_code == 200


    # Test # 2 - POST /public-api/users
    @pytest.mark.order(2)
    def test_post_a_user(self):
        my_data = {"name":self.name, "gender":self.gender, "email":self.email, "status":self.status}
        response = requests.post(self.test_url, headers=self.my_header , data=my_data)
        assert response.status_code == 200
        message = self.__parse_json(str(response.json()), "$.data[0].message")
        if message == "has already been taken":
            assert self.__parse_json(str(response.json()), "$.code") == 422
        else:
            ValueStorage.user_id = str(self.__parse_json(str(response.json()), "$.data.id"))
            assert self.__parse_json(str(response.json()), "$.code") == 201
            assert self.__parse_json(str(response.json()), "$.data.name") == self.name
            assert self.__parse_json(str(response.json()), "$.data.gender") == self.gender
            assert self.__parse_json(str(response.json()), "$.data.email") == self.email

    # Test # 3 - GET /public-api/users/{user_id}
    @pytest.mark.order(3)
    def test_get_a_users_with_id(self):
        test_url = "https://gorest.co.in/public-api/users/"+str(ValueStorage.user_id)
        response = requests.get(test_url, headers=self.my_header)
        assert response.status_code == 200
        assert self.__parse_json(str(response.json()), "$.code") == 200
        assert str(self.__parse_json(str(response.json()), "$.data.id")) == str(ValueStorage.user_id)
        assert self.__parse_json(str(response.json()), "$.data.name") == self.name
        assert self.__parse_json(str(response.json()), "$.data.gender") == self.gender
        assert self.__parse_json(str(response.json()), "$.data.email") == self.email

    # Test # 4 - PUT /public-api/users/123
    @pytest.mark.order(4)
    def test_put_a_user(self):
        my_data = {"name": "New_" + self.name, "gender":  self.gender, "email": "New_" + self.email,
                   "status":  self.status}
        test_url = "https://gorest.co.in/public-api/users/" + str(ValueStorage.user_id)
        response = requests.put(test_url, headers=self.my_header, data=my_data)
        assert response.status_code == 200
        assert self.__parse_json(str(response.json()), "$.code") == 200
        assert str(self.__parse_json(str(response.json()), "$.data.id")) == str(ValueStorage.user_id)
        assert self.__parse_json(str(response.json()), "$.data.name") == "New_" +self.name
        assert self.__parse_json(str(response.json()), "$.data.gender") == self.gender
        assert self.__parse_json(str(response.json()), "$.data.email") == "New_" +self.email
        assert self.__parse_json(str(response.json()), "$.data.status") == self.status

    # Test # 5 - PUT /public-api/users/{user_id} wrong gender and status
    @pytest.mark.order(5)
    def test_put_a_user_wrong_gender_status_values(self):
        my_data = {"name": "New_" + self.name, "gender": "New_" +self.gender, "email": "New_" + self.email,
                   "status": "New_" +self.status}
        test_url = "https://gorest.co.in/public-api/users/" + str(ValueStorage.user_id)
        response = requests.put(test_url, headers=self.my_header, data=my_data)
        assert response.status_code == 200
        assert self.__parse_json(str(response.json()), "$.code") == 422

    # Test # 6 - PUT /public-api/users/{user_id} wrong gender
    @pytest.mark.order(6)
    def test_put_a_user_wrong_gender_values(self):
        my_data = {"name": "New_" + self.name, "gender": "New_" + self.gender, "email": "New_" + self.email,
                   "status": self.status}
        test_url = "https://gorest.co.in/public-api/users/" + str(ValueStorage.user_id)
        response = requests.put(test_url, headers=self.my_header, data=my_data)
        assert response.status_code == 200
        assert self.__parse_json(str(response.json()), "$.code") == 422

    # Test # 7 - PUT /public-api/users/{user_id} wrong status
    @pytest.mark.order(7)
    def test_put_a_user_wrong_status_values(self):
        my_data = {"name": "New_" + self.name, "gender": self.gender, "email": "New_" + self.email,
                   "status": "New_" +self.status}
        test_url = "https://gorest.co.in/public-api/users/" + str(ValueStorage.user_id)
        response = requests.put(test_url, headers=self.my_header, data=my_data)
        assert response.status_code == 200
        assert self.__parse_json(str(response.json()), "$.code") == 422

    # Test # 8 - PUT /public-api/users/{user_id} wrong email
    @pytest.mark.order(8)
    def test_put_a_user_wrong_email_values(self):
        my_data = {"name": "New_" + self.name, "gender":  self.gender, "email": "",
                   "status": self.status}
        test_url = "https://gorest.co.in/public-api/users/" + str(ValueStorage.user_id)
        response = requests.put(test_url, headers=self.my_header, data=my_data)
        assert response.status_code == 200
        assert self.__parse_json(str(response.json()), "$.code") == 422

    # Test # 9 - DELETE /public-api/users/123
    @pytest.mark.order(9)
    def test_delete_a_user(self):
        test_url = "https://gorest.co.in/public-api/users/" + str(ValueStorage.user_id)
        response = requests.delete(test_url, headers=self.my_header)
        assert response.status_code == 200
        assert self.__parse_json(str(response.json()), "$.code") == 204

    # Test # 10 - DELETE /public-api/users/123 wrong url
    @pytest.mark.order(10)
    def test_delete_a_user_wrong_user_id(self):
        test_url = "https://gorest.co.in/public-api/users/" + str(ValueStorage.user_id)+"0000"
        response = requests.delete(test_url, headers=self.my_header)
        assert response.status_code == 200
        assert self.__parse_json(str(response.json()), "$.code") == 404

    # Test # 11 - POST /public-api/users verify Authentication by passing wrong access-token
    @pytest.mark.order(11)
    def test_post_a_user_with_wrong_access_token(self):
        my_data = {"name":self.name, "gender":self.gender, "email":self.email, "status":self.status}
        my_incorrect_header = {"Authorization": "Bearer a04bff50ce15f3106a23df3f6966a1c96c07e81e30d4ee1a5e3414728c2d605e_wrong"}
        response = requests.post(self.test_url, headers=my_incorrect_header , data=my_data)
        assert response.status_code == 200
        assert self.__parse_json(str(response.json()), "$.code") == 401
        assert str(self.__parse_json(str(response.json()), "$.data.message")) == "Authentication failed"

    # Test # 12 - POST /public-api/users verify with empty body
    @pytest.mark.order(12)
    def test_post_a_user_with_empty_body(self):
        my_data = {}
        response = requests.post(self.test_url, headers=self.my_header, data=my_data)
        assert response.status_code == 200
        assert self.__parse_json(str(response.json()), "$.code") == 422
        assert str(self.__parse_json(str(response.json()), "$.data[0].message")) == "can't be blank"

    # Test # 13 - POST /public-api/users verify with wrong body
    @pytest.mark.order(13)
    def test_post_a_user_with_wrong_body(self):
        my_data = {"my_name":self.name, "gender":self.gender, "my_email":self.email, "status":self.status}
        response = requests.post(self.test_url, headers=self.my_header, data=my_data)
        assert response.status_code == 200
        assert self.__parse_json(str(response.json()), "$.code") == 422
        assert str(self.__parse_json(str(response.json()), "$.data[0].message")) == "can't be blank"
        assert str(self.__parse_json(str(response.json()), "$.data[1].message")) == "can't be blank"