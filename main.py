from fastapi import FastAPI
import os
from script.proxy_checker import run_proxy_check

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Proxy Checker API is running"}

@app.get("/proxies/alive")
def get_alive_proxies():
    if os.path.exists("Data/alive.txt"):
        with open("Data/alive.txt", "r") as file:
            proxies = [line.strip() for line in file.readlines() if line.strip()]
        return {"proxies": proxies}
    return {"proxies": []}

@app.post("/proxies/check")
def check_proxies():
    run_proxy_check()
    return {"message": "Proxy check selesai"}
