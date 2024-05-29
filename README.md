# aa419 cacher

Example on how to use the aa419 JSON-API in Python.

Essentially this caches all current *active* scams of set search parameters in local json files for further tasks. It also does some extra regex parsing on the `PublicComments` field to grab out the e-mail address and add this as a standalone field in the JSON structure for ease of use in further tasks. Should be trivial to add onto for other types of info such as phone numbers etc if required by writing some regex.

See the [aa419 JSON-API documentation](https://www.aa419.org/jsonapi/) for further fine-tuning of results. Some things (status of scam, scamtype, what fields to extract) are already abstracted and configurable via the `config.yaml` and can be changed there without touching the python code itself.

## Getting started

1. create an [account](https://db.aa419.org/signup.php) on aa419 and [copy your api key](https://db.aa419.org/login.php).
2. copy the example config by running `cp config.yaml.example config.yaml`.
3. replace the API key in `config.yaml` with your own API key.
4. recommended to setup a virtual environment using your preferred method and then running `pip3 install -r requirements.txt`.
5. run the script `python3 main.py`.
