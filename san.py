import sys
import click


@click.group()
def cli():
	pass
	
@click.command()
@click.argument('cmd', default='cfg_full', type=str)
@click.option('-cfg_file', help='cfg file path', type=click.Path())
def config(cmd, cfg_file):
	""" 
	aaa
	bbb
	ccc
	"""
	print('cli cfg=:',cmd)
	print('cfg_file=',cfg_file)

@click.command()
@click.argument('excel',  type=click.Path())
def esi2excel(esi_file):
	print('esi:', esi_file)


cli.add_command(config)
cli.add_command(esi2excel)

	
if __name__ == "__main__":
	
    cli()