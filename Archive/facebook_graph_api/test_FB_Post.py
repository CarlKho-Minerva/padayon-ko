import requests


def create_facebook_post(message, access_token, page_id):
    url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {"message": message, "access_token": access_token}
    response = requests.post(url, data=payload)
    return response.json()


if __name__ == "__main__":
    FACEBOOK_ACCESS_TOKEN = ""
    FACEBOOK_PAGE_ID = ""
    TEST_MESSAGE = (
        "Hello World - Testing Facebook Graph API! From VS Code with Python this time"
    )

    response = create_facebook_post(
        TEST_MESSAGE, FACEBOOK_ACCESS_TOKEN, FACEBOOK_PAGE_ID
    )
    print(f"Facebook response: {response}")
