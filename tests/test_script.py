import httpx

BASE_URL = "http://127.0.0.1:8000"


def test_get_form():
    url = f"{BASE_URL}/get_form"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"applicant_name": "Test"}
    response = httpx.post(url, headers=headers, data=data)
    print(f"GET Form Response ({response.status_code}): {response.text}")


if __name__ == "__main__":
    try:
        print("Testing /get_form route:")
        test_get_form()

    except Exception as e:
        print(f"Error during testing: {e}")
