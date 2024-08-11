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


def upload_facebook_image(image_data, access_token):
    url = f"https://graph.facebook.com/me/photos"
    payload = {"access_token": access_token}
    files = {"source": ("cover_image.jpg", image_data, "image/jpeg")}
    response = requests.post(url, data=payload, files=files)
    return response.json()


def create_facebook_post(message, access_token, page_id, image_id=None):
    url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {"message": message, "access_token": access_token}
    if image_id:
        payload["object_attachment"] = image_id
    response = requests.post(url, data=payload)
    return response.json()
