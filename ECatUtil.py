import sys
import YoUtil
import ECatConfigUtil


def Main():
	print("ECatUtil -> ")
	YoUtil.print_list(sys.argv,1)
	numofParams = len(sys.argv)
	if numofParams > 1:
		cmd = sys.argv[1].lower()
		command_options = {
		'cfg_slaves' : cmd_slave_list_in_cfg,
		
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
	
def cmd_slave_list_in_cfg():
	if len(sys.argv) >= 3:
		cfg = ECatConfigUtil.Config(sys.argv[2])
		cfg.load_config()
		lst = cfg.get_slaves()
		for s in lst:
			s.print(1)
	else:
		print_usage()

		
		
if (__name__=='__main__'):
	Main()
	