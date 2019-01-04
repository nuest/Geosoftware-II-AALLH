import click
import getBoundingBox as box
import getTimeExtent as timeext
import extractGeoDataFromFolder as fext
import getPolygon as poly

# asking for parameters in command line
@click.command()
@click.option('--path', prompt="Pleas enter path to Folder", help='Path to Folder containing Geofiles')
@click.option('--clear','-c', default=False, is_flag=True, help='Clear screen before showing results')
@click.option('--time', '-t', default=False, is_flag=True, help="execute time extraction for one file")
@click.option('--space', '-s', default=False, is_flag=True, help="execute boundingbox extraction for one file")
@click.option('--hull', '-h', default=False, is_flag=True, help="execute convex-hull extraction for one file")
def main(path, clear, time, space, hull):
    output = []
    if time:
        name = click.prompt("Pleas enter filename")
        res = timeext.getTimeExtent(name, path)
        output.append("Timeextent:")
        if res[0] is not None:
            output.append(res[0])
        else:
            output.append(res[1])
    
    if space:
        if not time:
            name = click.prompt("Pleas enter filename")
        res = box.getBoundingBox(name, path)
        output.append("Spatialextent:")
        if res[0] is not None:
            output.append(res[0])
        else:
            output.append(res[1])

    if hull:
        if not (time or space):
            name = click.prompt("Pleas enter filename")
        res = poly.getPolygon(name, path)
        output.append("Spatialextent as Convex Hull:")
        if res[0] is not None:
            output.append(res[0])
        else:
            output.append(res[1])

    if not (time or space or hull):
        fext.extractFromFolder(path, clear)
    else:
        if clear:
            click.clear()
        for x in output:
            click.echo(x)

if __name__ == "__main__":
    main()
