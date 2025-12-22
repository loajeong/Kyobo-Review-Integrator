🚀 Kyobo Review Integrator: A Palantir-Inspired Data Pipeline
"Quantifying Translation Quality: An End-to-End Pipeline for 'The Techno-Republic' Analysis"
This project is a robust data engineering pipeline designed to collect and analyze customer feedback on the Korean translation of The Techno-Republic by Alex Karp (CEO of Palantir). Moving beyond simple web scraping, this project demonstrates advanced techniques in bypassing web security, verifying data integrity, and vertical system integration.

📌 Key Features
Hybrid Selenium-Request Engine: Bypasses Web Application Firewalls (WAF) by capturing session cookies via Selenium and transitioning to high-speed data collection.

Forensic Audit System: A specialized module that proved a discrepancy between the platform's claimed count (58) and actual rendered reviews (55) was due to "Ghost Data" (unsynchronized server-side deletions), ensuring 100% data reliability.

Vertical Integration: Consolidates separate stages—Scout (HTML analysis), Scrape (collection), Audit (verification), and Report (Excel generation)—into a single, high-efficiency PalantirIntegrator class.

Automated Insights: Integration with openpyxl to automatically highlight critical keywords (e.g., "translation," "literal translation") in exported Excel reports for immediate sentiment analysis.

🛠 Tech Stack
Language: Python

Core Libraries: Selenium, BeautifulSoup4, Pandas, Openpyxl

DevOps: Webdriver-manager for automated driver configuration

🔍 Engineering Challenge: The Quest for Data Integrity
One of the most significant challenges was resolving a 3-review discrepancy in the dataset. By implementing a Real-Sort UI Simulator that forced a "Sort by Latest" action via radio button triggers, I verified that the missing data was not a script error but a platform-side "Soft Delete" issue. This obsessive attention to detail is the core of my data philosophy.