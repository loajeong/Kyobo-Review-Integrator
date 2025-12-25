import requests
import pandas as pd
import time
import random
import json

def get_kyobo_reviews_final(book_id, max_pages=10):
    print(f"--- [Kyobo Bookstore] Data Collection Started (Book ID: {book_id}) ---")
    
    # [Core 1] Start Session: The 's' object will now remember cookies.
    s = requests.Session()
    
    base_url = "https://product.kyobobook.co.kr/api/review/list"
    detail_url = f"https://product.kyobobook.co.kr/detail/{book_id}"
    
    # Advanced Camouflage (Add Headers)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': "https://product.kyobobook.co.kr/",
        'Accept': 'application/json, text/plain, */*', # Explicitly stating readiness to receive JSON data
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    # [Core 2] Visit the book detail page first to acquire cookies
    print("1. Acquiring session cookies...")
    try:
        s.get(detail_url, headers=headers) 
    except Exception as e:
        print(f"Problem occurred during the connection phase: {e}")
        return pd.DataFrame()

    all_reviews = []

    print("2. Starting review data collection!")
    for page in range(1, max_pages + 1):
        params = {
            'page': page,
            'pageLimit': 100,
            'reviewSort': '001',
            'revType': 'buy',
            'saleCmdtid': book_id
        }

        try:
            # Using s.get instead of requests.get (Use Session)
            response = s.get(base_url, headers=headers, params=params)
            
            # [Debugging] Check what the server sent (Helpful for identifying the cause if an error occurs)
            # If response.text starts with '<html...', it means the request was blocked.
            if response.text.strip().startswith('<'):
                print(f"!! The server sent a webpage (HTML) instead of data. (Block or URL error)")
                print(f"Partial server response: {response.text[:100]}")
                break

            # Attempt JSON conversion
            data = response.json()
            
            # Check Kyobo Bookstore response structure
            reviews = data.get('data', {}).get('reviewList', [])
            
            if not reviews:
                print(f"Page {page}: Collection finished (No reviews)")
                break
            
            print(f"Page {page}: Successfully collected {len(reviews)} reviews")
            
            for review in reviews:
                extracted = {
                    'Bookstore': 'Kyobo',
                    'Date': review.get('createdDate', '')[:10],
                    'Writer': review.get('mmbrId', 'Anonymous'),
                    'Rating': review.get('revwRating', 0),
                    'Content': review.get('revwCntn', '').replace('\n', ' '),
                    'Likes': review.get('recmCnt', 0)
                }
                all_reviews.append(extracted)

            time.sleep(random.uniform(1, 2)) # Slowly

        except json.JSONDecodeError:
            print(f"!! Error: The server sent abnormal data. (Not JSON)")
            print(f"Content Preview: {response.text[:200]}")
            break
        except Exception as e:
            print(f"!! Unknown error: {e}")
            break
            
    return pd.DataFrame(all_reviews)

# --- Execution ---
target_book_id = "S000217251615" # Verification of Alex Karp's book ID is required!

df = get_kyobo_reviews_final(target_book_id, max_pages=3)

if not df.empty:
    print(f"\nCollected a total of {len(df)} reviews!")
    # Filtering for translation-related issues
    issues = df[df['Content'].str.contains('번역|직역|문장|이해|어려', na=False)]
    print(f"Reviews suspected of translation complaints: {len(issues)}")
    
    df.to_excel(f"kyobo_{target_book_id}.xlsx", index=False)
    print("File storage completed.")
else:
    print("\nCollection failed. Check if the Book ID is correct or if you are connected to the internet.")