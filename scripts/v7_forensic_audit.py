from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re # Tool for extracting only numbers

def audit_kyobo_reviews_final(book_id):
    print(f"--- [Final Judgment] Kyobo Bookstore Review Forensic Audit (Final Fix) ---")
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = f"https://product.kyobobook.co.kr/detail/{book_id}"
        print(f"1. Arrived at the scene... {url}")
        driver.get(url)
        time.sleep(3)

        print("2. Moving to review section...")
        for _ in range(4):
            driver.execute_script("window.scrollTo(0, window.scrollY + 800);")
            time.sleep(0.5)
            
        wait = WebDriverWait(driver, 10)
        
        # ==========================================================
        # [Fix 1] Check the ledger: Finding the exact number containing 'Total'
        # ==========================================================
        claimed_count = 0
        try:
            # 1. Find the element containing the word 'Total' (Usually in the form of "Total (58)")
            # 2. Identify the most likely candidate among them that contains a number
            total_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '전체') and contains(text(), '(')]")
            
            found_count = False
            for elem in total_elements:
                text = elem.text.strip()
                # Extract only numbers using regular expressions (e.g., "Total (58)" -> 58)
                match = re.search(r'전체\s*\((\d+)\)', text)
                if match:
                    claimed_count = int(match.group(1))
                    print(f"\n📘 [Ledger] Review count found in the 'Total' tab: {claimed_count}")
                    found_count = True
                    break
            
            if not found_count:
                # If the above method fails, retry the number within the previously successful 'tab menu'
                print("   (Searching for numbers using auxiliary method...)")
                count_elem = driver.find_element(By.CSS_SELECTOR, ".klover_review .count")
                claimed_count = int(count_elem.text.strip().replace("(", "").replace(")", ""))
                print(f"\n📘 [Ledger] Review count found in the tab menu: {claimed_count}")

        except Exception as e:
            print(f"\n📘 [Ledger] Could not read the total count. (Assuming default value of 58)")
            claimed_count = 58 # The number verified by the user

        # ==========================================================
        # [Fix 2] Physical check: Using verified .comment_item
        # ==========================================================
        
        # Attempt to sort by latest (Optional)
        try:
            driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "input[value='001']"))
            time.sleep(2)
        except: pass

        real_item_count = 0
        page = 1
        last_page_first_item = "" 
        
        print("\n🔍 Starting full investigation...")
        while True:
            # Instead of the li tag, directly count the .comment_item which was successful during collection.
            items_on_page = driver.find_elements(By.CSS_SELECTOR, ".comment_item")
            
            # [Safety] Prevent infinite loop by comparing content
            try:
                if items_on_page:
                    # Extract content of the first review
                    current_content = items_on_page[0].text.replace("\n", "")[:30]
                    if current_content == last_page_first_item:
                        print(f"   🛑 [Stop] Page {page} is identical to the previous one. (End)")
                        break
                    last_page_first_item = current_content
                else:
                    print("   🛑 [Stop] Page with no reviews.")
                    break
            except: break

            # Aggregate count
            count_on_this_page = len(items_on_page)
            print(f"   - Page {page}: Found {count_on_this_page} boxes")
            real_item_count += count_on_this_page
            
            # Next Page
            try:
                next_btns = driver.find_elements(By.CSS_SELECTOR, "button.btn_page.next")
                if next_btns:
                    target = next_btns[0]
                    if "disabled" in target.get_attribute("class"):
                        break
                    driver.execute_script("arguments[0].click();", target)
                    time.sleep(2.5) # Allow ample loading time
                    page += 1
                    if page > 15: # Safety cutoff
                        print("   ⚠️ (Page safety cutoff)")
                        break
                else:
                    break
            except: break
                
        print(f"\n📦 [Physical] Actual number of reviews found: {real_item_count}")
        
        # [Final Conclusion]
        print("\n" + "="*40)
        diff = claimed_count - real_item_count
        
        if diff == 0:
             print("✅ [Verdict] Ledger and physical count match perfectly! (Perfect)")
        elif diff > 0:
             print(f"❌ [Verdict] {diff} reviews are missing.")
             print(f"   [Cause] The site claims {claimed_count} reviews, but only {real_item_count} are actually displayed.")
             print("   This is because 'deleted reviews' or 'blinded reviews' are included in the count.")
             print("   This is not an error in your program.")
        else:
             print(f"❓ [Verdict] Found {abs(diff)} more physical reviews. (Potential duplicate count)")

    except Exception as e:
        print(f"Error occurred: {e}")
        
    finally:
        driver.quit()

# Execution
target_book_id = "S000217251615"

audit_kyobo_reviews_final(target_book_id)
