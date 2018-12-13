import click
import getBoundingBox as box
import getTimeExtent as timeext
import extractGeoDataFromFolder as fext

# asking for parameters in command line
@click.command()
@click.option('--path', prompt="File path", help='Path to file')
@click.option('-clear', default=False, help='Argument wether you want to display only the Output \nOptions: 1, yes, y and true')
@click.option('-t', 'switch', default=False, flag_value='t', help="execute time extraction for one file")
@click.option('-s', 'switch', default=False, flag_value='s', help="execute boundingbox extraction for one file")
def main(path, clear, switch):
    if switch == 't':
        name = click.prompt("Pleas enter filename")
        res = timeext.getTimeExtent(name, path)
        if clear:
            click.clear()
        if res[0] != None:
            click.echo(res[0])
        else:
            click.echo(res[1])
    
    if switch == 's':
        name = click.prompt("Pleas enter filename")
        res = box.getBoundingBox(name, path)
        if clear:
            click.clear()
        if res[0] != None:
            click.echo(res[0])
        else:
            click.echo(res[1])

    if not switch:
        fext.extractFromFolder(path, clear)

if __name__ == "__main__":
    main()
