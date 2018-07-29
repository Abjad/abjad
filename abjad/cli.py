"""
Command-line tools.
"""

import fnmatch
import importlib
import inspect
import os
import pathlib
import re
import shutil
import types
from abjad import utilities
from uqbar.cli import CLI, CLIAggregator


class AbjDevScript(CLIAggregator):
    '''
    Entry-point to the Abjad developer scripts catalog.

    Can be accessed on the commandline via `abj-dev` or `ajv`:

    ..  shell::

        ajv --help

    `ajv` supports subcommands similar to `svn`:

    ..  shell::

        ajv api --help

    '''

    ### CLASS VARIABLES ###

    config_name = '.abjadrc'
    short_description = 'Entry-point to Abjad developer scripts catalog.'

    ### SPECIAL METHODS ###

    @property
    def cli_classes(self):
        """
        Lists CLI classes for aggregation.
        """
        def scan_module(module):
            classes = []
            for name in dir(module):
                obj = getattr(module, name)
                if not isinstance(obj, type):
                    continue
                elif not issubclass(obj, CLI):
                    continue
                elif issubclass(obj, type(self)):
                    continue
                elif inspect.isabstract(obj):
                    continue
                classes.append(obj)
            return classes
        import abjad.cli
        classes = scan_module(abjad.cli)
        try:
            import abjadext  # type: ignore
            for abjadext_path in abjadext.__path__:
                abjadext_path = pathlib.Path(abjadext_path)
                for extension_path in abjadext_path.iterdir():
                    if (
                        extension_path.name.startswith(('.', '_')) or
                        not extension_path.is_dir() or
                        not (extension_path / '__init__.py').exists()
                    ):
                        continue
                    module_name = 'abjadext.{}'.format(extension_path.name)
                    module = importlib.import_module(module_name)
                    classes.extend(scan_module(module))
        except ImportError:
            pass
        classes.sort(key=lambda x: x.__name__)
        return classes


class CleanScript(CLI):
    '''
    Removes *.pyc, *.swp files and __pycache__ and tmp* directories recursively
    in a path.

    ..  shell::

        ajv clean --help

    '''

    ### CLASS VARIABLES ###

    alias = 'clean'
    config_name = '.abjadrc'
    short_description = (
        'Clean *.pyc, *.swp, .cache,  __pycache__ and tmp* '
        'files and folders from PATH.'
        )

    ### PRIVATE METHODS ###

    def _process_args(self, arguments):
        if (
            not arguments.cache and
            not arguments.pyc and
            not arguments.pycache and
            not arguments.swp and
            not arguments.tmp
        ):
            arguments.cache = True,
            arguments.pyc = True
            arguments.pycache = True
            arguments.swp = True
            arguments.tmp = True
        print('Cleaning...')
        if arguments.pyc:
            print('\t*.pyc files')
        if arguments.swp:
            print('\t*.swp files')
        if arguments.cache:
            print('\t.cache directories')
        if arguments.pycache:
            print('\t__pycache__ directories')
        if arguments.tmp:
            print('\ttmp* directories')

        for root_directory, directory_names, file_names in os.walk(
            arguments.path):
            if '.svn' in directory_names:
                directory_names.remove('.svn')
            extensions = ()
            if arguments.pyc:
                extensions += ('.pyc',)
            if arguments.swp:
                extensions += ('.swp',)
            for file_name in file_names:
                if file_name.endswith(extensions):
                    file_path = os.path.join(
                        root_directory,
                        file_name,
                        )
                    os.remove(file_path)
            directories_to_remove = []
            for directory_name in directory_names:
                directory = os.path.join(
                    root_directory,
                    directory_name,
                    )
                should_remove = False
                if arguments.cache:
                    if directory_name == '.cache':
                        should_remove = True
                if arguments.pycache:
                    if directory_name == '__pycache__':
                        should_remove = True
                if arguments.tmp:
                    if directory_name.startswith('tmp'):
                        should_remove = True
                if not os.listdir(directory):
                    should_remove = True
                if should_remove:
                    shutil.rmtree(directory)
                    directories_to_remove.append(directory_name)
            for directory_name in directories_to_remove:
                directory_names.remove(directory_name)

    def _setup_argument_parser(self, parser):
        parser.add_argument(
            'path',
            default=os.getcwd(),
            help='directory tree to be recursed over',
            nargs='?',
            type=self._validate_path,
            )
        parser.add_argument(
            '--cache',
            action='store_true',
            help='delete *.cache folders',
            )
        parser.add_argument(
            '--pyc',
            action='store_true',
            help='delete *.pyc files',
            )
        parser.add_argument(
            '--pycache',
            action='store_true',
            help='delete __pycache__ folders',
            )
        parser.add_argument(
            '--swp',
            action='store_true',
            help='delete Vim *.swp file',
            )
        parser.add_argument(
            '--tmp',
            action='store_true',
            help='delete tmp* folders',
            )


