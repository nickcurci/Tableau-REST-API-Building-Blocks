import logging
logpath = fr"Path.txt"
logging.basicConfig(filename=logpath,
                    filemode='w',
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                   level=logging.INFO)
                   