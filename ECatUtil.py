import sys
import YoUtil
import ECatConfigUtil
from YoUtil import ecat_excel_util as excel

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


	
def print_usage(cmd=None):
	print('ECatUtil Usage:')
	if cmd!= None:
		print('None valid Command option: ',cmd)
	print('  py ECatUtil cfg_slaves <file> - display the list of slaves in a config file')
	print('  py ECatUtil cfg_full <file> - display a full config display')
	print('  py ECatUtil cfg_xslt_initcmd <file> <excel_file>- build a excel filles with all InitCmd')
	
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

def cmd_slave_name_in_cfg():
	if len(sys.argv) >= 3:
		cfg = ECatConfigUtil.Config(sys.argv[2])
		cfg.load_config()
		slave_list = cfg.get_slaves_names()
		print(slave_list)
	else:
		print_usage()
	

		
if (__name__=='__main__'):
	Main()
	