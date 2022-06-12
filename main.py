import json
import logging
import os.path
from typing import TextIO
import click
from progress.bar import ChargingBar

from buster import DDBuster


# Setup logger
# TODO: setup logger


# NOTE: if your have no "auth.json" file, you need to create it,
# otherwise you should find one empty after the first you run the script.
# Inside "auth.json" you must set:
#   1. add "username": YOUR-USERNAME
#   2. add "password": YOUR-PASSWORD

# Check if "auth.json" exists, else create a new one empty
if not os.path.exists('auth.json'):
    empty_auth = {'username': 'YOUR-USERNAME', 'password': 'YOUR-PASSWORD'}
    with open('auth.json', 'w') as authfile:
        json.dump(empty_auth, authfile)
        authfile.close()
    logging.debug('Created new empty file "auth.json"')
# Load credentials
with open('auth.json', 'r') as authfile:
    credentials = json.load(authfile)
    authfile.close()
    logging.debug('Credentials loaded successfully')

# Load configuration
with open("config.json", 'r') as configfile:
    config = json.load(configfile)

    if "headers" in config.keys():
        headers = config['headers']
        logging.debug(f'Headers found: {headers}')
    else:
        headers = None

    if "downloadPath" in config.keys():
        download_path = config['downloadPath']
        logging.debug(f'Output path found: {download_path}')
        if not os.path.exists(download_path):
            os.makedirs(download_path)
            logging.debug(f'Created new directory {download_path}')
    else:
        download_path = None

    configfile.close()


@click.command()
@click.argument('url',
                nargs=1, type=click.STRING) # help="Url of the pdf to download"
@click.option('--filename', '-fn', help="Filename of the output .pdf file",
              nargs=1, type=click.STRING, default=None)
@click.option('--filepath', '-fp', help="Path of the output .pdf file",
              nargs=1, type=click.Path(exists=True), default=None)
def download(url: str, filename: str = None, filepath: str = None):
    # Choose download path
    if filepath is not None:
        dp = filepath
    else:
        dp = download_path
    # Initialize client
    buster = DDBuster(headers=headers, download_path=dp)

    # Download pdf
    if buster.login(credentials['username'], credentials['password']):
        buster.download(url, filename=filename)
    else:
        print('Unable to login, try later!')


@click.command()
@click.argument('source',
                nargs=1, type=click.File('r')) # help='Source .json file containing {"PDF-NAME": "PDF-URL"} fields'
@click.option('--usenames', '-un', help='Use keys of the .json source file as names',
              nargs=1, type=click.BOOL, default=False)
@click.option('--filepath', '-fp', help="Path of the output .pdf file",
              nargs=1, type=click.Path(exists=True), default=None)
def downloadMultiple(source: TextIO, usenames: bool = False, filepath: str = None):
    # Load urls
    urls = json.load(source)

    # Choose download path
    if filepath is not None:
        dp = filepath
    else:
        dp = download_path
    # Initialize client
    buster = DDBuster(headers=headers, download_path=dp)

    # Download pdf
    if buster.login(credentials['username'], credentials['password']):
        bar = ChargingBar('Download', max=len(urls))
        for key in urls.keys():
            url = urls[key]
            filename = key if usenames else None
            buster.download(url, filename=filename)
            bar.next()
        bar.finish()
    else:
        print('Unable to login, try later!')


@click.group(help="CLI to download pdf files from studwiz for POLIMI")
def cli():
    pass


def main():
    cli.add_command(download)
    cli.add_command(downloadMultiple)
    cli()


if __name__ == '__main__':
    main()
