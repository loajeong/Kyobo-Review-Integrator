# 🚀 Kyobo Review Integrator: A Palantir-Inspired Data Pipeline
> **"Quantifying Translation Quality: An End-to-End Pipeline for 'The Technological Republic-Hard Power, Soft Belief, and the Future of the West ' Analysis"**

This project is a high-performance data engineering pipeline designed to collect and analyze customer feedback for the Korean translation of **'The Technological Republic'** by Alex Karp (CEO of Palantir). Moving beyond basic web scraping, this system demonstrates advanced capabilities in bypassing web security, ensuring data integrity, and achieving seamless vertical integration.

## 🛠 Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-Selenium-%2343B02A?style=for-the-badge&logo=Selenium&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.12.2-blue?style=for-the-badge)

---

## 📌 Key Features

* **Hybrid Selenium-Request Engine**: 
    * Optimized performance by capturing session cookies via Selenium to bypass **Web Application Firewalls (WAF)**, then transitioning to high-speed data collection using the Requests library.
* **Forensic Audit System (Data Reliability)**: 
    * Identified and resolved a discrepancy between the platform's claimed count (58) and actual rendered reviews (55). Proven to be "Ghost Data" caused by unsynchronized server-side deletions, ensuring **100% data integrity**.
* **Vertical System Integration**: 
    * Consolidated the entire workflow—**Scout** (HTML analysis), **Scrape** (collection), **Audit** (verification), and **Report** (Excel generation)—into a single, high-efficiency `PalantirIntegrator` class.
* **Automated Insights**: 
    * Integrated with `openpyxl` to automatically highlight critical keywords (e.g., "translation," "literal translation") in exported reports, facilitating immediate sentiment analysis for stakeholders.

---

## 🔍 Engineering Challenge: The Quest for Data Integrity

> **"Uncompromising attention to data integrity is the core of my engineering philosophy."**

The most significant challenge in this project was resolving a 3-review discrepancy in the dataset.

1.  **The Problem**: The source website displayed a total of 58 reviews, but only 55 were accessible via standard scraping.
2.  **The Solution**: Developed a **Real-Sort UI Simulator** that forced a "Sort by Latest" action through radio button triggers, mimicking human interaction to reveal hidden DOM elements.
3.  **The Result**: Verified that the missing data was not a script error but a platform-side **"Soft Delete"** issue (data remaining on the server but hidden from the UI).

This rigorous verification process demonstrates my capability to handle data anomalies and deliver reliable, audit-ready datasets in a professional environment.

---

## 📂 Project Structure
* **Scout**: Advanced parsing and HTML structure analysis.
* **Scrape**: Multi-layered data extraction logic.
* **Audit**: Forensic verification of data quantity and quality.
* **Report**: Automated visualization and keyword-based reporting.

---

## ✉️ Contact
* **Author:** Seoyeon Jeong
* **LinkedIn:** [https://www.linkedin.com/in/im-seoyeon-jeong/]
* **Email:** [syn.eoeo@gmail.com]

