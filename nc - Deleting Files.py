def deletefiles(Market):
    for fl in os.listdir(os.path.join(path)):
        if fl == Market:
            print(f)
            for fi in os.listdir(os.path.join(path, fl)):
                fn = (os.path.join(path, fl, fi))
                print(fn)
                if 'Individual' in fi:
                    os.remove(fn)
                else:
                    pass
                if 'Summary' in fi:
                    os.remove(fn)
                else:
                   pass
        else:
            pass

for Market in market_list:
    deletefiles(Market)
    