\# **Sales Analytics System**



\## **Objective**

This project reads raw sales data from a text file, cleans invalid and incorrect records, and performs basic sales analysis using Python.



\## **Dataset Description**

The dataset contains sales transaction records with the following fields:



1\. Transaction ID

2\. Date

3\. Product ID

4\. Product Name

5\. Quantity

6\. Unit Price

7\. Customer ID

8\. Region



\## **Data Cleaning Rules**

The following records are removed:

1\. Quantity ≤ 0

2\. Unit Price ≤ 0

3\. Missing Customer ID

4\. Missing Region

5\. Transaction ID not starting with "T"



The following cleaning operations are performed:

1\. Removal of commas from product names

2\. Removal of commas from numeric fields



\## **Sales Analysis Performed**

1\. Total Revenue

2\. Revenue by Region

3\. Top Selling Product (by revenue)



\## **Project Structure**

sales-analytics-system/

├── main.py

├── README.md

├── data/

│   └── sales\_data.txt

├── utils/

│   └── file\_handler.py





\## **How to Run**

1\. Install Python 3

2\. Open terminal in project folder

3\. Run: python main.py



\##**Output**

The program displays:



1\. Total records processed

2\. Number of invalid records removed

3\. Number of valid records

4\. Sales analysis summary

