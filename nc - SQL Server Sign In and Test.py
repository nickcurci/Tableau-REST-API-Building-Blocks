import pyodbc
import pandas as pd
#Set the connection
conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                          "Server=xxxx-xxxxx.xxxx.xxxxxx;"
                          "Database=xxxx;"
                          "Trusted_Connection=yes;")

#Set the recipients query
SMGDistributionRecipientsBASE = pd.read_sql(sql=''' SELECT *
      FROM [xxxx].[xxxxxxxxxxxxxxx].[xxxxxxxxxxxxxxxxx] ''', con=conn)

#Query Results into List
LogRecipientsList = SMGDistributionRecipientsBASE.loc[SMGDistributionRecipientsBASE["LogFile"] == True]