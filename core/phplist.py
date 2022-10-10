import requests
import json
import base64

SUBSCRIBE_URL = "https://lists.gypsyswingrevue.com/lists/api/v2/subscribers"
BASE_URL = "https://lists.gypsyswingrevue.com/lists/api/v2"
LOGIN_NAME = "Elliot"
PASSWORD = "3lliotR33d"


def add_subscriber(subscriber_email):
    print(subscriber_email)

    login_name = LOGIN_NAME
    password = PASSWORD
    base_url = BASE_URL
    credentials = {}

    form_params = {
        "login_name": login_name,
        "password": password,
    }

    try:
        response = requests.post(base_url + "/sessions", form_params)
    except:
        print("Error")
        print(response)

    if response:
        print(response)

        data = response.json()
        print(data)

        key = data.get("key")

        # credentials = base64_encode(login_name)
        # credentials = {"login_name": key}
        credentials_string = f"{login_name}:{key}"
        credentials_bytes = credentials_string.encode("ascii")
        base64_bytes = base64.b64encode(credentials_bytes)
        credentials = base64_bytes.decode("ascii")

        print("cred_str: " + credentials_string)
        print("byte_str: ")
        print(credentials_bytes)
        print("cred: " + credentials)
        auth = "Basic " + credentials
        print("auth: " + auth)
        headers = {
            "Authorization": auth,
            "Content-Type": "application/json",
        }

        payload = {
            "email": subscriber_email,
            # "confirmed": "true",
            # "blacklisted": "false",
            # "htmlemail": "true",
            # "disabled": "false",
            "html_email": "true",
        }

        json_payload = json.dumps(payload)
        print("data: ", json_payload)

    try:
        subcriber_request = requests.post(
            base_url + "/subscribers",
            headers=headers,
            data=json_payload,
        )
        print(subcriber_request.json())

    except Exception as e:
        print("add error")
        print(e)
