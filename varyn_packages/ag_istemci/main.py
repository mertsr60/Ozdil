# Ağ İstemcisi ve REST API Kütüphanesi
import urllib.request
import json

def get_iste(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Varyn-HTTP/1.0"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.read().decode("utf-8")

def post_iste(url, veri_dict):
    data = json.dumps(veri_dict).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "Varyn-HTTP/1.0"}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.read().decode("utf-8")

def json_coz(metin):
    try:
        return json.loads(metin)
    except Exception:
        return None

def plugin():
    return {
        "ag_get_iste": get_iste,
        "ag_post_iste": post_iste,
        "ag_json_coz": json_coz
    }
