\# Sales Analytics System



This project is a Python-based sales analytics system that processes raw sales data, performs validation and analysis, generates reports, and enriches data using an external API.



---



\## Project Structure



sales-analytics-system/

│

├── data/

│ └── sales\_data.txt

│

├── output/

│ ├── sales\_report.txt

│ └── enriched\_sales\_data.txt

│

├── utils/

│ ├── file\_handler.py

│ ├── data\_processor.py

│ └── api\_handler.py

│

├── main.py

├── requirements.txt

├── .gitignore

└── README.md



---



\## Setup Instructions



1\. Clone the repository

```bash

git clone https://github.com/<your-username>/sales-analytics-system.git

cd sales-analytics-system



2\. Install dependencies

pip install -r requirements.txt



---



\## How to Run the Program



From the project root directory, run:

python main.py



---



\##Output Generated



After successful execution, the following files are generated:



1. output/sales\_report.txt

Contains:



i) Overall sales summary

ii) Region-wise performance

iii) Top products and customers

iv) Daily sales trends

v) Performance insights

vi) API enrichment summary



2\. output/enriched\_sales\_data.txt

Contains: 



i) sales transactions enriched with product information from an external API.



---



\##Notes



1. No hardcoded file paths are used.

2\. The program runs end-to-end without errors.

3\. External API integration uses the requests library.

4\. Repository is public and follows the required folder structure.





Rachit Acharya

