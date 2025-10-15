import sys
from functools import partial
print = partial(print, flush=True)

import requests
from bs4 import BeautifulSoup
import time
import logging
from http.client import HTTPConnection
from itertools import cycle

# --- Ücretsiz Proxy Listesi Çekme Bölümü (Değişiklik yok) ---
def get_free_proxies():
    """sslproxies.org'dan ücretsiz proxy listesi çeker."""
    url = "https://www.sslproxies.org/"
    try:
        print("-> Güncel proxy listesi alınıyor...")
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.text, "lxml")
        proxies = []
        # Tablodaki satırları bul (ilk satır başlık olduğu için atla)
        for row in soup.find("table", attrs={"class": "table"}).find_all("tr")[1:]:
            tds = row.find_all("td")
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            # Sadece HTTPS destekleyenleri (yes) alalım
            if 'yes' in tds[6].text.strip().lower():
                proxies.append(f"http://{ip}:{port}")
        
        print(f"-> {len(proxies)} adet potansiyel proxy bulundu.")
        return proxies
    except Exception as e:
        print(f"-> Proxy listesi alınırken hata oluştu: {e}")
        return []

# --- ANA FONKSİYON (MANTIK DEĞİŞİKLİĞİ İLE) ---
def find_current_domain():
    base_url = "https://www.inattvizle{}.top/"
    start_number = 265
    max_attempts = 120
    timeout_sec = 10

    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"),
        "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                   "image/avif,image/webp,*/*;q=0.8"),
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }

    sep = "=" * 50
    print(sep); print("INAT TV GUNCEL DOMAIN BULUCU (Proxy ile)"); print(sep)

    proxies = get_free_proxies()
    if not proxies:
        print("-> Hiç proxy bulunamadı. İşlem durduruluyor.")
        return None
    
    proxy_pool = cycle(proxies)

    for i in range(start_number, start_number + max_attempts):
        url = base_url.format(i)
        attempt = i - start_number + 1
        print(f"[{attempt}/{max_attempts}] Deneniyor: {url}")

        # Her domain için proxy listesini bir kez dönmeyi dene
        for _ in range(len(proxies)):
            proxy = next(proxy_pool)
            print(f"    -> Proxy ile deneniyor: {proxy}")
            
            proxy_dict = {"http": proxy, "https": proxy}
            
            try:
                r = requests.get(url, headers=headers, proxies=proxy_dict, timeout=timeout_sec, allow_redirects=True)
                sc = r.status_code
                final_url = r.url
                print(f"    -> GET status: {sc}")

                # =================================================================== #
                #                       >>> YENİ MANTIK <<<                         #
                # =================================================================== #

                # ÖNCELİK 1: Yönlendirme var mı? Varsa, durum kodu ne olursa olsun hedefi bulduk demektir.
                if final_url != url:
                    print(f"    -> Yönlendirme algılandı: {final_url}")
                    try:
                        with open("inat.txt", "w", encoding="utf-8") as f:
                            f.write(final_url)
                        print("    -> Yönlendirilen adres kaydedildi: inat.txt")
                    except Exception as efile:
                        print(f"    -> Dosyaya yazma hatası: {efile}")
                    
                    print(f"BASARILI! Guncel domain: {final_url}")
                    return final_url # <<<--- İşlemi başarıyla bitir.

                # ÖNCELİK 2: Yönlendirme yoksa, durum kodunu kontrol et.
                if sc == 200:
                    to_write = url
                    try:
                        with open("inat.txt", "w", encoding="utf-8") as f:
                            f.write(to_write)
                        print("    -> Doğrudan adres kaydedildi: inat.txt")
                    except Exception as efile:
                        print(f"    -> Dosyaya yazma hatası: {efile}")

                    print(f"BASARILI! Guncel domain: {to_write}")
                    return to_write # <<<--- İşlemi başarıyla bitir.

                # BAŞARISIZLIK DURUMLARI: Yönlendirme yok ve durum kodu iyi değil.
                if sc in (403, 407):
                     print("    -> Proxy engellenmiş veya hatalı (403/407). Diğer proxy'e geçiliyor.")
                     continue # Sonraki proxy'i dene
                else:
                    # Domain çalışmıyor olabilir (404 vb.), aynı proxy ile sonraki domaini deneyelim.
                    break 

            except requests.exceptions.ProxyError:
                print("    -> Proxy hatası. Başka bir proxy deneniyor...")
            except requests.exceptions.Timeout:
                print("    -> Zaman aşımı (Timeout). Bir sonraki denemeye geçiliyor...")
                break
            except requests.exceptions.RequestException as e:
                print(f"    -> Genel istek hatası: {type(e).__name__}. Başka bir proxy deneniyor...")
            
        print("")

    print(sep)
    print("BASARISIZ: aralikta uygun domain bulunamadi.")
    print(sep)
    return None

if __name__ == "__main__":
    res = find_current_domain()
    if res:
        print(f"Guncel domain: {res}")
    else:
        print("Bulunamadi")
