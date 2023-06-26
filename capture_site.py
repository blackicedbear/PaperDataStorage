import sys
import requests

def main():
    # Get url from user by sys.argv
    url = sys.argv[1]
    
    # Get file name from user by sys.argv
    file_name = sys.argv[2]

    # Get the content of the site
    content = get_content(url)

    # Save the content to a file
    save_content(content, file_name)

def get_content(url):
    # Get the content of the site with custom user agent
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.3.904 Yowser/2.5 Safari/537.36'}
    content = requests.get(url, headers=headers)

    # Return the content
    return content

def save_content(content, file_name):
    # Save the content to a file
    with open(file_name, 'wb') as binary_file:
        binary_file.write(content.content)

if __name__ == "__main__":
    main()