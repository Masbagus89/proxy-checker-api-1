import socket
import ssl
import json
import re
from app.models import save_proxy

IP_RESOLVER = "speed.cloudflare.com"
PATH_RESOLVER = "/meta"
PROXY_FILE = "Data/ProxyIsp.txt"

def check(host, path, proxy):
    payload = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "User-Agent: Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240\r\n"
        "Connection: close\r\n\r\n"
    )

    ip = proxy.get("ip", host)
    port = int(proxy.get("port", 443))
    conn = None

    try:
        ctx = ssl.create_default_context()
        conn = socket.create_connection((ip, port), timeout=5)
        conn = ctx.wrap_socket(conn, server_hostname=host)
        conn.sendall(payload.encode())

        resp = b""
        while True:
            data = conn.recv(4096)
            if not data:
                break
            resp += data

        resp = resp.decode("utf-8", errors="ignore")
        headers, body = resp.split("\r\n\r\n", 1)
        return json.loads(body)
    except:
        return {}
    finally:
        if conn:
            conn.close()

def clean_org_name(org_name):
    return re.sub(r'[^a-zA-Z0-9\s]', '', org_name) if org_name else org_name

def run_proxy_check():
    try:
        with open(PROXY_FILE, "r") as f:
            proxies = f.readlines()
    except FileNotFoundError:
        print(f"File tidak ditemukan: {PROXY_FILE}")
        return

    for line in proxies:
        line = line.strip()
        if not line:
            continue
        try:
            ip, port, country, org = line.split(",")
            proxy_data = {"ip": ip, "port": port}

            ori, pxy = [
                check(IP_RESOLVER, PATH_RESOLVER, {}),
                check(IP_RESOLVER, PATH_RESOLVER, proxy_data)
            ]

            if ori and pxy and ori.get("clientIp") != pxy.get("clientIp"):
                org_name = clean_org_name(pxy.get("asOrganization"))
                proxy_country = pxy.get("country")
                save_proxy(ip, port, proxy_country or country, org_name or org)
        except:
            continue
