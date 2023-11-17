import sqlite3
import csv

# Menu functionality
def display_main_menu():
    print("MAIN MENU")
    print("0 Exit")
    print("1 CRUD operations")
    print("2 Show top ten companies by criteria")

def display_crud_menu():
    print("CRUD MENU")
    print("0 Back")
    print("1 Create a company")
    print("2 Read a company")
    print("3 Update a company")
    print("4 Delete a company")
    print("5 List all companies")

def display_top_ten_menu():
    print("TOP TEN MENU")
    print("0 Back")
    print("1 List by ND/EBITDA")
    print("2 List by ROE")
    print("3 List by ROA")

def process_top_ten_menu_option(cursor, option):
    if option == '0':
        return 'main'
    elif option == '1':
        display_top_ten(cursor, calculate_top_ten_nd_ebitda, "ND/EBITDA")
    elif option == '2':
        display_top_ten(cursor, calculate_top_ten_roe, "ROE")
    elif option == '3':
        display_top_ten(cursor, calculate_top_ten_roa, "ROA")
    # Additional options for other indicators
    elif option == '4':
        display_top_ten(cursor, calculate_top_ten_pe, "P/E")
    elif option == '5':
        display_top_ten(cursor, calculate_top_ten_ps, "P/S")
    elif option == '6':
        display_top_ten(cursor, calculate_top_ten_pb, "P/B")
    elif option == '7':
        display_top_ten(cursor, calculate_top_ten_la, "L/A")
    else:
        print("Invalid option!")

    return 'main'  # Always return to the main menu after displaying top ten




