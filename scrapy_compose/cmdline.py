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
			inproject = self.inproject
			load_package(
				"scrapy_compose.commands",
				key = lambda c: (
					iscommand( c ) and
					( inproject or not c.requires_project ) and
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
			parser.usage = " ".join([ self.name, self.action, cmd.syntax() ])
			parser.description = cmd.long_desc()

			cmd.settings = settings
			cmd.add_options( parser )
			cmd.crawler_process = CrawlerProcess(settings)

			self._cmd = cmd
		return self._cmd

	def __init__( self, argv = None, settings = None ):

		from scrapy.utils.project import inside_project, get_project_settings

		self.argv = ( sys.argv if argv is None else argv )[1:]
		self.inproject = inside_project()

		self.settings = get_project_settings() if settings is None else settings
		self.settings.setmodule(
			"scrapy_compose.compose_settings"
			, priority = "default"
		)

	def print_header( self ):
		import scrapy
		p_str = "Scrapy " + scrapy.__version__ + " - "
		if self.inproject:
			p_str += "project : " + self.settings['BOT_NAME']
		else:
			p_str += "no active project"
		print( "" )

	def print_commands( self ):
		self.print_header()

		print("Usage:")
		print("  " + self.name + " <command> [options] [args]\n")
		print("Available commands:")
		for c_name, cmd in sorted( self.commands.items() ):
			print( "  %-13s %s" % ( c_name, cmd.short_desc() ) )

		if not self.inproject:
			print( "" )
			print( "  [ more ]      More commands available when run from project directory" )

		print( "" )
		print( 'Use "scrapy <command> -h" to see more info about a command' )

	def print_unknown_command( self ):
		self.print_header()
		print( "Unknown or unavailable command: " + self.action )
		print( 'Use "scrapy-compose" to see available commands' )

	def __call__( self ):

		action = self.action

		if not action:
			self.print_commands()
			sys.exit(0)

		elif (
				action not in self.commands or
				not self.inproject and self.cmd.requires_project
			):
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
