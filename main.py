import requests
import xlwt

hasMore = True
offset = 0
store_urls = []
result = []
section_id = 1
headers = {
    "apikey": "A045608F-898F-44A7-A5FB-F54A7C1930E2",
    "location": "6F0EA99C-1CEA-4E93-967B-98D97C5A2912",
    "pricelist": "9D51AB88-A56E-4F7E-A6BE-16854A976FAE",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

response = requests.get("https://partnersapi.gethomesome.com/product/list?shortList=true", headers=headers, json={})
data = response.json()

