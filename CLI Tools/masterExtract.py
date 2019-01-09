import click

import extractGeoDataFromFolder as fext
import getBoundingBox as box
import getPolygon as poly
import getTimeExtent as timeext


# asking for parameters in command line
@click.command()
@click.option('--path', prompt="Pleas enter path to Folder", help='Path to Folder containing Geofiles')
@click.option('--clear','-c', default=False, is_flag=True, help='Clear screen before showing results')
@click.option('--time', '-t', default=False, is_flag=True, help="execute time extraction for one file")
@click.option('--space', '-s', default=False, is_flag=True, help="execute boundingbox extraction for one file")
@click.option('--hull', '-h', default=False, is_flag=True, help="execute convex-hull extraction for one file")
def main(path, clear, time, space, hull):
    output = []

    name = ""
    if time or space or hull:
        name = click.prompt("Please enter filename")

    def timeOption(path, name):
        res = timeext.getTimeExtent(name, path)
        if res[0] is not None:
            return res[0]
        else:
            return res[1]

    def spaceOption(path, name):
        res = box.getBoundingBox(name, path)
        if res[0] is not None:
            return res[0]
        else:
            return res[1]

    def polyOption(path, name):
        res = poly.getPolygon(name, path)
        if res[0] is not None:
            return res[0]
        else:
            return res[1]

#################################################################

    if time:
        output.append("Timeextent:")
        output.append(timeOption(path, name))
        output.append("\n")
    
    if space:
        output.append("Spatialextent:")
        output.append(spaceOption(path, name))
        output.append("\n")

    if hull:
        output.append("Spatialextent as Convex Hull:")
        output.append(polyOption(path, name))
        output.append("\n")

    if not (time or space or hull):
        fext.extractFromFolder(path, clear)
    else:
        if clear:
            click.clear()
        for x in output:
            click.echo(x)

if __name__ == "__main__":
    main()
