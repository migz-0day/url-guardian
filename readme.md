## URL GUARDIAN
A security focused url analysis tool that helps in identifying potentially suspicious or malicious URLs.

## Features
# URL Analysis
- URL protocal normalization
- URL shortener detection
- Ip address detection
- suspecious key words
- Punycode detection
- subdomain stucture checks
- Non standard port detection
- Excessive slash detecion
- Excessive hyphen detection

# Advanced
- domain age analysis using WHOIS.
- HTTP redirection detection
- URL decoding and encoded-character inspection.

## Technologies

- Python (flask,requests,python-whois)
- javaScript
- HTML
- CSS
- SQLite

## Project structure
```
URL-Gurdian/
|
|---app.py
|--hist.db
|--requirements.txt
|
|--templates/
|   --home.html
|
|--static/
    |--script.js
    ---style.css
```

## How it works
1. User enters a URL
2. URL Guardian noemalizes and parses the URL.
3. inspecion is done on different URL characteristics.
4. Whois and http checks gather more info
5. The result is presented to the user inluding reasons.
6. scan history is stored in SQlite(hist.db)

## Installation
  # requirements
 * Python 3.13 or any compatible version.
 * pip or uv

# Set up
 clone the repo
 ```bash
 git clone https://github.com/migz-0day/url-guardian.git
 cd url-gurdian
 ```
 create an enviroment
 ```bash
 python -m venv .venv
```
install dependacies
```bash
pip install -r requirements.txt
```
To run
```bash
python app.py
```
## NOTE  
Confidence is URL Guardian telling you how confident it is with the result.

#

<img width="1920" height="901" alt="Document — Mozilla Firefox 8_27_2026 10_27_39 PM" src="https://github.com/user-attachments/assets/c5e54baa-c045-4f55-914a-c3afd32b2d09" />
<img width="1920" height="881" alt="Document — Mozilla Firefox 8_27_2026 10_29_04 PM" src="https://github.com/user-attachments/assets/cf9f8e7b-a2bd-4610-92e7-bbe76261a158" />
<img width="1920" height="870" alt="Document — Mozilla Firefox 8_27_2026 10_29_43 PM" src="https://github.com/user-attachments/assets/8ed2ece2-b2fc-4205-8e35-44befa560b1d" />
<img width="1920" height="899" alt="Document — Mozilla Firefox 8_27_2026 11_02_26 PM" src="https://github.com/user-attachments/assets/e867a335-cf88-4e66-888b-bc0a0e4059e5" />
<img width="1920" height="879" alt="Document — Mozilla Firefox 8_27_2026 11_03_08 PM" src="https://github.com/user-attachments/assets/38b618cc-94d9-4334-9744-fc60594c97e8" />
<img width="1920" height="879" alt="Document — Mozilla Firefox 8_27_2026 11_04_13 PM" src="https://github.com/user-attachments/assets/1ba56ea7-c036-427d-a4f1-c9bc4d260889" />

# working on


## sec note
It's risk score is not a garantee that the url is safe or malicious.
