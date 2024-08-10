from notion_client import Client
import requests
import os

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_API_KEY"))


# Function to fetch page properties, including cover image
def fetch_page_properties(page_id):
    try:
        page = notion.pages.retrieve(page_id)
        print(f"Page properties: {page}")  # Debugging: Print the entire response
        # Get cover image URL from the 'file' type
        cover_image_url = page.get("cover", {}).get("file", {}).get("url", "")
        if not cover_image_url.lower().startswith(("http://", "https://")):
            cover_image_url = ""
        return cover_image_url
    except Exception as e:
        print(f"An error occurred while fetching page properties: {e}")
        return ""


# Function to download an image from a URL
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


def main():
    # Replace with your Notion page ID
    page_id = "4a7a4f9c-e3ae-49a1-873a-7baa70a0b178"

    # Fetch cover image URL
    cover_image_url = fetch_page_properties(page_id)
    print(f"Cover Image URL: {cover_image_url}")

    # Download cover image
    if cover_image_url:
        cover_image_data = download_image(cover_image_url)
        if cover_image_data:
            print("Cover image downloaded successfully.")
            # Optionally save the image to a file
            with open("cover_image.jpg", "wb") as file:
                file.write(cover_image_data)
            print("Cover image saved as cover_image.jpg.")
        else:
            print("Failed to download cover image.")
    else:
        print("No cover image URL found.")


if __name__ == "__main__":
    main()
