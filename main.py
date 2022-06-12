import json
import logging
import re
from bs4 import BeautifulSoup
from requests import Session

logger = logging.getLogger(__name__)


class DDBuster:

    def __init__(self):
        self.__session = Session()
        self.__session.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
        }

    def __find_urls(self, string):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, string)
        return [x[0] for x in url]

    def __fetch_download_url(self, url: str) -> str or None:
        response = self.__session.get(url=url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            scripts = soup.findAll('script')

            download_script = next(filter(lambda script: '"src"' in script.text, scripts), None)
            if download_script is not None:
                urls = self.__find_urls(download_script.text)
                target_url = next(filter(lambda url: 'pdf_auto_download.php' in url, urls), None)

                if target_url is not None:
                    logger.debug(f'Download url found: {target_url}')
                    return target_url

                else:
                    logger.debug('Unable to find valid url')
                    return None

            logger.debug('Unable to locate the download script')
            return None

        logger.debug(f'URL {url} not working')
        return None

    def __save_pdf(self, filename: str, pdf_bytes: bytes, filepath: str = None):
        # Build path
        if filepath is not None:
            path = filepath + "/"
        else:
            path = "./"

        try:
            # Save file at path
            with open(f'{path}{filename}.pdf', 'wb') as pdffile:
                pdffile.write(pdf_bytes)
                pdffile.close()
            logger.debug('File saved successfully')

        except Exception as e:
            logger.error("Exception occurred!", exc_info=True)

    def login(self, username: str, password: str) -> bool:
        login_url = "https://www.studwiz.com/user/userAccount.php"
        payload = {
            'email': username,
            'password': password,
            'loginSubmit': "Sign In"
        }
        response = self.__session.post(url=login_url, data=payload)

        if response.status_code == 200:
            logger.debug('Logged in!')
            return True
        else:
            logger.debug(f'Unable to log in, reason: {response.status_code}')
            return False

    def download(self, url: str):
        target_url = self.__fetch_download_url(url)
        response = self.__session.get(target_url)
        if response.status_code == 200:
            logger.debug('Download successful')
            filename = url.split("/")[-1]
            self.__save_pdf(filename, response.content)
        else:
            logger.debug('Unable to download the file')


if __name__ == '__main__':
    with open('auth.json', 'r') as authfile:
        credentials = json.load(authfile)
        authfile.close()

    buster = DDBuster()
    if buster.login(credentials['username'], credentials['password']):
        url = input('Enter a url to download: ')
        buster.download(url)
    else:
        print('Unable to login, try later!')