class ReplaceScript(CLI):
    '''
    Replaces text in files recursively.

    ..  shell::

        ajv replace text --help

    Multiple patterns for excluding files or folders can be specified by
    restating the `--without-files` or `--without-dirs` commands:

    ..  code-block:: bash

        abjad$ ajv replace text . foo bar -F *.txt -F *.rst -F *.htm

    '''

    ### CLASS VARIABLES ###

    alias = 'replace'
    config_name = '.abjadrc'
    short_description = 'Replace text.'

    ### PRIVATE METHODS ###

    def _get_naive_search_callable(self, arguments):

        class NaiveSearch(object):

            def __init__(self, pattern):
                self.pattern = pattern

            def __call__(self, line, pos):
                index = line.find(self.pattern, pos)
                if 0 <= index:
                    return index, len(self.pattern)
                return -1, 0

        return NaiveSearch(arguments.old)

    def _get_regex_search_callable(self, arguments):

        class RegexSearch(object):

            def __init__(self, pattern, escaped=False, whole_words_only=False):
                try:
                    if escaped:
                        pattern = re.escape(pattern)
                    if whole_words_only:
                        pattern += r'\b'
                    self.pattern = re.compile(pattern)
                    self.whole_words_only = whole_words_only
                except Exception:
                    message = "can't compile {!r} as a regex pattern."
                    message = message.format(pattern)
                    raise ValueError(message)

            def __call__(self, line, pos):
                start, length = self._search(line, pos)
                if self.whole_words_only and 0 < start:
                    while start != -1 and (
                        line[start - 1].isalnum() or line[start - 1] == '_'):
                        start, length = self._search(line, start + length)
                return start, length

            def _search(self, line, pos):
                match = self.pattern.search(line, pos)
                if match is None:
                    return -1, 0
                return match.start(), match.end() - match.start()

        return RegexSearch(
            arguments.old,
            escaped=not arguments.regex,
            whole_words_only=arguments.whole_words_only,
            )

    def _process_args(self, arguments):
        import abjad
        message = 'Replacing {!r} with {!r} ...'
        message = message.format(arguments.old, arguments.new)
        print(message)
        skipped_dirs_patterns = self.skipped_directories
        skipped_dirs_patterns += arguments.without_dirs
        skipped_files_patterns = self.skipped_files + arguments.without_files
        if (arguments.regex or
            (not arguments.regex and arguments.whole_words_only)
            ):
            arguments.old = self._get_regex_search_callable(arguments)
            index, length = arguments.old('', 0)
            if 0 <= index:
                message = 'regex pattern {!r} matches the empty string.'
                message = message.format(arguments.old.pattern.pattern)
                raise ValueError(message)
        else:
            arguments.old = self._get_naive_search_callable(arguments)
        changed_file_count = 0
        changed_line_count = 0
        changed_item_count = 0
        for root, dirs, files in os.walk(arguments.path):
            dirs_to_remove = []
            for dir in dirs:
                for pattern in skipped_dirs_patterns:
                    if fnmatch.fnmatch(dir, pattern):
                        dirs_to_remove.append(dir)
                        break
            for dir in dirs_to_remove:
                dirs.remove(dir)
            for file in sorted(files):
                valid = True
                for pattern in skipped_files_patterns:
                    if fnmatch.fnmatch(file, pattern):
                        valid = False
                        break
                if not valid:
                    continue
                changed_lines, changed_items = self._process_file(
                    arguments, os.path.join(root, file))
                if changed_lines:
                    changed_file_count += 1
                    changed_line_count += changed_lines
                    changed_item_count += changed_items
        print()
        item_identifier = abjad.String('instance').pluralize(changed_item_count)
        line_identifier = abjad.String('line').pluralize(changed_line_count)
        file_identifier = abjad.String('file').pluralize(changed_file_count)
        message = '\tReplaced {} {} over {} {} in {} {}.'
        message = message.format(
            changed_item_count,
            item_identifier,
            changed_line_count,
            line_identifier,
            changed_file_count,
            file_identifier,
            )
        print(message)

    def _process_file(self, arguments, path):
        changed_items = 0
        changed_lines = 0
        try:
            with open(path, 'r') as f:
                lines = f.read().split('\n')
        except UnicodeDecodeError:
            return changed_lines, changed_items
        results = []
        for i, line in enumerate(lines):
            line, changes = self._process_line(
                line, i, path, arguments.old, arguments.new, arguments.force, arguments.verbose)
            results.append(line)
            if changes:
                changed_items += changes
                changed_lines += 1
        if results != lines:
            with open(path, 'w') as f:
                f.write('\n'.join(results))
        return changed_lines, changed_items

    def _process_line(
        self,
        line,
        line_number,
        file_name,
        search,
        replacement,
        force,
        verbose,
        ):
        index, changes = 0, 0
        index, length = search(line, index)
        while 0 <= index:
            should_replace = False
            replaced_line = line[:index] + replacement + line[index + length:]
            carats = (' ' * index) + ('^' * length)
            if force:
                should_replace = True
                if verbose:
                    print()
                    print('{}: {}'.format(file_name, line_number))
                    print('-{}'.format(line))
                    print('+{}'.format(replaced_line))
            else:
                print()
                print('{}: {}'.format(file_name, line_number))
                print()
                print('{}'.format(line))
                print('{}'.format(carats))
                print()
                result = input('Replace? [Y/n] > ').lower()
                while result not in ('', 'y', 'yes', 'n', 'no'):
                    result = input('Replace? [Y/n] > ').lower()
                if result in ('', 'y', 'yes'):
                    should_replace = True
            if should_replace:
                index += length - (length - len(replacement))
                line = replaced_line
                changes += 1
            else:
                index += length
            index, length = search(line, index)
        return line, changes

    def _setup_argument_parser(self, parser):
        parser.add_argument(
            'path',
            default=os.getcwd(),
            help='directory tree to be recursed over',
            nargs='?',
            type=self._validate_path,
            )
        parser.add_argument(
            'old',
            help='old text',
            )
        parser.add_argument(
            'new',
            help='new text',
            )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='print replacement info even when --force flag is set.',
            )
        parser.add_argument(
            '-Y', '--force',
            action='store_true',
            help='force "yes" to every replacement'
            )
        parser.add_argument(
            '-R', '--regex',
            action='store_true',
            help='treat "old" as a regular expression',
            )
        parser.add_argument(
            '-W', '--whole-words-only',
            action='store_true',
            help='''match only whole words, similar to grep's "-w" flag''',
            )
        parser.add_argument(
            '-F', '--without-files',
            action='append',
            default=[],
            help='Exclude files matching pattern(s)',
            metavar='PATTERN',
            )
        parser.add_argument(
            '-D', '--without-dirs',
            action='append',
            default=[],
            help='Exclude folders matching pattern(s)',
            metavar='PATTERN',
            )

    ### PUBLIC PROPERTIES ###

    @property
    def skipped_directories(self):
        r'''Skipped directories.

        Returns list.
        '''
        return [
            '.svn',
            '.git',
            'build'
            ]

    @property
    def skipped_files(self):
        r'''Skipped files.

        Returns list.
        '''
        return [
            __file__,
            self.program_name,
            '*.ai',
            '*.backup',
            '*.doc',
            '*.docx',
            '*.doctree',
            '*.gif',
            '*.indd',
            '*.indt',
            '*.jpg',
            '*.jpeg',
            '*.mid',
            '*.midi',
            '*.nb',
            '*.pages',
            '*.pdf',
            '*.pickle',
            '*.pkl',
            '*.png',
            '*.ps',
            '*.psd',
            '*.pyc',
            '*.rtf',
            '*.tif',
            '*.tiff',
            '*.txt',
            '*.wav',
            '*.zip',
            '.DS_Store',
            ]


