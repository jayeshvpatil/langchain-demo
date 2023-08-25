import pyodbc

server = 'localhost' 
database = 'cisdemo' 
username = 'sa' 
password = 'p@55word' 
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=no;UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

cursor.execute('SELECT top 10 * FROM dbo.Patient')

for i in cursor:
    print(i)


    # pip install --no-binary :all: pyodbc

    """
    install macos driver
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18
    """