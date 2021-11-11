import pandas as pd
import snowflake.connector
def testDV():
    # Test whether DV Table has been updated

    # ## Testing the snowflake Connection
    print('Testing the snowflake connection')
    # #The credentials can be stored in a text file.
    # with open(snowflakefile, 'r', encoding='utf-8') as f:
    #     snow = f.readlines()
    #
    # username = str(snow[0]).replace('\n', '')
    # password = str(snow[1]).replace('\n', '')
    # account = str(snow[2]).replace('\n', '')
    # warehouse = str(snow[3]).replace('\n', '')
    # database = str(snow[4]).replace('\n', '')
    # schema = str(snow[5]).replace('\n', '')

    username = 'xxxx'
    password = 'xxxxx'
    account = 'xxxxxx'
    warehouse = 'xxxxxxxx'
    database = 'xxxxxxxx'
    schema = 'xxxxxxxxx'

    ctx = snowflake.connector.connect(
        user=username,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema)
    print('ctx generated')
    # Create a cursor object.
    cur = ctx.cursor()
    print('cursor set')

# The connection was successful at this point
    # now testing DV with a query
    #Query can also be stored in a text file

    # with open(CheckDV_SQL, 'r', encoding='utf-8') as f:
    #     sql = f.read()
    #     sql = sql.replace('\n', '')
    # Execute a statement that will generate a result set.
    sql = ''' select  * FROM X '''
    cur.execute(sql)
    print(f'The query is: {sql} and it has been executed')
    # Fetch the result set from the cursor and deliver it as the Pandas DataFrame.
    df = cur.fetch_pandas_all()
    print(f'The df returned is: {df}')

    #grouping the DF
    groupeddf = df['CONTEXTID'].groupby(df['TABLENAME']).count().reset_index()
    print(f'The query returned: {groupeddf}')

    #testing the DF to see if 4 rows have been returned for each ID
    if groupeddf.empty:
        print('...DV not updated, sleeping for 15 minutes and then retrying')
        #
        # time.sleep(900)
        # raise Exception("Retrying...")
    else:
        print('setting query results into list')
        mylist = []
        for row in groupeddf['CONTEXTID']:
            if row != 4:
                mylist.append('fail')
                print(f'the list is {mylist}')
            else:
                mylist.append('pass')
                print(f'the list is {mylist}')
        if 'fail' in mylist:
            print('...DV not updated, sleeping for 15 minutes and then retrying')
            #
            # time.sleep(900)
            # raise Exception("Retrying...")
        else:
            print('...DV appears to be updated, continuing on...')
testDV()

