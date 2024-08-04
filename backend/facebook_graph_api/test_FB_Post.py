import requests


def create_facebook_post(message, access_token, page_id):
    url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {"message": message, "access_token": access_token}
    response = requests.post(url, data=payload)
    return response.json()


if __name__ == "__main__":
    FACEBOOK_ACCESS_TOKEN = "EAALn51qddPIBO1b3w0XH4Y0MfQ2eRkAc1lxadC1xuZCoVk4KguZCG8csusAxjsRJyEqeHzOBo5VnvZAyMzLfqQhDQ4wnjJDR0beNVQkK0l5Jglkg8yl1lr5tkSz62rcVQVHZAvn32UdEToxq1aWsbVfZCl8SWv7ZA8I53FRbMndyCHMseyvcF0rL1WUpeBeAVAGGjdDNlPSag7aXff9KPF6yCBDJkSz5ocZBD4HjTXk"
    FACEBOOK_PAGE_ID = "394193433777965"
    TEST_MESSAGE = (
        "Hello World - Testing Facebook Graph API! From VS Code with Python this time"
    )

    response = create_facebook_post(
        TEST_MESSAGE, FACEBOOK_ACCESS_TOKEN, FACEBOOK_PAGE_ID
    )
    print(f"Facebook response: {response}")
