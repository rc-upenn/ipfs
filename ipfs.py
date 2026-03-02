import requests
import json

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	jwt = os.getenv("PINATA_JWT")
	if not jwt:
        raise RuntimeError("PINATA_JWT not set, so cid can’t be created.")

    r = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        headers={"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"},
        json=data,
        timeout=30
    )
    r.raise_for_status()

    cid = r.json()["IpfsHash"]
    return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	r = requests.get(f"https://ipfs.io/ipfs/{cid}", timeout=30)
    r.raise_for_status()

    if content_type == "json":
        data = r.json()
    else:
        data = json.loads(r.content.decode("utf-8"))

    assert isinstance(data, dict), "get_from_ipfs should return a dict"
    return data
