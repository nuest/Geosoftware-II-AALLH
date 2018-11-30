"""
@Author Henry Fock
"""


import getBoundingBox as box
import getTimeExtent as timeEx
import subprocess
import threading

from os import listdir
from os.path import isfile, join
import click

@click.command()
@click.option('--path', prompt="File path", help='Path to file')
def main(path):
    threads = []
    res = []
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    for name in onlyfiles:
        current = CliTools(path, name)
        threads.append(current)
        current.start()

    for thread in threads:
        thread.join()
        res.append(thread.result)

    click.echo("\n Ergebnis:")
    for x in res:
        if x[1][0] == None:
            if x[2][0] == None:
                click.echo((x[0], x[1][1], x[2][1]))
            else:
                click.echo((x[0], x[1][1], x[2][0]))
        else:
            if x[2][0] == None:
                click.echo((x[0], x[1][0], x[2][1]))
            else:
                click.echo((x[0], x[1][0], x[2][0]))



class CliTools(threading.Thread):
    def __init__(self, path, name): 
        threading.Thread.__init__(self) 
        self.path = path
        self.name = name
        self.result = []

    def run(self):
        bbox = box.getBoundingBox(path=self.path, name=self.name)
        time = timeEx.getTimeExtend(path=self.path, name=self.name)
        self.result.extend([self.name, bbox, time])


if __name__ == '__main__':
    main()