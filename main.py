import requests
import xlwt
import imghdr
import os
from datetime import datetime

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
titleData = ["id","Store page link", "Product item page link", "Store_name", "Category", "Product_description", "Product Name", "Weight/Quantity", "Units/Counts", "Price", "image_file_names", "Image_Link", "Store Rating", "Store Review number", "Product Rating", "Product Review number", "Address", "Phone number", "Latitude", "Longitude", "Description Detail", "SubCategory"]
widths = [10,50,50,60,45,70,35,25,25,20,130,130,30,30,30,30,60,50,60,60,80,60]
style = xlwt.easyxf('font: bold 1; align: horiz center')

response = requests.get("https://partnersapi.gethomesome.com/product/list?shortList=true", headers=headers, json={})
data = response.json()

products = data["products"]
records = []

if(not os.path.isdir("products")):
    os.mkdir("products")

now = datetime.now()
current_time = now.strftime("%m-%d-%Y-%H-%M-%S")
prefix = now.strftime("%Y%m%d%H%M%S%f_")
os.mkdir("products/"+current_time)
os.mkdir("products/"+current_time+"/images")

for product in products:
    try:
        download_url = ""
        image_url = "https://s3.us-west-2.amazonaws.com/www.gethomesome.com/productimages_tn/" + product["name"] + ".jpg"
        if(product["hasImage"]):
            try:
                responseImage = requests.get(image_url, headers=headers)
                image_type = imghdr.what(None, responseImage.content)
                if responseImage.status_code == 200:
                    img_url = "products/"+current_time+"/images/"+prefix+str(section_id)+'.'+image_type
                    with open(img_url, 'wb') as file:
                        file.write(responseImage.content)
                        download_url = img_url
                # download_url = "products/"+current_time+"/images/"+prefix+str(section_id)+'.'+"jpg"
            except Exception as e:
                print(e)
        record = [
            str(section_id),
            "https://shop.patelbros.com",
            "https://shop.patelbros.com/shop/"+product["type"]+"?subcategory="+product["subType"],
            "Patel Brothers",
            product["type"],
            "",
            product["displayName"],
            product["unitQuantity"],
            product["unit"],
            product["price"],
            download_url,
            image_url,
            "",
            "",
            "",
            "",
            "3428 North University Drive Sunrise, FL 33351",
            "+1(954)742-3004",
            "26.17042574238772",
            "-80.25393490216432",
            "",
            product["subType"]
        ]
        print(record)
        records.append(record)
        section_id = section_id + 1
    except Exception as e:
        print(e)
    
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Sheet1')

for col_index, value in enumerate(titleData):
    first_col = sheet.col(col_index)
    first_col.width = 256 * widths[col_index]  # 20 characters wide
    sheet.write(0, col_index, value, style)
    
for row_index, row in enumerate(records):
    for col_index, value in enumerate(row):
        sheet.write(row_index+1, col_index, value)

# Save the workbook
workbook.save("products/"+current_time+"/products.xls")
