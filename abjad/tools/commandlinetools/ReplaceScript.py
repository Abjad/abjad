import fnmatch
import os
import re
from .CommandlineScript import CommandlineScript


class ReplaceScript(CommandlineScript):
    r'''Replaces text in files recursively.

    ..  shell::

        ajv replace text --help

    Multiple patterns for excluding files or folders can be specified by
    restating the `--without-files` or `--without-dirs` commands:

    ..  code-block:: bash

        abjad$ ajv replace text . foo bar -F *.txt -F *.rst -F *.htm

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    alias = 'replace'
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
                except:
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
            print('FAILED READING: {}'.format(path))
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
