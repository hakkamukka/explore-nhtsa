import os
import zipfile
import urllib2

data_url = "ftp://ftp.nhtsa.dot.gov/GES/GES12/GES12_Flatfile.zip"
zip_name = "GES12_Flatfile.zip"

cwd = os.getcwd()
# dir_path = os.path.join(cwd, "GES12")
dir_path = os.path.dirname(cwd)
zip_path = os.path.join(dir_path, zip_name)

if not os.path.exists(dir_path):
    os.mkdir(dir_path)

if not os.path.exists(zip_path):
    f = urllib2.urlopen(data_url)
    # print f.read(100)
    with open(zip_path, 'wb') as fh:
        x = f.read()
        fh.write(x)

with zipfile.ZipFile(os.path.join(dir_path, zip_name), 'r') as z:
    z.extractall(dir_path)

# print cwd
# p = os.path.join(dir_path, '..')
# print p
