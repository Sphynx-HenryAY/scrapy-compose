
import sys
import optparse

from inspect import isclass

from scrapy.cmdline import (
	_run_print_help,
	_run_command,
	_print_commands,
	_print_unknown_command
)

class EntryPoint:

	name = "scrapy-compose"

	from scrapy.commands import ScrapyCommand as BaseCommand

	_action = None
	_cmd = None
	_cmds = None
	_parser = None

	@staticmethod
	def iscommand( obj ):
		BaseCommand = EntryPoint.BaseCommand
		return (
			isclass( obj ) and
			issubclass( obj, BaseCommand ) and
			obj != BaseCommand
		)

	@property
	def action( self ):
		if not self._action:
			argv = self.argv
			if argv and not argv[0].startswith( "-" ):
				self._action = argv.pop( 0 )
		return self._action

	@property
	def commands( self ):
		if not self._cmds:
			from scrapy_compose.utils.load import package as load_package
			cmds = {}
			iscommand = self.iscommand
			load_package(
				"scrapy_compose.commands",
				key = lambda c: (
					iscommand( c ) and
					cmds.update(
						{ c.__module__.split(".")[-1]: c() }
					)
				)
			)
			self._cmds = cmds
		return self._cmds

	@property
	def parser( self ):
		if not self._parser:
			import optparse
			self._parser = optparse.OptionParser(
				conflict_handler = 'resolve',
				formatter = optparse.TitledHelpFormatter(),
			)
		return self._parser

	@property
	def cmd( self ):
		if not self._cmd:
			from scrapy.crawler import CrawlerProcess

			cmd = self.commands[ self.action ]

			settings = self.settings
			settings.setdict( cmd.default_settings, priority = "command" )

			parser = self.parser
			parser.usage = f"{self.name} {self.action} {cmd.syntax()}"
			parser.description = cmd.long_desc()

			cmd.settings = settings
			cmd.add_options( parser )
			cmd.crawler_process = CrawlerProcess(settings)

			self._cmd = cmd
		return self._cmd

	def __init__( self, argv = None, settings = None ):

		from scrapy.utils.project import inside_project, get_project_settings
		from .utils.load import settings as load_settings

		self.argv = ( sys.argv if argv is None else argv )[1:]
		self.inproject = inside_project()

		self.settings = get_project_settings() if settings is None else settings
		self.settings.setdict(
			load_settings( "scrapy_compose.compose_settings" )
			, priority = "default"
		)

	def print_header( self ):
		import scrapy
		if self.inproject:
			print( f"Scrapy {scrapy.__version__} - project: {self.settings['BOT_NAME']}" )
		else:
			print( f"Scrapy {scrapy.__version__} - no active project" )
		print()

	def print_commands( self ):
		self.print_header()

		avl = [
			"\u2718", # cross
			"\u2713", # tick
		]

		inproject = self.inproject

		print(
			f"Usage:\n"
			f"  {self.name} <command> [options] [args]\n"
			f"\n"
			f"Commands:"
		)
		for c_name, cmd in sorted( self.commands.items(), key = lambda x: not x[1].requires_project ): print(
			f"  {c_name:<13s} {avl[inproject or cmd.requires_project]} {cmd.short_desc()}"
		)

	def print_unknown_command( self ):
		self.print_header()
		print(
			f"Unknown command: {self.action}\n"
			'Use "scrapy" to see available commands'
		)

	def __call__( self ):

		action = self.action

		if not action:
			self.print_commands()
			sys.exit(0)

		elif action not in self.commands:
			self.print_unknown_command()
			sys.exit(2)

		settings = self.settings
		cmd = self.cmd
		parser = self.parser

		opts, args = parser.parse_args( args = self.argv )
		_run_print_help(parser, cmd.process_options, args, opts)
		_run_print_help(parser, _run_command, cmd, args, opts)
		sys.exit(cmd.exitcode)

main = EntryPoint()
