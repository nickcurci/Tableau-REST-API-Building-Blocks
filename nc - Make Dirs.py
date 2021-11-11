import os
import datetime
today = datetime.date.today()


daily_output_path = fr"Path"
path = daily_output_path + '/' + today.strftime('%Y %m %d')


def safe_make_dir(path):
    print('Making dirs')
    """Safe Make Directory

    Creates directories for file storage but checks whether the path already exists, if it does then return
    if not then create the directories

    @param path: the path of the directory to be created
    """
    print('checking to see if folders already exist')
    if os.path.exists(path):
        print(f'{today} folder skipper')
        # print(str(today) + " folder skipped")
        return
    else:
        # makedirs makes all directories necessary for the path. On first run this will make the parent directory with child and after will only make the child
        os.mkdir(path)
        print(f'{today} folder created')
        # print(str(today) + " folder created")
safe_make_dir(path)
 