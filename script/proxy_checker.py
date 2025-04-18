import socket
import ssl
import json
import concurrent.futures
import re
import os

IP_RESOLVER = "speed.cloudflare.com"
PATH_RESOLVER = "/meta"
PROXY_FILE = "Data/ProxyIsp.txt"
OUTPUT_FILE = "Data/alive.txt"
active_proxies = []

def check(host, path, proxy):
    payload = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "User-Agent: Mozilla/5.0\r\n"
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
    except Exception:
        pass
    finally:
        if conn:
            conn.close()
    return {}

def clean_org_name(org_name):
    return re.sub(r'[^a-zA-Z0-9\s]', '', org_name) if org_name else org_name

def process_proxy(proxy_line):
    proxy_line = proxy_line.strip()
    if not proxy_line:
        return

    try:
        ip, port, country, org = proxy_line.split(",")
        proxy_data = {"ip": ip, "port": port}
        ori, pxy = [
            check(IP_RESOLVER, PATH_RESOLVER, {}),
            check(IP_RESOLVER, PATH_RESOLVER, proxy_data)
        ]

        if ori and pxy and ori.get("clientIp") != pxy.get("clientIp"):
            org_name = clean_org_name(pxy.get("asOrganization"))
            proxy_entry = f"{ip},{port},{country},{org_name}"
            print(f"CF PROXY LIVE!: {proxy_entry}")
            active_proxies.append(proxy_entry)
        else:
            print(f"CF PROXY DEAD!: {ip}:{port}")
    except Exception as e:
        print(f"Error saat memproses proxy {proxy_line}: {e}")

def run_proxy_check():
    global active_proxies
    active_proxies = []

    if not os.path.exists(PROXY_FILE):
        print(f"File tidak ditemukan: {PROXY_FILE}")
        return

    open(OUTPUT_FILE, "w").close()

    with open(PROXY_FILE, "r") as f:
        proxies = f.readlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(process_proxy, proxy) for proxy in proxies]
        concurrent.futures.wait(futures)

    if active_proxies:
        with open(OUTPUT_FILE, "w") as f_out:
            f_out.write("\n".join(active_proxies) + "\n")
