import sys
from functools import partial
print = partial(print, flush=True)

import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_free_proxies():
    """sslproxies.org'dan ücretsiz proxy listesi çeker."""
    url = "https://www.sslproxies.org/"
    try:
        print("-> Güncel proxy listesi alınıyor...")
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.text, "lxml")
        proxies = []
        for row in soup.find("table", attrs={"class": "table"}).find_all("tr")[1:]:
            tds = row.find_all("td")
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            if 'yes' in tds[6].text.strip().lower():
                proxies.append(f"http://{ip}:{port}")
        print(f"-> {len(proxies)} adet potansiyel proxy bulundu.")
        return proxies
    except Exception as e:
        print(f"-> Proxy listesi alınırken hata oluştu: {e}")
        return []

def check_domain(url, proxy, headers, timeout):
    """Belirli bir domaini belirli bir proxy ile kontrol eder."""
    try:
        proxy_dict = {"http": proxy, "https": proxy}
        r = requests.get(url, headers=headers, proxies=proxy_dict, timeout=timeout, allow_redirects=True)
        
        # Öncelik 1: Yönlendirme varsa, bu bizim cevabımızdır.
        if r.url != url:
            print(f"    [BAŞARILI] Yönlendirme bulundu: {r.url} (Proxy: {proxy})")
            return r.url
        
        # Öncelik 2: Yönlendirme yok ama sayfa direkt çalışıyorsa (200 OK).
        if r.status_code == 200:
            print(f"    [BAŞARILI] Doğrudan adres bulundu: {url} (Proxy: {proxy})")
            return url
            
    except requests.RequestException:
        # Proxy veya bağlantı hataları normaldir, sessizce geç.
        pass
    return None

def find_current_domain():
    base_url = "https://www.inattvizle{}.top/"
    start_number = 265
    max_attempts = 120
    timeout_sec = 8
    MAX_WORKERS = 100 # Aynı anda çalışacak işlem sayısı

    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36")
    }

    sep = "=" * 50
    print(sep); print("INAT TV GUNCEL DOMAIN BULUCU (Hızlı Paralel Tarama)"); print(sep)

    proxies = get_free_proxies()
    if not proxies:
        print("-> Hiç proxy bulunamadı. İşlem durduruluyor.")
        return None

    tasks = []
    # Denenecek tüm domain ve proxy kombinasyonlarını bir liste yap
    for i in range(start_number, start_number + max_attempts):
        url = base_url.format(i)
        for proxy in proxies:
            tasks.append((url, proxy))
    
    print(f"-> Toplam {len(tasks)} görev oluşturuldu. Paralel tarama başlıyor...")

    # ThreadPoolExecutor ile görevleri paralel olarak çalıştır
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # submit ile her bir görevi havuza gönder
        future_to_task = {executor.submit(check_domain, task[0], task[1], headers, timeout_sec): task for task in tasks}
        
        # as_completed ile görevler tamamlandıkça sonuçları al
        for future in as_completed(future_to_task):
            result = future.result()
            if result:
                # Başarılı bir sonuç bulunur bulunmaz, diğer tüm bekleyen görevleri iptal et ve sonucu dön
                print("-> Sonuç bulundu, diğer tüm işlemler durduruluyor...")
                executor.shutdown(wait=False, cancel_futures=True)
                return result

    print(sep)
    print("BASARISIZ: aralıkta uygun domain bulunamadi.")
    print(sep)
    return None

if __name__ == "__main__":
    start_time = time.time()
    res = find_current_domain()
    
    if res:
        try:
            with open("inat.txt", "w", encoding="utf-8") as f:
                f.write(res)
            print("-> Kaydedildi: inat.txt")
        except Exception as e:
            print(f"-> Dosyaya yazma hatası: {e}")
        
        print(f"\nBASARILI! Guncel domain: {res}")
    else:
        print("\nBulunamadi")
        
    end_time = time.time()
    print(f"-> Toplam süre: {end_time - start_time:.2f} saniye")
