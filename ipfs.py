import json
import os
import requests




def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"
    
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIyMDZlNWU3Yi05NzI4LTQxYzYtOWM0MS0wNTg0NWViM2Q0NTIiLCJlbWFpbCI6InJ3aWxsZUBzZWFzLnVwZW5uLmVkdSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6IkZSQTEifSx7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6Ik5ZQzEifV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiJhNzVkOTkxNzc0YmFmNDI4NTIwYSIsInNjb3BlZEtleVNlY3JldCI6IjY5ODJlNmNmMmQ0ZWY2NzJjZjhmMDI0MmQ4YzQwODRkNTQ2YjQwNjUwOTY5OTI3ZGE5NzYyM2QyNTc4ZDVhNDkiLCJleHAiOjE4MDQwMjg2NjV9.fNHVS4LD-qXuw8BSaLQlAnGoJIe0WolKS1POmeDCU1U"
    
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json"
    }
    
    r = requests.post(url, headers=headers, json=data, timeout=30)
    r.raise_for_status()
    
    cid = r.json()["IpfsHash"]
    return cid


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), "get_from_ipfs accepts a cid in the form of a string"
    
    r = requests.get(f"https://ipfs.io/ipfs/{cid}", timeout=30)
    r.raise_for_status()
    
    data = r.json()
    
    assert isinstance(data, dict), "get_from_ipfs should return a dict"
    return data


