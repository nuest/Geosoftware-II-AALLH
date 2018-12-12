"""
@Author Henry Fock
"""
import sys
file_path = '../Python_Modules'
sys.path.append(file_path)

import getBoundingBox as box
import getTimeExtent as timeEx
import subprocess
# import threading
import gevent.monkey

from os import listdir
from os.path import isfile, join
import click

@click.command()
@click.option('--path', prompt="File path", help='Path to file')
def main(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    jobs = [gevent.spawn(getAllDataFromCliTools, name, path) for name in onlyfiles]
    gevent.joinall(jobs)

    click.echo("\n Ergebnis:")
    for x in jobs:
        if x.value[1][0] == None:
            if x.value[2][0] == None:
                click.echo((x.value[0], x.value[1][1], x.value[2][1]))
            else:
                click.echo((x.value[0], x.value[1][1], x.value[2][0]))
        else:
            if x.value[2][0] == None:
                click.echo((x.value[0], x.value[1][0], x.value[2][1]))
            else:
                click.echo((x.value[0], x.value[1][0], x.value[2][0]))


def getAllDataFromCliTools(name, path):
    bbox = box.getBoundingBox(path=path, name=name)
    time = timeEx.getTimeExtent(path=path, name=name)
    return [name, bbox, time]


if __name__ == '__main__':
    main()