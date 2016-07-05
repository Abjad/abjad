# -*- coding: utf-8 -*-
try:
    import ConfigParser as configparser
except ImportError:
    import configparser
from abjad.tools import commandlinetools


class AbjadBookScript(commandlinetools.CommandlineScript):
    r'''Entry point script for abjad-book.

    ::

        >>> from abjad.tools import abjadbooktools
        >>> script = abjadbooktools.AbjadBookScript()
        >>> print(script.formatted_help)
        usage: abjad-book [-h] [--version] [-c] [-o OUTPUT_FILE_PATH] [-s] [-v]
                          [-y STYLESHEET] [-a ASSETS_DIRECTORY]
                          [-l LATEX_ROOT_DIRECTORY] [-g CONFIG]
                          input_file_path [input_file_path ...]
        <BLANKLINE>
        Preprocess LaTeX files with Abjad.
        <BLANKLINE>
        positional arguments:
          input_file_path       LaTeX file to process
        <BLANKLINE>
        optional arguments:
          -h, --help            show this help message and exit
          --version             show program's version number and exit
          -c, --clean           remove all output blocks
          -o OUTPUT_FILE_PATH, --output-file-path OUTPUT_FILE_PATH
                                optional output file path
          -s, --skip-rendering  skip all image rendering and simply execute the code
          -v, --verbose         verbose output
          -y STYLESHEET, --stylesheet STYLESHEET
                                optional LilyPond stylesheet
          -a ASSETS_DIRECTORY, --assets-directory ASSETS_DIRECTORY
                                optional assets directory
          -l LATEX_ROOT_DIRECTORY, --latex-root-directory LATEX_ROOT_DIRECTORY
                                optional LaTeX root directory
          -g CONFIG, --config CONFIG
                                path to config file
        <BLANKLINE>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Entry Points'

    alias = 'book'
    short_description = 'Preprocess LaTeX files with Abjad.'
    version = 3.0

    ### PRIVATE METHODS ###

    def _process_args(self, args):
        from abjad.tools import abjadbooktools
        assets_directory = args.assets_directory
        clean = args.clean
        configuration = self._read_config(args.config)
        input_file_path = args.input_file_path
        latex_root_directory = args.latex_root_directory
        output_file_path = args.output_file_path
        skip_rendering = args.skip_rendering
        stylesheet = args.stylesheet
        verbose = args.verbose
        if 1 < len(input_file_path):
            document_handlers = []
            for path in input_file_path:
                document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
                    input_file_path=path,
                    assets_directory=assets_directory,
                    latex_root_directory=latex_root_directory,
                    )
                document_handlers.append(document_handler)
            for document_handler in document_handlers:
                document_handler(
                    clean=clean,
                    configuration=configuration,
                    skip_rendering=skip_rendering,
                    stylesheet=stylesheet,
                    verbose=verbose,
                    )
        else:
            document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
                input_file_path=input_file_path[0],
                assets_directory=assets_directory,
                latex_root_directory=latex_root_directory,
                )
            document_handler(
                clean=clean,
                configuration=configuration,
                output_file_path=output_file_path,
                skip_rendering=skip_rendering,
                stylesheet=stylesheet,
                verbose=verbose,
                )

    def _read_config(self, config_path):
        configuration = {}
        if config_path is None:
            return configuration
        parser = configparser.ConfigParser()
        parser.read(config_path)
        for section in parser.sections():
            configuration[section] = {}
            for key, value in parser.items(section):
                value = tuple(_.strip() for _ in value.splitlines()
                    if _.strip())
                configuration[section][key] = value
        return configuration

    def _setup_argument_parser(self, parser):
        parser.add_argument(
            'input_file_path',
            nargs='+',
            help='LaTeX file to process',
            )
        parser.add_argument(
            '-c', '--clean',
            action='store_true',
            help='remove all output blocks',
            )
        parser.add_argument(
            '-o', '--output-file-path',
            help='optional output file path',
            )
        parser.add_argument(
            '-s', '--skip-rendering',
            action='store_true',
            help='skip all image rendering and simply execute the code',
            )
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='verbose output',
            )
        parser.add_argument(
            '-y', '--stylesheet',
            help='optional LilyPond stylesheet',
            )
        parser.add_argument(
            '-a', '--assets-directory',
            help='optional assets directory',
            )
        parser.add_argument(
            '-l', '--latex-root-directory',
            help='optional LaTeX root directory',
            )
        parser.add_argument(
            '-g', '--config',
            help='path to config file',
            )
