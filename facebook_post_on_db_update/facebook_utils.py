import requests


def download_image(image_url):
    if not image_url:
        print("No image URL provided.")
        return None
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"An error occurred while downloading the image: {e}")
        return None


import requests


def download_image(image_url):
    if not image_url:
        print("No image URL provided.")
        return None
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"An error occurred while downloading the image: {e}")
        return None


def create_facebook_post_with_image(message, access_token, page_id, image_data=None):
    url = f"https://graph.facebook.com/{page_id}/photos"

    payload = {"message": message, "access_token": access_token}

    files = None
    if image_data:
        files = {"source": ("image.jpg", image_data, "image/jpeg")}

    try:
        response = requests.post(url, data=payload, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while creating the Facebook post: {e}")
        return None
