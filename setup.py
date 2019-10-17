from setuptools import setup, find_packages

setup(
	name = "scrapy-compose",
	version = "0.8",
	packages = find_packages(),
	author = "Henry AY",
	author_email = "pyc05079@gmail.com",
	url = "https://github.com/Sphynx-HenryAY/scrapy-compose.git",
	entry_points = {
		"console_scripts": [ 'scrapy-compose = scrapy_compose.cmdline:main' ]
	},
	python_requires = '>=3',
	install_requires = [
		"Scrapy",
		"PyYaml"
	]
)
