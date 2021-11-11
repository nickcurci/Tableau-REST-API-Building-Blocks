def closeFile():
    try:
        os.system('TASKKILL /F /IM excel.exe')
    except Exception:
        print("Oh no, our table, its broken")
closeFile()
