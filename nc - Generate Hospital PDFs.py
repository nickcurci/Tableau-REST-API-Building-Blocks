'''
    req = s.get(
        f'https://tableau.website.org/api/3.11/sites/siteid/views/{Daily_Charge_ID}/pdf?vf_Provider%20Market={ProvMarket}&orientation=landscape&maxAge=1',
        headers=headers)
'''

def get_Market_PDF(ProvMarket, index):
    """Get KPI Reports

    This function generates reports for the given provider and stores it in the folder given in the mailing list. This function is called
    by the driver below and passed in arguments which help it request the proper report.

    This function generates and stores a (.pdf) file containing the providers KPI report and a (.xlsx) file containing the providers Code Adjustments report

    @param name (str): the full name of the provider (used for formatting only)
    @param first_name (str): the first name of the provider as it appears in tableau
    @param last_name (str): the last name of the provider as it appears in tableau
    @param generate (str): a string which generates the reports for the given provider only if it is yes (redundency for the mailing list)
    @param generate_data_detail (str): a character (y) which indicates if a data detail report should be generated for the provider
    @param index (int): integer representing the index of the provider in a dataframe. Used to pull information about where to store the files
    """
    # the folder which all reports generated will be stored in (Ex. 2021 Jun)
    # the folder which seperates reports to specific hospitals (Ex. GSMC)
    print('setting the market folder index')
    MarketFolder = provmarket_list["Market"][index]

    # Sending request for KPI report using the provider filter and name to grab the individual report
    req = s.get(
        f'https://tableau.website.org/api/3.11/sites/siteid/views/{Daily_Charge_ID}/pdf?vf_Provider%20Market={ProvMarket}&orientation=landscape&maxAge=1',
        headers=headers)
    print('sending request')
    req.raise_for_status()
    print('request recieved')
    # Make sure returned object is a (.pdf)
    assert req.headers["content-type"] == "application/pdf"
    print('headers have been asserted')
    # Writing PDF to destination directory
    file_path = path + "/" + MarketFolder + "/" + ProvMarket + " Individual Charge Detail - " + yesterday.strftime(
        '%Y %m %d') + ".pdf"
    print(f'file path is set to {file_path}')
    print('now actually writing the pdfs')
    f = open(
        file_path, "wb")
    f.write(req.content)
    f.close()
    print(f'{ProvMarket} report written to {file_path}')
    # Generate Code Report if requestet
    returned_provmarket_list["Generated"][index] = True

print('...All PDFs generated')
print('Getting Excels...')

for i in range(len(ProvMarket)):  # range(250):
    get_Market_PDF(ProvMarket[i], i)