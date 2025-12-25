# 🚀 Kyobo Review Integrator: A Universal Data Pipeline
> **"High-Fidelity Data Extraction & Forensic Audit Engine: Tested on 'The Technological Republic'"**

This project is a high-performance data engineering pipeline designed for the reliable collection and analysis of customer feedback from major bookstores. 

### 🎯 Strategic Source Selection: Why Kyobo Bookstore?
**Kyobo Bookstore** was strategically selected as the primary data source because it holds the **largest market share** in the South Korean book industry. This market dominance ensures an **overwhelmingly higher volume and density of review data** compared to any other platform. By targeting the industry leader, this pipeline secures a statistically significant and comprehensive dataset, providing the deepest possible insights into reader sentiment and translation quality.

While this version is showcased using **Alex Karp's 'The Technological Republic'**, the architecture is built as a **universal engine** capable of processing any target book with uncompromising data precision.

---

## 🛠 Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-Selenium-%2343B02A?style=for-the-badge&logo=Selenium&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.12.2-blue?style=for-the-badge)

---

## 📌 Key Features

* **Universal & Extensible Architecture**: 
    * Engineered with a modular class-based structure (`UniversalReviewIntegrator`), allowing the system to adapt to various book IDs and categories beyond a single use case.
* **Hybrid Selenium-Request Engine**: 
    * Optimized performance by capturing session cookies via Selenium to bypass **Web Application Firewalls (WAF)**, ensuring stable access to protected data layers.
* **Forensic Audit System (Data Reliability)**: 
    * A specialized module that identifies and resolves discrepancies between claimed counts and actual rendered data. In this project, it successfully proved "Ghost Data" issues, ensuring **100% data integrity**.
* **Vertical System Integration**: 
    * Consolidated the entire workflow—**Scout** (HTML analysis), **Scrape** (collection), **Audit** (verification), and **Report** (Excel generation)—into a single, high-efficiency pipeline.
* **Automated Insights**: 
    * Utilizes `openpyxl` to automatically highlight critical keywords (e.g., "translation," "readability") in exported reports for immediate sentiment analysis.

---

## 🔍 Engineering Challenge: The Quest for Data Integrity

> **"Uncompromising attention to data integrity is the core of my engineering philosophy."**

The defining challenge of this project was resolving a 3-review discrepancy found during the audit phase.

1.  **The Problem**: The source website claimed 58 reviews, but only 55 were accessible via standard rendering.
2.  **The Solution**: Developed a **Real-Sort UI Simulator** that forced a "Sort by Latest" action through radio button triggers, bypassing UI glitches to reveal hidden DOM elements.
3.  **The Result**: Verified that the missing data was a platform-side **"Soft Delete"** issue (unsynchronized server-side deletions), confirming that the pipeline had captured every single *valid* review.

---

## 🏗 Technical Note: Scalability & Honesty

While the current implementation focuses on high-fidelity extraction for a single target ID per execution to ensure maximum precision, the underlying architecture is designed to be **extensible**. 

* **Future Roadmap**: The system is prepared for future iterations including batch processing for multiple IDs and parallel multi-source integration. 
* **Design Philosophy**: I chose a "Surgical Strike" approach over "Mass Scraping" to prioritize data quality and audit-readiness—essential traits for any enterprise-grade data pipeline.

---

## 📂 Project Structure

```text
Kyobo-Review-Integrator/
├── main.py                 # Final Integrated Universal Integrator Class
├── requirements.txt        # List of dependencies
├── README.md               # Professional documentation
├── scripts/                # Legacy scripts showing the evolution of the pipeline
│   ├── v1_prototype.py     # Initial connection attempt
│   ├── v5_highlighter.py   # Visualization module
│   └── v7_forensic_audit.py# Final integrity verification logic
├── data/                   # Sample output reports (Excel)
└── assets/                 # Screenshots of highlighted results

---



## ✉️ Contact
* **Author:** Seoyeon Jeong
* **LinkedIn:** [https://www.linkedin.com/in/im-seoyeon-jeong/]
* **Email:** [syn.eoeo@gmail.com]




