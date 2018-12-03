from setuptools import setup

setup(
	name='san',
	version='1.0'
	py_modules=['san'],
	install_reuires=[	'Click',],
	entry_points='''
		[console_scripts]
		san=san.cli
		''',
)