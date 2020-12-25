from setuptools import setup

setup(
	name='CopyTextFromImage',
	packages=['CopyTextFromImage'],
	entry_points={
		'console_scripts' : [
			'ctfi = CopyTextFromImage.ctfi:main'
		]
	},
	include_package_data=True,
	install_requires=[
		'clipboard',
		'pytesseract',
		'Pillow',
		'pynput',
		'pywin32'
	]
)