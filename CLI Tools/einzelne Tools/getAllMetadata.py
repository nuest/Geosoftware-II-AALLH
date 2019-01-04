import os
import sys

# add local modules folder
file_path = '../Python_Modules'
sys.path.append(file_path)

from osgeo import gdal, ogr, osr
from subprocess import Popen, PIPE, call
import click

# asking for parameters in command line
@click.command()
@click.option('--path', prompt="File path", help='Path to file')
@click.option('--name', prompt="File name", help="File name with extension")
def main(path, name):
	filepath = "%s\%s" % (path, name)
	# try:
	# 	gdal.UseExceptions()
	# 	ds = gdal.Open(filepath)
	# 	info = gdal.Info(ds)
	# 	print(info)
	# except:
	# 	try:
	# 		args = ['ogrinfo', '-ro', '-so', '-al', '%s' % filepath]
	# 		process = Popen(args, stdout=PIPE, stderr=PIPE)
	# 		stdout = process.communicate()[0].decode('utf-8').strip()
	# 		print(stdout)
	# 	except:
	# 		pass
	print(call(['get-acl', filepath], shell=True))



if __name__ == "__main__":
    main()