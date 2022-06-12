# ddbuster
Pdf downloader for andreadd's repository (aka studwiz).

## Setup
NOTE: you need an account on studwiz.com

## Requirements
Install the requirements via
```
python -m pip install -r requirements.txt
```

### Credentials
You need to create an `auth.json` file or run the cli one time through the command `python main.py` to create automatically a structured empty auth file.
The structure of the auth file must be the following:
```
{
  "username": YOUR-USERNAME,
  "password": YOUR-PASSWORD
}
```
Replace ´YOUR-USERNAME´ with the username (or email) to your account on studwiz.com and `YOUR-PASSWORD` with the corresponding password.

### Configuration
Inside the `ddbuster` folder you should have the file `config.json` that specify some general configuration (already containing default values).
```
{
  "downloadPath": DOWNLOAD-PATH,
  "headers": HEADERS
}
```
* `DOWNLOAD-PATH` specify the path of the output PDF files;
* `HEADERS` specify the headers used by the HTTP client to perform requests.

## Usage
There are two available commands:
* `download`: download one PDF given its url
* `downloadMultiple`: download multiple PDF given a JSON formatted file containing their urls

The JSON file used by `downloadMultiple` must contain a pair `"KEY": "URL"` for each pdf you want to download.
```
{
  "KEY-1": "URL-1",
  "KEY-2": "URL-2",
  ...
}

Each command has its options and arguments. To find out more about the usage you can type:
* `python main.py`for general help
* `python main.py COMMAND --help`for specific help
