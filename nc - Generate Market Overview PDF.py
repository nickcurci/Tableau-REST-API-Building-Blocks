'''
    req = s.get(
        f'https://tableau.website.org/api/3.11/sites/siteid/views/{Daily_Charge_ID}/pdf?vf_Market={Market}&orientation=landscape&maxAge=1',
        headers=headers)
'''
def get_full_pdfs(Market, index):
    # the folder which all reports generated will be stored in (Ex. 2021 Jun)
    # the folder which seperates reports to specific hospitals (Ex. GSMC)
    MarketFolder = provmarket_list["Market"][index]

    print('sending request')

    req = s.get(
        f'https://tableau.website.org/api/3.11/sites/siteid/views/{Daily_Charge_ID}/pdf?vf_Market={Market}&orientation=landscape&maxAge=1',
        headers=headers)
    print('sending request')
    req.raise_for_status()
    print('request recieved')
    # Make sure returned object is a (.pdf)
    assert req.headers["content-type"] == "application/pdf"

    # Writing PDF to destination directory
    file_path = path + "/" + Market + "/" + Market + " Summary Daily Charge Report - " + yesterday.strftime(
        '%Y %m %d') + ".pdf"
    print(f'file path is set to {file_path}')

    print('now actually writing the pdfs')
    f = open(
        file_path, "wb")
    f.write(req.content)
    f.close()
    # Generate Code Report if requestet
    returned_provmarket_list["Generated"][index] = True

    print(f'{Market} report generated in {str(final_time)}')

    for Market in market_list:
        get_full_pdfs(Market, i)