## Table Operations
def create_company(cursor, conn):
    ticker = input("Enter ticker (in the format 'MOON'): ")
    name = input("Enter company (in the format 'Moon Corp'): ")
    sector = input("Enter industries")

    # Financial data
    ebitda = float(input("Enter ebitda (in the format '987654321'): "))
    sales = float(input("Enter sales (in the format '987654321'): "))
    net_profit = float(input("Enter net profit (in the format '987654321'): "))
    market_price = float(input("Enter market price (in the format '987654321'): "))
    net_debt = float(input("Enter net debt (in the format '987654321'): "))
    assets = float(input("Enter assets (in the format '987654321'): "))
    equity = float(input("Enter equity (in the format '987654321'): "))
    cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'): "))
    liabilities = float(input("Enter liabilities (in the format '987654321'): "))

    # Insert into companies table
    cursor.execute("INSERT INTO companies VALUES (?, ?, ?)", (ticker, name, sector))

    # Insert into financial table
    cursor.execute("INSERT INTO financial VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (ticker, ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_equivalents, liabilities))
    conn.commit()
    print("Company created successfully!")

def read_company(cursor):
    name = input("Enter company name: ")
    cursor.execute("SELECT * FROM companies WHERE name LIKE ?", ('%' + name + '%',))
    companies = cursor.fetchall()

    if not companies:
        print("Company not found!")
        return

    for idx, company in enumerate(companies):
        print(f"{idx} {company[1]}")

    company_number = int(input("Enter company number: "))
    ticker = companies[company_number][0]

    cursor.execute("SELECT * FROM financial WHERE ticker = ?", (ticker,))
    financial = cursor.fetchone()

    # Use correct fields for calculations
    ebitda = financial[1]
    sales = financial[2]
    net_profit = financial[3]
    market_price = financial[4]
    net_debt = financial[5]
    assets = financial[6]
    equity = financial[7]
    cash_equiv = financial[8]
    liabilities = financial[9]

    pe = round(market_price / net_profit, 2) if net_profit else None
    ps = round(market_price / sales, 2) if sales else None
    pb = round(market_price / assets, 2) if equity else None
    nd_ebitda = None if ebitda is None or ebitda == 0 else round(net_debt / ebitda, 2)
    roe = round(net_profit / equity, 2) if equity else None
    roa = round(net_profit / assets, 2) if assets else None
    la = round(liabilities / assets, 2) if assets else None

    # Printing results
    print(f"{ticker} {companies[company_number][1]}")
    print(f"P/E = {pe}")
    print(f"P/S = {ps}")
    print(f"P/B = {pb}")
    print(f"ND/EBITDA = {nd_ebitda}")
    print(f"ROE = {roe}")
    print(f"ROA = {roa}")
    print(f"L/A = {la}")

def update_company(cursor, conn):
    name = input("Enter company name: ")
    cursor.execute("SELECT * FROM companies WHERE name LIKE ?", ('%' + name + '%',))
    companies = cursor.fetchall()

    if not companies:
        print("Company not found!")
        return

    for idx, company in enumerate(companies):
        # Only output index and company name
        print(f"{idx} {company[1]}")

    company_number = int(input("Enter company number: "))
    ticker = companies[company_number][0]

    # New financial data
    ebitda = float(input("Enter ebitda (in the format '987654321'): "))
    sales = float(input("Enter sales (in the format '987654321'): "))
    net_profit = float(input("Enter net profit (in the format '987654321'): "))
    market_price = float(input("Enter market price (in the format '987654321'): "))
    net_debt = float(input("Enter net debt (in the format '987654321'): "))
    assets = float(input("Enter assets (in the format '987654321'): "))
    equity = float(input("Enter equity (in the format '987654321'): "))
    cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'): "))
    liabilities = float(input("Enter liabilities (in the format '987654321'): "))

    # Update financial table
    cursor.execute('''UPDATE financial SET ebitda=?, sales=?, net_profit=?, market_price=?, 
                      net_debt=?, assets=?, equity=?, cash_equivalents=?, liabilities=? 
                      WHERE ticker=?''',
                   (ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_equivalents, liabilities, ticker))
    conn.commit()
    print("Company updated successfully!")

def delete_company(cursor, conn):
    name = input("Enter company name: ")
    cursor.execute("SELECT * FROM companies WHERE name LIKE ?", ('%' + name + '%',))
    companies = cursor.fetchall()

    if not companies:
        print("Company not found!")
        return

    # Display only the company names, not the tickers
    for idx, company in enumerate(companies):
        print(f"{idx} {company[1]}")  # company[1] is the name

        company_number = int(input("Enter company number: "))
    ticker = companies[company_number][0]

    # Delete from companies and financial tables
    cursor.execute("DELETE FROM companies WHERE ticker=?", (ticker,))
    cursor.execute("DELETE FROM financial WHERE ticker=?", (ticker,))
    conn.commit()
    print("Company deleted successfully!")

def list_all_companies(cursor):
    print("COMPANY LIST")
    cursor.execute("SELECT ticker, name, sector FROM companies ORDER BY ticker")  # Exclude the ticker from the SELECT statement
    for company in cursor.fetchall():
        # Ensure only the company name and sector are printed
        print(f"{company[0]} {company[1]} {company[2]}")

## Ratio computations for Top 10 menu
def display_top_ten(cursor, calculation_function, indicator_name):
    results = calculation_function(cursor)
    print(f"TICKER {indicator_name}")
    for ticker, value in results:
        print(f"{ticker} {round(value, 2)}")

def calculate_top_ten_nd_ebitda(cursor):
    cursor.execute('''
        SELECT ticker, (net_debt / ebitda) AS nd_ebitda
        FROM financial
        WHERE ebitda != 0 AND net_debt IS NOT NULL AND ebitda IS NOT NULL
        ORDER BY nd_ebitda DESC
        LIMIT 10
    ''')
    return cursor.fetchall()

def calculate_top_ten_pe(cursor):
    cursor.execute('''
        SELECT ticker, (market_price / net_profit) AS pe
        FROM financial
        WHERE net_profit != 0 AND market_price IS NOT NULL AND net_profit IS NOT NULL
        ORDER BY pe DESC
        LIMIT 10
    ''')
    return cursor.fetchall()

def calculate_top_ten_ps(cursor):
    cursor.execute('''
        SELECT ticker, (market_price / sales) AS ps
        FROM financial
        WHERE sales != 0 AND market_price IS NOT NULL AND sales IS NOT NULL
        ORDER BY ps DESC
        LIMIT 10
    ''')
    return cursor.fetchall()

def calculate_top_ten_pb(cursor):
    cursor.execute('''
        SELECT ticker, (market_price / equity) AS pb
        FROM financial
        WHERE equity != 0 AND market_price IS NOT NULL AND equity IS NOT NULL
        ORDER BY pb DESC
        LIMIT 10
    ''')
    return cursor.fetchall()

def calculate_top_ten_roe(cursor):
    cursor.execute('''
        SELECT ticker, (net_profit / equity) AS roe
        FROM financial
        WHERE equity != 0 AND net_profit IS NOT NULL AND equity IS NOT NULL
        ORDER BY roe DESC
        LIMIT 10
    ''')
    return cursor.fetchall()

def calculate_top_ten_roa(cursor):
    cursor.execute('''
        SELECT ticker, (net_profit / assets) AS roa
        FROM financial
        WHERE assets != 0 AND net_profit IS NOT NULL AND assets IS NOT NULL
        ORDER BY roa DESC
        LIMIT 10
    ''')
    return cursor.fetchall()

def calculate_top_ten_la(cursor):
    cursor.execute('''
        SELECT ticker, (liabilities / assets) AS la
        FROM financial
        WHERE assets != 0 AND liabilities IS NOT NULL AND assets IS NOT NULL
        ORDER BY la DESC
        LIMIT 10
    ''')
    return cursor.fetchall()


# Function to read data from CSV, replace empty values with None
def read_csv_data(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header row
        data = []
        for row in reader:
            data.append([None if cell == '' else cell for cell in row])
        return header, data

def is_table_empty(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0] == 0

def load_data_from_csv(cursor):
    companies_header, companies_data = read_csv_data('../../test/companies.csv')
    financial_header, financial_data = read_csv_data('../../test/financial.csv')

    cursor.executemany('INSERT INTO companies VALUES (?, ?, ?)', companies_data)
    cursor.executemany('INSERT INTO financial VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', financial_data)

def initialize_database(cursor):
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            ticker TEXT PRIMARY KEY,
            name TEXT,
            sector TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial (
            ticker TEXT PRIMARY KEY,
            ebitda REAL,
            sales REAL,
            net_profit REAL,
            market_price REAL,
            net_debt REAL,
            assets REAL,
            equity REAL,
            cash_equivalents REAL,
            liabilities REAL
        )
    ''')

    # Load data from CSV only if tables are empty
    if is_table_empty(cursor, "companies") and is_table_empty(cursor, "financial"):
        load_data_from_csv(cursor)


def main():
    print("Welcome to the Investor Program!")
    # Open a connection to the SQLite database file `investor.db`
    conn = sqlite3.connect('investor.db')
    # Create a new SQLite3 cursor
    cursor = conn.cursor()
    # Initialize the database
    initialize_database(cursor)

    current_menu = 'main'
    while True:
        if current_menu == 'main':
            display_main_menu()
        elif current_menu == 'crud':
            display_crud_menu()
        elif current_menu == 'top_ten':
            display_top_ten_menu()

        option = input("Enter an option: ")

        if current_menu == 'main':
            if option == '0':
                print("Have a nice day!")
                break
            elif option == '1':
                current_menu = 'crud'
            elif option == '2':
                current_menu = 'top_ten'
            else:
                print("Invalid option!")
        elif current_menu == 'crud':
            if option == '0':
                current_menu = 'main'
            elif option == '1':
                create_company(cursor, conn)
                current_menu = 'main'
            elif option == '2':
                read_company(cursor)
                current_menu = 'main'
            elif option == '3':
                update_company(cursor, conn)
                current_menu = 'main'
            elif option == '4':
                delete_company(cursor, conn)
                current_menu = 'main'
            elif option == '5':
                list_all_companies(cursor)
                current_menu = 'main'
            else:
                print("Invalid option!")

        elif current_menu == 'top_ten':
            # display_top_ten_menu()
            current_menu = process_top_ten_menu_option(cursor, option)

    conn.commit()
    conn.close()

# Call the main function when the script is executed
if __name__ == "__main__":
    main()

