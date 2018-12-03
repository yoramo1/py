import sys
import os
import YoUtil
import ECatConfigUtil
from ECatEsiUtil import EsiUtil as EsiUtil
from ECatEsiUtil import EsiFile as EsiFile
from YoUtil import ecat_excel_util as excel
from YoUtil import print_util as pr
import click

#---------------------------------
#click site: https://github.com/pallets/click
#            https://click.palletsprojects.com/en/latest/
#tutorial -  https://dbader.org/blog/mastering-click-advanced-python-command-line-apps
#---------------------------------


@click.group()
def cli():
	pass

@click.command()
@click.argument('cfg_file',  type=click.Path())
@click.option('--excel',help='generate a excel file',type=click.Path())
def config(cfg_file,excel):
	'''  dispay a full config '''
	if os.path.isfile(cfg_file):
		pr1 = pr()
		cfg = ECatConfigUtil.Config(cfg_file)
		cfg.load_config()
		master = cfg.get_master();
		slave_list = cfg.get_slaves()
		str = ''
		if master!=None:
			str += master.tostring(1)
		for s in slave_list:
			str += s.tostring(1)
		pr1.print(str)
		if excel != None:
			generate_excel(cfg, excel)
	else:
		pr.print ('Error: [%s] is not a file '% cfg_file)

@click.command()
@click.argument('cfg_file',  type=click.Path())
def slave_names(cfg_file):
	if os.path.isfile(cfg_file):
		pr1 = pr()
		cfg = ECatConfigUtil.Config(cfg_file)
		cfg.load_config()
		slave_list = cfg.get_slaves_names()
		pr1.print(slave_list)
	pass

def generate_excel(cfg,excel_file):
	slave_list = cfg.get_slaves()
	xlsx = excel()
	xlsx.create_file(excel_file)
	num=0
	for s in slave_list:
		name = s.name_in_res
		if name is None:
			name = 'Slave '+str(num)
		xlsx.append_slave_initCmd(s,name)
		num+=1
	xlsx.close()

@click.command()
@click.option('-vendor',  type=str, default=None)
@click.option('-product',  type=str, default=None)
def find_esi(vendor,product):
	'''
		finds ESI files can fileter by [vendor] and [product]
	'''
	pr1= pr()
	esi = EsiUtil()
	vendor_id = None
	productCode=None
	if vendor!=None:
		vendor_id = YoUtil.get_int(vendor)
	if product!= None:
		productCode = YoUtil.get_int(product)
	files = esi.get_ESI_files(vendor_id,productCode)
	if files != None and len(files)>0:
		YoUtil.print_list(files,1)
	else:
		pr1.print('ESI not found !')
	
@click.command()
@click.argument('esi_path',  type=click.Path())
def esi_devices(esi_path):
	'''
	dispay the devices in a ESI file
	'''
	pr1= pr()
	esi_file = EsiFile(esi_path)
	if esi_file != None:
		esi_file.load_devices()
		for d in esi_file.devices:
			pr1.print('(0x%x,0x%x) - %s' % (d.product_code, d.revision, d.name))
		pass
	else:
		pr1.print('Error loading ESI file')
	pass
	
'''
#can be deprecated
def Main():
	print("ECatUtil -> ")
	#YoUtil.print_list(sys.argv,1)
	numofParams = len(sys.argv)
	if numofParams > 1:
		cmd = sys.argv[1].lower()
		command_options = {
		'cfg_slaves' : cmd_slave_list_in_cfg,
		'cfg_slave_names': cmd_slave_name_in_cfg,
		'cfg_full' : cmd_cfg_full,
		'cfg_xslt_initcmd': cmd_cfg_xslt_initcmd,
		}
		if cmd is None:
			print_usage()
		elif cmd in command_options.keys():
			command_options[cmd]()
		else:
			print_usage(cmd)
	else:
		print_usage()


#can be deprecated	
def print_usage(cmd=None):
	print('ECatUtil Usage:')
	if cmd!= None:
		print('None valid Command option: ',cmd)
	print('  py ECatUtil cfg_slaves <file> - display the list of slaves in a config file')
	print('  py ECatUtil cfg_full <file> - display a full config display')
	print('  py ECatUtil cfg_xslt_initcmd <file> <excel_file>- build a excel filles with all InitCmd')
	
#can be deprecated
def cmd_slave_list_in_cfg():
	if len(sys.argv) >= 3:
		cfg = ECatConfigUtil.Config(sys.argv[2])
		cfg.load_config()
		slave_list = cfg.get_slaves()
		str = ''
		for s in slave_list:
			str += s.tostring(1)
		print(str)
	else:
		print_usage()

#can be deprecated
def cmd_cfg_full():
	if len(sys.argv) >= 3:
		cfg = ECatConfigUtil.Config(sys.argv[2])
		cfg.load_config()
		master = cfg.get_master();
		slave_list = cfg.get_slaves()
		str = ''
		if master!=None:
			str += master.tostring(1)
		for s in slave_list:
			str += s.tostring(1)
		print(str)
	else:
		print_usage()

#can be deprecated		
def cmd_cfg_xslt_initcmd():
	if len(sys.argv) >= 4:
		cfg = ECatConfigUtil.Config(sys.argv[2])
		cfg.load_config()
		master = cfg.get_master();
		slave_list = cfg.get_slaves()
		xlsx = excel()
		xlsx.create_file(sys.argv[3])
		num=0
		for s in slave_list:
			name = s.name_in_res
			if name is None:
				name = 'Slave '+str(num)
			xlsx.append_slave_initCmd(s,name)
			num+=1
		xlsx.close()
	else:
		print_usage()

#can be deprecated
def cmd_slave_name_in_cfg():
	if len(sys.argv) >= 3:
		cfg = ECatConfigUtil.Config(sys.argv[2])
		cfg.load_config()
		slave_list = cfg.get_slaves_names()
		print(slave_list)
	else:
		print_usage()
	
'''
#Add Commands
cli.add_command(config)
cli.add_command(slave_names)
cli.add_command(find_esi)
cli.add_command(esi_devices)

		
if (__name__=='__main__'):
	cli()
	