import json
import os
import requests




def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def _try_extract_jwt_from_env_text(txt: str):
    for line in txt.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == "PINATA_JWT":
            return v.strip().strip('"').strip("'")
    return None


def _try_extract_jwt_from_json_text(txt: str):
    try:
        d = json.loads(txt)
        if isinstance(d, dict):
            for k in ("PINATA_JWT", "pinata_jwt", "jwt"):
                v = d.get(k)
                if isinstance(v, str) and v.strip():
                    return v.strip()
    except Exception:
        pass
    return None


def _get_pinata_jwt():
    # 1) env var
    jwt = os.getenv("PINATA_JWT")
    if isinstance(jwt, str) and jwt.strip():
        return jwt.strip()

    cred_dir = "student_credentials"
    if os.path.isdir(cred_dir):
        common = [
            "PINATA_JWT",
            "pinata_jwt",
            "pinata_jwt.txt",
            ".env",
            "pinata.json",
            "credentials.json",
        ]

        paths = []
        for name in common:
            paths.append(os.path.join(cred_dir, name))
        for name in os.listdir(cred_dir):
            paths.append(os.path.join(cred_dir, name))

        seen = set()
        for p in paths:
            if p in seen:
                continue
            seen.add(p)

            if not os.path.isfile(p):
                continue

            try:
                txt = _read_text(p)
            except Exception:
                continue

            if txt.startswith("eyJ") and len(txt) > 50:
                return txt

            jwt2 = _try_extract_jwt_from_env_text(txt)
            if jwt2:
                return jwt2

            jwt3 = _try_extract_jwt_from_json_text(txt)
            if jwt3:
                return jwt3

    raise RuntimeError("PINATA_JWT not found (env var or student_credentials/ files).")


def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    jwt = _get_pinata_jwt()
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"}

    r = requests.post(url, headers=headers, json=data, timeout=30)
    r.raise_for_status()

    out = r.json()
    cid = out.get("IpfsHash")
    if not isinstance(cid, str) or not cid:
        raise RuntimeError(f"Pinata response missing IpfsHash: {out}")

    return cid


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), "get_from_ipfs accepts a cid in the form of a string"

    gateways = [
        "https://ipfs.io/ipfs",
        "https://cloudflare-ipfs.com/ipfs",
    ]

    last_err = None
    for gw in gateways:
        try:
            r = requests.get(f"{gw}/{cid}", timeout=30)
            r.raise_for_status()

            if content_type == "json":
                data = r.json()
            else:
                data = json.loads(r.content.decode("utf-8"))

            assert isinstance(data, dict), "get_from_ipfs should return a dict"
            return data
        except Exception as e:
            last_err = e

    raise RuntimeError(f"Failed to fetch {cid} from IPFS gateways. Last error: {last_err}")
