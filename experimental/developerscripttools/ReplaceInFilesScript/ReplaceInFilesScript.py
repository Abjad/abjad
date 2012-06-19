from experimental.developerscripttools.DirectoryScript import DirectoryScript
import fnmatch
import os
import re


class ReplaceInFilesScript(DirectoryScript):

    ### PUBLIC READ-ONLY ATTRIBUTES ###

    @property
    def alias(self):
        return 'text'

    @property
    def skipped_files(self):
        return [
            __file__,
            self.program_name,
            '*.doctree',
            '*.gif',
            '*.jpg',
            '*.jpeg',
            '*.ly',
            '*.nb',
            '*.pdf',
            '*.pickle',
            '*.pkl',
            '*.png',
            '*.ps',
            '*.pyc',
            '*.rtf',
            '*.tex',
            '*.txt',
        ]

    @property
    def skipped_directories(self):
        return [
            '.svn',
        ]

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'replace'

    @property
    def short_description(self):
        return 'Replace text.'

    @property
    def version(self):
        return 1.0

    ### PRIVATE METHODS ###

    def _process_file(self, args, path):

        changed_items = 0
        changed_lines = 0

        with open(path, 'r') as f:
            lines = f.read().split('\n')

        results = []
        for i, line in enumerate(lines):
            line, changes = self._process_line(line, i, path, args.old, args.new, args.force)
            results.append(line)
            if changes:
                changed_items += changes
                changed_lines += 1

        if results != lines:
            with open(path, 'w') as f:
                f.write('\n'.join(results))

        return changed_lines, changed_items

    def _process_line(self, line, line_number, filename, search, replacement, force):
        index, changes = 0, 0
        index, length = search(line, index)

        while 0 <= index:

            should_replace = False
            if force:
                should_replace = True
            else:
                carats = (' ' * index) + ('^' * length)
                print ''
                print '{}: {}'.format(filename, line_number)
                print ''
                print '{}'.format(line)
                print '{}'.format(carats)
                print ''
                result = raw_input('Replace? [Y/n] > ').lower()
                while result not in ('', 'y', 'yes', 'n', 'no'):
                    result = raw_input('Replace? [Y/n] > ').lower()
                if result in ('', 'y', 'yes'):
                    should_replace = True

            if should_replace:
                line = line[:index] + replacement + line[index+length:]
                index += length - (length - len(replacement))
                changes += 1
            else:
                index += length

            index, length = search(line, index)

        return line, changes

    def _get_naive_search_callable(self, old):
        class NaiveSearch(object):
            def __init__(self, pattern):
                self.pattern = pattern
            def __call__(self, line, pos):
                index = line.find(self.pattern, pos)
                if 0 <= index:
                    return index, len(self.pattern)
                return -1, 0
        return NaiveSearch(old)

    def _get_regex_search_callable(self, old):
        class RegexSearch(object):
            def __init__(self, pattern):
                try:
                    self.pattern = re.compile(pattern)
                except:
                    raise ValueError("Can't compile {!r} as a regex pattern.".format(pattern))
            def __call__(self, line, pos):
                match = self.pattern.search(line, pos)
                if match is None:
                    return -1, 0
                return match.start(), match.end() - match.start()
        return RegexSearch(old)

    ### PUBLIC METHODS ###

    def process_args(self, args):

        print 'Replacing {!r} with {!r}...'.format(args.old, args.new)

        skipped_dirs_patterns = self.skipped_directories + args.without_dirs
        skipped_files_patterns = self.skipped_files + args.without_files

        if args.regex:
            args.old = self._get_regex_search_callable(args.old)
            index, length = args.old('', 0)
            if 0 <= index:
                raise ValueError('Regex pattern {!r} matches the empty string.'.format(args.old.pattern.pattern))
        else:
            args.old = self._get_naive_search_callable(args.old)

        changed_file_count = 0
        changed_line_count = 0
        changed_item_count = 0

        for root, dirs, files in os.walk(args.path):

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

                changed_lines, changed_items = self._process_file(args, os.path.join(root, file))
                if changed_lines:
                    changed_file_count += 1
                    changed_line_count += changed_lines
                    changed_item_count += changed_items

        print ''
        print 'Replaces {} instances over {} lines in {} files.'.format(
            changed_item_count, changed_line_count, changed_file_count)

    def setup_argument_parser(self, parser):

        parser.add_argument('path',
            type=self._validate_path,
            help='directory tree to be recursed over'
            )

        parser.add_argument('old',
            help='old text',
            )

        parser.add_argument('new',
            help='new text',
            )

        parser.add_argument('--force',
            action='store_true',
            help='force "yes" to every replacement'
            )

        parser.add_argument('--regex',
            action='store_true',
            help='treat "old" as a regular expression',
            )

        parser.add_argument('-WF', '--without-files',
            action='append',
            default=[],
            help='Exclude files matching pattern(s)',
            metavar='PATTERN',
            )

        parser.add_argument('-WD', '--without-dirs',
            action='append',
            default=[],
            help='Exclude folders matching pattern(s)',
            metavar='PATTERN',
            )
