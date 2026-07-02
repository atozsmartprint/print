import time
import os
import requests
import gdown
import shutil  # यह टूल फाइल की डुप्लीकेट कॉपी बनाएगा
from docx2pdf import convert

API_URL = "https://script.google.com/macros/s/AKfycbxWoAL9yvBcDOhcz2TzoVR2PyR7ayZ-2wFQPXWXtVuyepa_mp4Tj_7HSprOfhnbOYWE/exec"
SAVE_DIR = r"C:\PrintJobs"
LOG_FILE = "printed_history.txt"

if not os.path.exists(SAVE_DIR): os.makedirs(SAVE_DIR)
os.chdir(SAVE_DIR)

printed_orders = set()
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        for line in f:
            printed_orders.add(line.strip())

print("🖨️ A To Z Solution - Multi-Copy Smart Server Active...")
print(f"🧠 Old orders remembered: {len(printed_orders)}. Ready for new jobs!")

while True:
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            orders = response.json()
            for order in orders:
                order_id = str(order.get('orderId', ''))
                full_service = str(order.get('service', '')).upper()
                file_url = order.get('fileUrl', '')
                
                if order_id and order_id not in printed_orders:
                    
                    # कॉपी की संख्या निकालना
                    copies = 1
                    service = full_service
                    if "_X" in full_service:
                        parts = full_service.split("_X")
                        service = parts[0]
                        try:
                            copies = int(parts[1])
                        except:
                            copies = 1
                            
                    print(f"\n📥 New Order: {order_id} [{service}] - Copies Required: {copies}")
                    
                    ext = ".pdf"
                    if "WORD" in service or "word" in file_url.lower() or "document" in file_url.lower(): 
                        if not file_url.endswith('.pdf'):
                            ext = ".docx"
                    if "PHOTO" in service: 
                        ext = ".jpg"
                    
                    file_name = f"order_{order_id}{ext}"
                    
                    gdown.download(file_url, file_name, quiet=True)
                    time.sleep(2) 
                    
                    if os.path.exists(file_name):
                        if "PHOTO" in service:
                            print(f"📸 Photo Saved. (Customer needs {copies} copies)")
                            
                        elif file_name.endswith(".docx"):
                            print("🔄 Converting Word to PDF...")
                            pdf_name = file_name.replace(".docx", ".pdf")
                            convert(file_name, pdf_name)
                            print(f"🖨️ Printing Word (as PDF) - {copies} times...")
                            
                            # यहाँ है नया जुगाड़ (कॉपी बनाकर प्रिंट करना)
                            for i in range(copies):
                                temp_copy = f"temp_print_{i}_{pdf_name}"
                                shutil.copy(pdf_name, temp_copy) # नई फाइल बनाई
                                os.startfile(temp_copy, "print") # उसे प्रिंट किया
                                time.sleep(4) # प्रिंटर को पेज खींचने का समय दिया
                                
                        else:
                            print(f"🖨️ Printing {service} - {copies} times...")
                            
                            # यहाँ भी वही नया जुगाड़
                            for i in range(copies):
                                temp_copy = f"temp_print_{i}_{file_name}"
                                shutil.copy(file_name, temp_copy) # नई फाइल बनाई
                                os.startfile(temp_copy, "print") # उसे प्रिंट किया
                                time.sleep(4) # 4 सेकंड का गैप दिया ताकि मशीन हैंग न हो
                                
                        printed_orders.add(order_id)
                        with open(LOG_FILE, "a") as f:
                            f.write(order_id + "\n")
                            
    except Exception as e:
        pass
    time.sleep(8)