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

def get_kyobo_reviews_complete(book_id, max_pages=5):
    print(f"--- [Kyobo Bookstore] Final Collection Mission Started (Book ID: {book_id}) ---")
    
    # 1. Browser Configuration (Visible mode enabled for observation)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080") # Large screen
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    all_reviews = []
    
    try:
        # Access book page
        url = f"https://product.kyobobook.co.kr/detail/{book_id}"
        print(f"1. Connecting to page... {url}")
        driver.get(url)
        time.sleep(3)

        # 2. Scroll down to the review section
        print("2. Searching for review section...")
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, window.scrollY + 1000);")
            time.sleep(1)
            
        # Wait for review list to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".comment_list"))
            )
            print("   >> Review list found!")
        except:
            print("   >> Loading is taking a while? Scrolling once more!")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        # 3. Collect data while navigating through pages
        for page in range(1, max_pages + 1):
            print(f"--- Collecting Page {page} ---")
            
            # Capture the entire HTML of the current page
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # [Core] Find boxes according to the established HTML structure (.comment_item)
            review_items = soup.select(".comment_item")
            
            print(f"   Found {len(review_items)} reviews")
            
            if not review_items:
                print("   No reviews found. Loading failed or reached the end.")
                time.sleep(2)
                continue

            for item in review_items:
                try:
                    # 1) Extract content (Replace newlines with spaces)
                    content = item.select_one(".comment_text").get_text(" ", strip=True)
                    
                    # 2) Extract rating (Value from the input tag)
                    # Based on structure: <input class="... rating-input" value="2.5">
                    rating = item.select_one(".rating-input")['value']
                    
                    # 3) Writer and Date (Grouped in info_items)
                    # First is the ID, second is the date
                    info_items = item.select(".user_info_box .info_item")
                    writer = info_items[0].text.strip() if len(info_items) > 0 else "Anonymous"
                    date = info_items[1].text.strip() if len(info_items) > 1 else "No Date"
                    
                    # 4) Number of likes
                    likes = item.select_one(".btn_like .text").text.strip() if item.select_one(".btn_like .text") else "0"

                    # Save data
                    all_reviews.append({
                        'Page': page,
                        'Writer': writer,
                        'Date': date,
                        'Rating': rating,
                        'Likes': likes,
                        'Content': content
                    })
                    
                except Exception as e:
                    # If any extraction fails, skip and continue
                    continue

            # Click [Next Page] button
            if page < max_pages:
                try:
                    # Find next page button (btn_page next)
                    next_btns = driver.find_elements(By.CSS_SELECTOR, "button.btn_page.next")
                    if next_btns:
                        target_btn = next_btns[0]
                        
                        # If the button is disabled, the process is finished
                        if "disabled" in target_btn.get_attribute("class"):
                            print("   No more pages available. (End)")
                            break
                        
                        # Force click via JavaScript (Most reliable)
                        driver.execute_script("arguments[0].click();", target_btn)
                        print("   [>] Moving to next page")
                        time.sleep(3) # Give time for loading
                    else:
                        print("   Next button not visible.")
                        break
                except Exception as e:
                    print(f"   Failed to navigate to next page: {e}")
                    break

    except Exception as e:
        print(f"Error occurred: {e}")
        
    finally:
        print("Closing browser.")
        driver.quit()
        
    return pd.DataFrame(all_reviews)

# --- Execution ---
# ID of the book for analysis (e.g., Alex Karp's book)
target_book_id = "S000217251615" 

# Setting to 10 pages for a generous collection (100 reviews)
df = get_kyobo_reviews_complete(target_book_id, max_pages=10)

if not df.empty:
    print(f"\n[Success!] Collected a total of {len(df)} reviews.")
    
    # Filtering for translation/sentence complaints
    keywords = ['번역', '직역', '문장', '오역', '이해', '가독성', '읽기']
    issues = df[df['Content'].apply(lambda x: any(k in x for k in keywords))]
    
    print(f"Reviews mentioning translation issues: {len(issues)} cases")
    print(issues[['Rating', 'Content']].head()) # Show a short preview
    
    # Save to Excel
    filename = "palantir_book_reviews_final.xlsx"
    df.to_excel(filename, index=False)
    print(f"\nFile saved: {filename}")
else:
    print("\nNo data collected.")