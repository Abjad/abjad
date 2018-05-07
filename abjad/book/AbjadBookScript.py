import configparser
from uqbar.cli import CLI


class AbjadBookScript(CLI):
    '''
    Entry point script for abjad-book.

    ..  shell::

        ajv book --help

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Entry Points'
    alias = 'book'
    config_name = '.abjadrc'
    short_description = 'Preprocess LaTeX files with Abjad.'
    version = 3.0

    ### PRIVATE METHODS ###

    def _process_args(self, arguments):
        import abjad.book
        assets_directory = arguments.assets_directory
        clean = arguments.clean
        configuration = self._read_config(arguments.config)
        input_file_path = arguments.input_file_path
        latex_root_directory = arguments.latex_root_directory
        output_file_path = arguments.output_file_path
        skip_rendering = arguments.skip_rendering
        stylesheet = arguments.stylesheet
        verbose = arguments.verbose
        if 1 < len(input_file_path):
            document_handlers = []
            for path in input_file_path:
                document_handler = abjad.book.LaTeXDocumentHandler.from_path(
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
            document_handler = abjad.book.LaTeXDocumentHandler.from_path(
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
                value = tuple(
                    _.strip() for _ in value.splitlines()
                    if _.strip()
                    )
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
