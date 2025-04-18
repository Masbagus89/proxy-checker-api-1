# Proxy Checker API

API untuk mengecek daftar proxy apakah valid sebagai Cloudflare proxy atau tidak.

## Fitur
- Mengecek IP proxy secara otomatis tiap jam
- Menyimpan hasil ke database
- Endpoint API untuk ambil dan cek manual

## Endpoint
- `GET /proxies/alive` — Ambil semua proxy aktif
- `POST /proxies/check` — Jalankan pengecekan manual

## Deploy
1. Upload ke GitHub
2. Deploy ke Railway
3. Tambahkan file `Data/ProxyIsp.txt` berisi daftar proxy `ip,port,country,org`

## Format Proxy
```
1.2.3.4,443,US,Cloudflare
```
