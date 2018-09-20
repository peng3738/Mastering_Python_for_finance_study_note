#from urllib import request
from urllib.request import urlretrieve

url_path='http://www.stoxx.com/download/historical_values/'
stoxxeu600_url=url_path+'hbrbcpe.txt'

#vstoxx_url=url_path+'h_vstoxx.txt'

vstoxx_url=url_path+'h_vstoxx.txt'

data_folder='E:/python_study/Mastering_Python_for_finance/chapter_6/data'
stoxxeu600_filepath=data_folder+"stoxxeu600.txt"
vstoxx_filepath=data_folder+"vstoxx.csv"

urlretrieve(stoxxeu600_url,stoxxeu600_filepath)
urlretrieve(vstoxx_url,vstoxx_filepath)

import os.path
os.path.isfile(stoxxeu600_filepath)
os.path.isfile(vstoxx_filepath)


