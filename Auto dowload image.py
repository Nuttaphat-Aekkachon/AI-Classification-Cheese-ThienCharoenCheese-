from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
from PIL import Image
from io import BytesIO

# ฟังก์ชันสำหรับดาวน์โหลดภาพ
def download_images_selenium(query, num_images, save_folder):
    # ตรวจสอบและสร้างโฟลเดอร์ถ้าไม่มี
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # ตั้งค่า ChromeDriver ในโหมด headless
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # เปิดหน้า Google Images ด้วย query ที่ต้องการ
    driver.get(f"https://www.google.com/search?hl=en&tbm=isch&q={query}")
    time.sleep(2)
    
    downloaded = 0
    print(f"เริ่มดาวน์โหลดรูปภาพ {query} จำนวน {num_images} รูป...")

    # เลื่อนหน้าเพื่อโหลดภาพเพิ่มเติม
    while downloaded < num_images:
        driver.find_element('tag name', 'body').send_keys(Keys.END)
        time.sleep(2)

        image_elements = driver.find_elements('css selector', 'img')
        
        for img_element in image_elements[downloaded:num_images]:
            if downloaded >= num_images:
                break
            try:
                img_url = img_element.get_attribute('src')
                if img_url and img_url.startswith('http'):
                    # เพิ่มการตั้งค่าขีดจำกัดเวลาให้กับ requests.get
                    img_data = requests.get(img_url, timeout=10).content
                    img = Image.open(BytesIO(img_data))
                    img.save(f"{save_folder}/{query}_{downloaded}.jpg")
                    downloaded += 1
                    print(f"ดาวน์โหลดสำเร็จ: รูปที่ {downloaded}/{num_images}")
            except Exception as e:
                print(f"ข้อผิดพลาดในการดาวน์โหลด {img_url}: {e}")
                continue  # ข้ามรูปนี้แล้วดาวน์โหลดรูปถัดไป
    
    driver.quit()
    print(f"ดาวน์โหลดรูปภาพ {query} เสร็จสิ้นแล้ว ({downloaded}/{num_images})")

# รายการประเภทของชีสจากคอลัมน์ family
cheese_families = [
    "Cheddar", "Blue", "Brie", "Pecorino", "Gouda", "Parmesan",
    "Camembert", "Feta", "Cottage", "Pasta filata", "Swiss Cheese",
    "Mozzarella", "Tomme", "Monterey Jack", "Caciotta", "Cornish",
    "Raclette", "Italian Cheese", "Havarti", "Saint-Paulin"
]

# ดาวน์โหลดภาพชีสแต่ละประเภท
for family in cheese_families:
    # เปิดและปิด ChromeDriver แยกกันสำหรับแต่ละประเภทของชีส
    download_images_selenium(family + " cheese", 200, f"cheese_images/{family}")
    
    # download_images_selenium(family + " cheese", 200, f"saint-paulin cheese/{family}")
