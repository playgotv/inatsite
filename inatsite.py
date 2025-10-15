import sys
from functools import partial
print = partial(print, flush=True)  # tum print'ler aninda yazsin [web:121][web:115]

import requests
import time
import logging
from http.client import HTTPConnection  # py3

# HTTP debug (istege bagli ayrintili log)
def enable_http_debug():
    HTTPConnection.debuglevel = 1  # alt seviye HTTP loglari [web:132]
    logging.basicConfig(level=logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True  # loglari konsola akit [web:132][web:37]

def find_current_domain():
    base_url = "https://www.inattvizle{}.top/"
    start_number = 265
    max_attempts = 120
    timeout_sec = 8

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
        "Pragma": "no-cache",
        "Referer": "https://www.google.com/"
    }

    sep = "=" * 50
    print(sep); print("INAT TV GUNCEL DOMAIN BULUCU (Pydroid net cikti)"); print(sep)

    s = requests.Session()
    s.headers.update(headers)

    for i in range(start_number, start_number + max_attempts):
        url = base_url.format(i)
        attempt = i - start_number + 1
        print("[" + str(attempt) + "/" + str(max_attempts) + "] Deneniyor: " + url)

        try:
            # HEAD (opsiyonel hizli kontrol)
            head_ok = False
            try:
                h = s.head(url, timeout=timeout_sec, allow_redirects=True)
                print("    -> HEAD status: " + str(h.status_code))
                head_ok = h.status_code in (200, 301, 302)
            except Exception as ehead:
                print("    -> HEAD hata: " + str(ehead))

            # GET
            r = s.get(url, timeout=timeout_sec, allow_redirects=True)
            sc = r.status_code
            final_url = r.url
            print("    -> GET status: " + str(sc))
            if final_url != url:
                print("    -> Yonlendirme: " + final_url)

            if sc in (200, 301, 302) or head_ok:
                to_write = final_url if sc in (301, 302) else url
                try:
                    with open("inat.txt", "w", encoding="utf-8") as f:
                        f.write(to_write)
                    print("    -> Kaydedildi: inat.txt")
                except Exception as efile:
                    print("    -> Dosyaya yazma hatasi: " + str(efile))
                print("BASARILI! Guncel domain: " + to_write)
                return to_write  # bulur bulmaz bitir

            if sc == 403:
                print("    -> 403 alindi, tekrar denenecek...")
                time.sleep(1.0)
                r2 = s.get(url, timeout=timeout_sec, allow_redirects=True)
                print("    -> GET(tekrar) status: " + str(r2.status_code))
                if r2.status_code in (200, 301, 302):
                    try:
                        with open("inat.txt", "w", encoding="utf-8") as f:
                            f.write(r2.url)
                        print("    -> Kaydedildi: inat.txt")
                    except Exception as efile2:
                        print("    -> Dosyaya yazma hatasi: " + str(efile2))
                    print("BASARILI! Guncel domain: " + r2.url)
                    return r2.url

        except requests.exceptions.Timeout:
            print("    -> Zaman asimi (Timeout)")
        except requests.exceptions.ConnectionError:
            print("    -> Baglanti hatasi")
        except Exception as e:
            print("    -> Hata: " + str(e))

        time.sleep(0.2)
        print("")  # satir sonu tamponu bosaltsin

    print(sep)
    print("BASARISIZ: aralikta uygun domain bulunamadi.")
    print(sep)
    return None

if __name__ == "__main__":
    # İsterseniz HTTP ayrıntılı log açın:
    # enable_http_debug()  # gerektiginde aktif edin [web:132][web:37]
    res = find_current_domain()
    if res:
        print("Guncel domain: " + res)
    else:
        print("Bulunamadi")            r = s.get(url, timeout=timeout_sec, allow_redirects=True)
            sc = r.status_code
            final_url = r.url

            if sc in (200, 301, 302) or head_ok:
                to_write = final_url if sc in (301, 302) else url
                with open("inat.txt", "w", encoding="utf-8") as f:
                    f.write(to_write)
                return to_write

            if sc == 403:
                # iki ek deneme, arada bekleme
                for _ in range(2):
                    time.sleep(1.0)
                    r2 = s.get(url, timeout=timeout_sec, allow_redirects=True)
                    if r2.status_code in (200, 301, 302):
                        with open("inat.txt", "w", encoding="utf-8") as f:
                            f.write(r2.url)
                        return r2.url

        except Exception:
            pass

        time.sleep(1.0)

    return None

if __name__ == "__main__":
    res = find_current_domain()
    print("Guncel domain: " + res if res else "Bulunamadi")        try:
            head_ok = False
            try:
                h = s.head(url, timeout=timeout_sec, allow_redirects=True)
                log("    -> HEAD status: " + str(h.status_code))
                head_ok = h.status_code in (200, 301, 302)
            except Exception as ehead:
                log("    -> HEAD hata: " + str(ehead))

            r = s.get(url, timeout=timeout_sec, allow_redirects=True)
            sc = r.status_code
            final_url = r.url
            log("    -> GET status: " + str(sc))
            if final_url != url:
                log("    -> Yonlendirme: " + final_url)

            if sc in (200, 301, 302) or head_ok:
                to_write = final_url if sc in (301, 302) else url
                try:
                    with open("inat.txt", "w", encoding="utf-8") as f:
                        f.write(to_write)
                    log("    -> Kaydedildi: inat.txt")
                except Exception as efile:
                    log("    -> Dosyaya yazma hatasi: " + str(efile))
                log("BASARILI! Guncel domain: " + to_write)
                return to_write  # Bulur bulmaz fonksiyondan çık

            if sc == 403:
                log("    -> 403 alindi, tekrar denenecek...")
                time.sleep(1.0)
                r2 = s.get(url, timeout=timeout_sec, allow_redirects=True)
                log("    -> GET(tekrar) status: " + str(r2.status_code))
                if r2.status_code in (200, 301, 302):
                    try:
                        with open("inat.txt", "w", encoding="utf-8") as f:
                            f.write(r2.url)
                        log("    -> Kaydedildi: inat.txt")
                    except Exception as efile2:
                        log("    -> Dosyaya yazma hatasi: " + str(efile2))
                    log("BASARILI! Guncel domain: " + r2.url)
                    return r2.url  # Bulur bulmaz çık

        except requests.exceptions.Timeout:
            log("    -> Zaman asimi (Timeout)")
        except requests.exceptions.ConnectionError:
            log("    -> Baglanti hatasi")
        except Exception as e:
            log("    -> Hata: " + str(e))

        time.sleep(0.2)
        log("")

    log("BASARISIZ: aralikta uygun domain bulunamadi.")
    return None

if __name__ == "__main__":
    res = find_current_domain()
    # input(...) satırı tamamen kaldırıldı; script sonuçtan sonra otomatik biter [web:23][web:34].
