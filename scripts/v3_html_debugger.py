from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

def debug_kyobo_html(book_id):
    print(f"--- [Kyobo Bookstore] Magnifying Glass Mode Started (Book ID: {book_id}) ---")
    
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Commented out to see the window opening
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = f"https://product.kyobobook.co.kr/detail/{book_id}"
        print(f"1. Connecting... {url}")
        driver.get(url)
        time.sleep(4) 

        print("2. Scrolling down...")
        driver.execute_script("window.scrollTo(0, window.scrollY + 1000);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, window.scrollY + 1000);")
        time.sleep(2)
        
        # Wait for review section loading
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".review_list_wrap")))
        except:
            print("Failed to wait for review section loading (proceeding anyway)")

        # Get HTML
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find review boxes
        review_items = soup.select(".comment_item")
        print(f"\n>>> Found {len(review_items)} review boxes")
        
        if len(review_items) > 0:
            print("\n★★★ Revealing the internal structure (HTML) of the first review! ★★★\n")
            print("=" * 50)
            
            # Pretty print the HTML of the first review
            first_item = review_items[0]
            print(first_item.prettify()) 
            
            print("=" * 50)
            print("\n▲ Copy and share the content above!")
        else:
            print("Could not find review boxes (.comment_item). The overall page structure might have changed.")
            # Print part of the full HTML just in case
            # print(soup.prettify()[:1000]) 

    except Exception as e:
        print(f"Error occurred: {e}")
        
    finally:
        driver.quit()

# Execution
target_book_id = "S000217251615"
debug_kyobo_html(target_book_id)