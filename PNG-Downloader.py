"""
The script is designed to download PNG images from a website,
while also supporting Basic Auth if the website requires it.
"""
# import modules
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# define function download_images with patameters: url(Site URL),
# output_directory(the path to the folder where the photo will be uploaded),
# username and password(if required))


def download_images(url, output_directory, username=None, password=None):
    # Add HTTP Basic Authentication headers
    headers = {}
    if username and password:
        headers['Authorization'] = requests.auth.HTTPBasicAuth(
            username, password)

    # Send a GET request to the URL
    response = requests.get(url, headers=headers, allow_redirects=True)

    # Response status code if it's not 200
    response.raise_for_status()

    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <img> tags whose src attribute ends with .png
    image_tags = soup.find_all(
        'img', {'src': lambda src: src.lower().endswith('.png')})

    # Loop for download each image and save to output dir
    for img in image_tags:
        img_url = urljoin(url, img['src'])
        response = requests.get(img_url, headers=headers)
        response.raise_for_status()
        filename = os.path.basename(img_url)
        output_path = os.path.join(output_directory, filename)
        with open(output_path, 'wb') as f:
            f.write(response.content)

    print(f"Downloaded {len(image_tags)} images to {output_directory}")


if __name__ == '__main__':
    # input user data
    url = input("Insert URL: ")
    output_directory = input("Enter path to download directory: ")
    username = input("Enter username (optional): ")
    password = input("Enter password (optional): ")

    # call function
    download_images(url, output_directory, username, password)
