# Predicting Blue-Chip Financial Health Trajectory  

By Jessica Villanueva, Param Sejpal, Yu-Heng Chi, Yihan Yang, and Zhiyi Zhang

The focus of this project is to use machine learning to predict financial health trajectories of the 2024 Fortune1000 companies. Our objectives include (i) performing regression to predict future market cap based on historical EBITDA, revenue, and other financial metrics and (ii) using classification models to label companies as *Profitable* or *Non-Profitable*.


## Installation

1. Clone this repo
2. Set up a virtual environment
3. `pip install -r requirements.txt`
4. (Optional) the dataset we use is included in this repo, but to see how we created the data, run the data creation script `generate.py` to create the dataset
5. Run the Jupyter notebook!


## Setup
This directory includes the following files.

1. **FinancialData.csv**: the final dataset we created and are using in this project.
2. `generate.py`: a quick script that can be run to see how the dataset was created.
    * Financial metrics that were added to the dataset come from Yahoo! Finance.
3. **KaggleData.csv**: The Kaggle dataset with basic company metrics (ticker, revenue, etc.) used in creating the dataset. 


## Dataset
Many companies report EBITDA or earnings differently, which is why we created a dataset based on what we determined is the most consistent reflection of income statement and balance sheet data. **FinancialData.csv** is Financial data from Fortune1000 companies that was created using different sources of financial data. Income statement and balance sheet information was accessed from:
 
1. A [Kaggle dataset](https://www.kaggle.com/datasets/jeannicolasduval/2024-fortune-1000-companies/data) (k04dRunn3r on Kaggle).
2. Yahoo! Finance financials.
3. 10-K reports from the EDGAR archives on SEC.gov.


## Brief Descriptions of Metrics

1. **Earnings before Interest, Taxes, Depreciation, and Amortization (EBITDA)**: A non-GAAP, capital structure-neutral, accrual accounting-based measure of profitability. An EBITDA margin represents EBITDA as a percentage of total revenue.
2. **EBITDA Profitability**: Profitability of a company; the company is profitable if total income outweighs expenses.
3. **Revenue**: Sales prior to any expenses.
7. **market cap**: Size of the equity portion of the business.
8. **Gross Profit**: Profit after deducting cost of goods sold.
9. **Profits Percent Change** and **Revenue Percent Change**: Growth percentage of current year's metric value from year before.
<br>
