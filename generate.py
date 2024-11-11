import pandas as pd
import yfinance as yf


# Quick script for generating a dataset of basic 2024 Fortune1000 company raw EBITDA from Yahoo! Finance

def get_financials(ticker):
    """
    Extract 2024 EBITDA for each Fortune1000 except for the company's without reported earnings,
    where an EBITDA proxy is used instead.  
    """
    company = yf.Ticker(ticker)
    total_financials = company.financials

    if not total_financials.empty and "EBITDA" in total_financials.index:
        yearly_ebitda = total_financials.loc["EBITDA"]
        ebitda_data = get_annual_data(yearly_ebitda, ticker)

        if 2024 in ebitda_data:
            print(f"{ticker} | ***2024 EBITDA: {ebitda_data[2024]}***")


            return ebitda_data[2024]
        
    print(f"{ticker} | 2024 EBITDA not found. Extracting quarterly data to calculate LTM...")


    quarterly_financials = company.quarterly_financials

    # calculate LTM in the event that enough quarters are available. 
    if not quarterly_financials.empty and "EBITDA" in quarterly_financials.index:

        try:
            quarterly_ebitda = quarterly_financials.loc["EBITDA"]

            ltm = get_ltm(quarterly_ebitda, ticker)

            if ltm is not None:
                print(f"{ticker} | ***LTM: {ltm}***")

                return ltm
            
        except Exception as e:
            print(f"{ticker} | ERROR calculating LTM: {e}")

    print(f"{ticker} | No quarterly data. Checking for yearly EBITDA. (1/2)")

    if not total_financials.empty and "EBITDA" in total_financials.index:

        yearly_ebitda = total_financials.loc["EBITDA"]
        ebitda_data = get_annual_data(yearly_ebitda, ticker)

        prev_year = max(ebitda_data.keys(), default=None)
        if prev_year:
            print(f"{ticker} | Using previous year's EBITDA: {ebitda_data[prev_year]}. (2/2)")

            return ebitda_data[prev_year]

    # use the most previous year's EBITDA otherwise
    print(f"{ticker} | ERROR: No yearly (2024 or previous) OR quarterly EBITDA data available. (2/2)")


    return None


def get_annual_data(yearly_ebitda, ticker):
    """
    Extracts EBITDA by fiscal year. The company financials within the original dataset
    are from 2024 (from the available quarters at the time). 
    """

    ebitda_data = {}

    for timestamp, value in yearly_ebitda.items():
        try:
            year = pd.to_datetime(timestamp).year
            ebitda_data[year] = value

        except Exception as e:
            print(f"ERROR ({ticker} | timestamp: {timestamp}): {e}")    # typically due to mismatching timestamp expression

    return ebitda_data


def get_ltm(quarterly_ebitda, ticker):
    """
    Calculate a proxy for EBITDA in scenarios where companies have not reported their earnings yet.
    Some companies did not yet publish 2024 reports, so we can use the previous year and the latest 
    quarter to calculate the last 12 months (LTM). 
    """

    try:
        # LTM is the sum of last four quarters (e.g., 3Q'24, 2Q'24, 1Q'24, 4Q'23)
        ltm = quarterly_ebitda.sort_index(ascending=False)[:4].sum()

        if not pd.isna(ltm):
            return ltm
        
    except Exception as e:
        # print(f"{ticker} | ERROR calculating LTM: {e}")
        pass

    return None

def check_values(df):
    """
    Check amount of missing values are in the resulting dataset. These will
    be handled in the main program. 
    """
    na_pct = df['EBITDA'].isna().sum() / len(df)

    if na_pct > 0:
        print(f"{na_pct} metrics missing")
    



def generate_data(kaggle_data, generated_data):
    """
    Create dataset based on 2024 EBITDA for all companies in the original dataset
    along with their original listed metrics.
    """
    ebitda_values = []

    df = pd.read_csv(kaggle_data)
    metrics = "EBITDA/LTM", "EBITDA Margins"

    for ticker in df["Ticker"]:

        if pd.isna(ticker):
            # print(f"ERROR ({ticker}): No ticker found.")
            ebitda_values.append(None)
            continue

        ebitda = get_financials(ticker)
        ebitda_values.append(ebitda)


    df["EBITDA"] = ebitda_values
    df["EBITDA_Margin"] = df["EBITDA"] / df["Revenues_M"]
    df["EBITDA_Margin"] = df["EBITDA_Margin"].fillna(0)

    # these columns are irrelevant
    columns_to_drop = ['Rank', 'CEO', 'Founder_is_CEO', 'Growth_in_Jobs', 'Change_in_Rank', 
                       'Gained_in_Rank', 'Global500', 'Dropped_in_Rank', 'Newcomer_to_the_Fortune500',
                       'FemaleCEO', 'Worlds_Most_Admired_Companies', 'Footnote', 'Best_Companies_to_Work_For',
                       'Country', 'HeadquartersCity', 'HeadquartersState', 'Website', 'Updated', 'Ticker']

    df = df.drop(columns=columns_to_drop, errors='ignore')
    

    check_values(df)

    df.to_csv(generated_data, index=False)
    print(f"**COMPLETE**\nDataset '{generated_data}' generated with {metrics}.")


if __name__ == "__main__":

    # # quick test using a few tickers instead of the entire set from the Kaggle data.
    # tickers = ["GOOGL", "WBA", "COST"]  # e.g., Google is an example of a company without 2024 financials, so we should get LTM.
    # for ticker in tickers:
    #     financial_metric = get_financials(ticker)
    #     print(f"{ticker} EBITDA: {financial_metric}")

    kaggle_data = "data/KaggleData.csv"  # our original Kaggle dataset
    generated_data = "data/FinancialData.csv"


    generate_data(kaggle_data, generated_data)
