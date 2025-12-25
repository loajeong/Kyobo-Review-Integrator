from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random
from bs4 import BeautifulSoup

def get_kyobo_reviews_ui_mode(book_id, max_pages=5):
    print(f"--- [Kyobo Bookstore] Human Simulation Mode Started (Book ID: {book_id}) ---")
    
    # 1. Configuration for Bot Detection Evasion
    options = webdriver.ChromeOptions()
    # Remove the 'Chrome is being controlled by automated test software' notification
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # Disable GPU acceleration (To prevent errors)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Window size configuration (For responsive web compatibility)
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Execute script to prevent bot detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    all_reviews = []
    
    try:
        # Access book detail page
        url = f"https://product.kyobobook.co.kr/detail/{book_id}"
        print(f"1. Connecting to page... {url}")
        driver.get(url)
        time.sleep(3) # Wait for loading

        # 2. Scroll down until the review section is visible
        print("2. Scrolling to the review section...")
        # Induce data loading by scrolling down incrementally
        for i in range(1, 4):
            driver.execute_script("window.scrollTo(0, window.scrollY + 1000);")
            time.sleep(1)
            
        # Wait for the review tab to load (Max 10 seconds)
        try:
            wait = WebDriverWait(driver, 10)
            # Wait until the element containing the review list appears
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".review_list_wrap")))
            print("   >> Review section found!")
        except:
            print("   >> Warning: Review section not found immediately. Scrolling further down.")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        # 3. Start collection while navigating through pages
        for page in range(1, max_pages + 1):
            print(f"--- Collecting Page {page} ---")
            
            # Get the HTML of the current screen and analyze it with BeautifulSoup (Faster and fewer errors than Selenium)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find review boxes
            review_items = soup.select(".comment_item") # Kyobo review item class
            
            if not review_items:
                print("   Unable to find review items. (Loading delay or end of list)")
                # Wait 2 more seconds and retry just in case
                time.sleep(2)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                review_items = soup.select(".comment_item")

            print(f"   Found {len(review_items)} reviews")
            
            for item in review_items:
                try:
                    content = item.select_one(".comment_contents").text.strip()
                    writer = item.select_one(".user_name").text.strip()
                    date = item.select_one(".date").text.strip()
                    
                    # Store data
                    all_reviews.append({
                        'Page': page,
                        'Writer': writer,
                        'Date': date,
                        'Content': content
                    })
                except AttributeError:
                    continue # Skip if some elements are missing

            # Click [Next Page] button
            if page < max_pages:
                try:
                    # Find 'Next' arrow button (Usually has a class like 'btn_page next')
                    # Selector tailored to Kyobo UI structure (Subject to change)
                    next_button = driver.find_element(By.CSS_SELECTOR, "button.btn_page.next")
                    
                    # Check if the button is disabled
                    if "disabled" in next_button.get_attribute("class"):
                        print("   No more pages. Ending collection.")
                        break
                        
                    # Click! (Clicking via JavaScript is more stable)
                    driver.execute_script("arguments[0].click();", next_button)
                    print("   [>] Next page button clicked successfully")
                    
                    # Give enough time for new data to load (Like a human)
                    time.sleep(3) 
                    
                except Exception as e:
                    print(f"   Next page button not found or reached the end. ({e})")
                    break

    except Exception as e:
        print(f"Critical error occurred: {e}")
        
    finally:
        print("Closing browser.")
        driver.quit()
        
    return pd.DataFrame(all_reviews)

# --- Execution ---
# ID of the book you want to analyze
target_book_id = "S000217251615" 

df = get_kyobo_reviews_ui_mode(target_book_id, max_pages=10)

if not df.empty:
    print(f"\n[Success!] Collected a total of {len(df)} reviews.")
    print(df.head())
    
    # Save to Excel
    df.to_excel(f"kyobo_ui_final_{target_book_id}.xlsx", index=False)
    print("File storage completed.")
else:
    print("\nNo data collected. Please check if reviews appeared on the screen.")