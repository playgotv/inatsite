import requests
import sys
import time

def find_current_domain():
    base_url = "https://www.inattvizle{}.top/"
    start_number = 271
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
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://www.google.com/"
    }

    s = requests.Session()
    s.headers.update(headers)

    for i in range(start_number, start_number + max_attempts):
        url = base_url.format(i)
        sys.stdout.flush()
        try:
            head_ok = False
            try:
                h = s.head(url, timeout=timeout_sec, allow_redirects=True)
                head_ok = h.status_code in (200, 301, 302)
            except Exception:
                pass

            r = s.get(url, timeout=timeout_sec, allow_redirects=True)
            sc = r.status_code
            final_url = r.url

            if sc in (200, 301, 302) or head_ok:
                to_write = final_url if sc in (301, 302) else url
                with open("inat.txt", "w", encoding="utf-8") as f:
                    f.write(to_write)
                return to_write

            if sc == 403:
                time.sleep(1.0)
                r2 = s.get(url, timeout=timeout_sec, allow_redirects=True)
                if r2.status_code in (200, 301, 302):
                    with open("inat.txt", "w", encoding="utf-8") as f:
                        f.write(r2.url)
                    return r2.url

        except Exception:
            pass

        time.sleep(0.2)

    return None

if __name__ == "__main__":
    found = find_current_domain()
    if found:
        print("Guncel domain: " + found)
    else:
        print("Bulunamadi")
