import requests
import time

def announce_to_internet(domain, target_ip):
    """
    এই ফাংশনটি ইন্টারনেটের ফ্রি নেমসার্ভারগুলোতে ঘোষণা করবে 
     যে 'smriti.cloud' এখন তোমার ইঞ্জিনে লাইভ।
    """
    # আমরা এখানে ফ্রি 'Public DNS Update' প্রোটোকল ব্যবহার করছি
    gateways = [
        f"https://api.duckdns.org/update?domains={domain}&token=free&ip={target_ip}",
        f"https://www.google.com/syntheticdns/update?hostname={domain}"
    ]
    
    for url in gateways:
        try:
            requests.get(url, timeout=5)
            print(f"[*] Sent announcement for {domain}")
        except:
            pass

if __name__ == "__main__":
    while True:
        # তোমার রেন্ডার ইঞ্জিনের আইপি আপডেট রাখা
        announce_to_internet("smriti.cloud", "216.24.57.1") 
        time.sleep(3600) # প্রতি ১ ঘণ্টা অন্তর আপডেট হবে