class StatsScript(CLI):
    '''
    Builds statistics about a codebase.

    ..  shell::

        ajv stats  --help

    '''

    ### CLASS VARIABLES ###

    alias = 'stats'
    config_name = '.abjadrc'
    short_description = 'Build statistics about Python modules in PATH.'

    ### PRIVATE METHODS ###

    def _iterate_module(self, module):
        results = []
        for name in dir(module):
            obj = getattr(module, name)
            if not isinstance(obj, (type, types.FunctionType)):
                continue
            elif obj.__module__ != module.__name__:
                continue
            results.append(obj)
        return results

    def _print_results(self, counts):
        template = utilities.String.normalize('''
            Source lines: {source_lines}
            Public classes: {public_classes}
                Unique public methods: {unique_public_methods}
                Unique public properties: {unique_public_properties}
                Unique private methods: {unique_private_methods}
                Unique private properties: {unique_private_properties}
            Public functions: {public_functions}
            Private classes: {private_classes}
            Private functions: {private_functions}
        ''')
        result = template.format(
            source_lines=counts['source_lines'],
            public_classes=counts['public_classes'],
            unique_public_methods=counts['unique_public_methods'],
            unique_public_properties=counts['unique_public_properties'],
            unique_private_methods=counts['unique_private_methods'],
            unique_private_properties=counts['unique_private_properties'],
            public_functions=counts['public_functions'],
            private_classes=counts['private_classes'],
            private_functions=counts['private_functions'],
            )
        print(result)

    def _process_args(self, arguments):
        from abjad import utilities
        path = arguments.path
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        counts = self._setup_counts()
        for module in utilities.yield_all_modules(
            code_root=path,
            ignored_file_names=[],
            ):
            with open(module.__file__, 'r') as file_pointer:
                contents = file_pointer.read()
                counts['source_lines'] += contents.count('\n')
            for obj in self._iterate_module(module):
                if isinstance(obj, types.FunctionType):
                    if obj.__name__.startswith('_'):
                        counts['private_functions'] += 1
                    else:
                        counts['public_functions'] += 1
                elif isinstance(obj, type):
                    if obj.__name__.startswith('_'):
                        counts['private_classes'] += 1
                    else:
                        counts['public_classes'] += 1
                        for attr in inspect.classify_class_attrs(obj):
                            if attr.defining_class != obj:
                                continue
                            if attr.kind in ('method', 'class method', 'static method'):
                                if attr.name.startswith('_'):
                                    counts['unique_private_methods'] += 1
                                else:
                                    counts['unique_public_methods'] += 1
                            elif attr.kind in ('property,'):
                                if attr.name.startswith('_'):
                                    counts['unique_private_properties'] += 1
                                else:
                                    counts['unique_public_properties'] += 1

        self._print_results(counts)

    def _setup_argument_parser(self, parser):
        parser.add_argument(
            'path',
            default=os.getcwd(),
            help='directory tree to be recursed over',
            nargs='?',
            type=self._validate_path,
            )

    def _setup_counts(self):
        counts = {
            'source_lines': 0,
            'private_classes': 0,
            'private_functions': 0,
            'public_classes': 0,
            'public_functions': 0,
            'unique_public_methods': 0,
            'unique_public_properties': 0,
            'unique_private_methods': 0,
            'unique_private_properties': 0,
            }
        return counts


def run_ajv():
    r'''Entry point for setuptools.

    One-line wrapper around AbjDevScript.
    '''
    AbjDevScript()()
