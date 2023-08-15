import requests
import json


PROXY_URL = "https://proxylist.geonode.com/api/proxy-list?limit=500&sort_by=lastChecked&sort_type=desc&page="
LIMIT = 500

r = requests.get(PROXY_URL)
if r.status_code - 200:
    print(f"ERROR: cannot create connection to proxy_list by href {PROXY_URL}")
    exit()

total_proxies = int(json.loads(r.text)['total'])
print(f'total proxies is {total_proxies}\n')

num_of_pages = total_proxies // LIMIT + 1
num_of_pages = 1

proxy_list = dict()
proxy_list['data'] = []

for numpage in range(1, num_of_pages + 1):
    print(f'processing {numpage} page of {num_of_pages}')

    r = requests.get(PROXY_URL + str(numpage))
    if r.status_code != 200:
        print(f"ERROR: cannot create connection to proxy_list by href {r.url}")
        exit()
    
    proxy_list['data'].extend(json.loads(r.text)['data'])
    
with open("rc/proxylist.json", 'w', encoding="utf-8") as proxyfile:
    proxyfile.write(json.dumps(proxy_list, indent=2))  # для экономии места можно indent убрать