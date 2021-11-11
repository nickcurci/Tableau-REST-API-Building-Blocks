'''
    from PyPDF2 import PdfFileMerger
    pdfs = res
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(os.path.join(market_path, f"{Market} Daily Charge Report - {yesterday}.pdf"))
    merger.close()
'''
def mergePDFs(Market):
    market_path = path + "/" + Market
    file_paths = []
    for folder, subs, files in os.walk(market_path):
        for filename in files:
            file_paths.append(os.path.abspath(os.path.join(folder, filename)))
    print(file_paths)
    newlist = []
    for f in file_paths:
        if f.endswith('.pdf'):
            newlist.append(f)
            newlist.sort()
        else:
            print(f'{f} is not a pdf')

    res = []
    for n in newlist:
        if 'Summary Daily Charge Report' in n:
            res.append(n)
        else:
            pass
    for n in newlist:
        if 'Summary Daily Charge Report' in n:
            pass
        else:
            res.append(n)


    from PyPDF2 import PdfFileMerger
    pdfs = res
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(os.path.join(market_path, f"{Market} Daily Charge Report - {yesterday}.pdf"))
    merger.close()

    for Market in market_list:
        mergePDFs(Market)
