import codecs
import os
import re

from sys import version_info
from setuptools import setup, find_packages


def read(*parts):
	path = os.path.join(os.path.dirname(__file__), *parts)
	with codecs.open(path, encoding='utf-8') as fobj:
		return fobj.read()

def find_version(*file_paths):
	version_file = read(*file_paths)
	version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
	if version_match:
		return version_match.group(1)
	raise RuntimeError("Unable to find version string.")


install_requires = [
	"Scrapy",
	"pyyaml"
]

if version_info.major == 2:
	install_requires += [
		"backports.functools_lru_cache",
	]


setup(
	name = "scrapy-compose",
	version = find_version( "scrapy_compose", "__init__.py" ),
	description = "Define and run Scrapy without knowing how to write Python.",
	author = "Henry AY",
	author_email = "pyc05079@gmail.com",
	license = "MIT",
	url = "https://github.com/Sphynx-HenryAY/scrapy-compose",
	packages = find_packages(),
	entry_points = {
		"console_scripts": [ 'scrapy-compose = scrapy_compose.cmdline:main' ]
	},
	classifiers = [
		"Framework :: Scrapy",
		"Development Status :: 2 - Pre-Alpha",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: Implementation :: CPython",
		"Topic :: Software Development :: Libraries :: Python Modules",
	],
	python_requires = '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
	install_requires = install_requires,
)
