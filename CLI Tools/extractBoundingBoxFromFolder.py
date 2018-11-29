import getBoundingBox as box
import getTimeExtent as timeEx
import subprocess

from os import listdir
from os.path import isfile, join
import click

@click.command()
@click.option('--path', prompt="File path", help='Path to file')
def main(path):
    res = getAllResultsFromCLIFromFolder(path)
    for x in res:
        if x[1][0] == None:
            if x[2][0]:
                click.echo((x[0], x[1][1], x[2][1]))
            else:
                click.echo((x[0], x[1][1], x[2][0]))
        else:
            if x[2][0] == None:
                click.echo((x[0], x[1][0], x[2][1]))
            else:
                click.echo((x[0], x[1][0], x[2][0]))


def getAllResultsFromCLIFromFolder(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    # print(onlyfiles)
    res = []
    for fileFromDir in onlyfiles:
        resultFromFile = [fileFromDir,box.getBoundingBox(path=path, name=fileFromDir), timeEx.getTimeExtend(path=path, name=fileFromDir)]
        res.append(resultFromFile)

    return res


if __name__ == '__main__':
    main()