from setuptools import setup, find_packages

setup(
	name = "scrapy-compose",
	version = "0.8",
	author = "Henry AY",
	author_email = "pyc05079@gmail.com",
	url = "https://github.com/Sphynx-HenryAY/scrapy-compose.git",
	packages = find_packages(),
	classifiers = [
		"Operating System :: OS Independent",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3.5",
		"Framework :: Scrapy",
	],
	python_requires = '>=3.5',
	install_requires = [
		"Scrapy",
		"PyYaml"
	],
	entry_points = {
		"console_scripts": [ 'scrapy-compose = scrapy_compose.cmdline:main' ]
	},
)
