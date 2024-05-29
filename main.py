import json
import logging
import pathlib
import re

import requests
import yaml

# load config.yaml
with open("config.yaml") as c:
    cfg = yaml.load(c, Loader=yaml.FullLoader)


# setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S")
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

# helper function to recursively delete folders
def rm_tree(pth: pathlib.Path):
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


def main(cfg=cfg, logger=logger):
    # setup base dir variables
    base_dir = pathlib.Path().absolute()
    base_cache_folder = pathlib.Path(f"{base_dir}/cache")

    # clear the cache folder
    if base_cache_folder.exists():
        rm_tree(base_cache_folder)

    # setup the HTTP header for the API request
    h = {
        "Auth-API-Id": cfg["api_key"],
    }

    """
    loop over pages until we hit a 404.
    use pgno as a counter.
    """
    pgno = 1
    while True:
        p = {
            "pgno": pgno,
            "pgsize": cfg["pgsize"],
            "expired": cfg["expired"],
            "Status": cfg["status"],
            "scamtype": cfg["scamtype"],
            "fields": cfg["fields"],
        }

        logger.info(
            f"Getting {p['pgsize']} results on page {pgno} of ScamType {p['scamtype']} from aa419 API."
        )

        # do API request
        r = requests.get("https://api.aa419.org/fakesites", params=p, headers=h)

        """
        if we get a 404 ('No rows found') it means
        we got all the current active scams and that
        the loop can be stopped.
        
        Otherwise, add 1 to the pgno counter and
        start caching results to local JSON files.
        """
        if r.status_code == 404:
            break
        else:
            pgno = pgno + 1

        # loop over the results
        for j in r.json():
            # setup the local cache folder
            cache_folder = f"{base_cache_folder}"
            pathlib.Path(cache_folder).mkdir(parents=True, exist_ok=True)
            cache_file = f"{cache_folder}/{j['Id']}.json"

            # parse out the email from 'PublicComments' when available
            email = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", j["PublicComments"])
            try:
                j["email"] = email.group(0)
            except AttributeError:
                j["email"] = ""

            # cache current scam
            logger.info(f"Caching to file {cache_file}.")
            with pathlib.Path(f"{cache_file}").open("w") as f:
                json.dump(j, f)


if __name__ == "__main__":
    main()
