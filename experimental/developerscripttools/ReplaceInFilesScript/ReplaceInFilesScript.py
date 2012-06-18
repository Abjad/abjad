from experimental.developerscripttools.DirectoryScript import DirectoryScript
import fnmatch
import os


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
            '*.gif',
            '*.jpg',
            '*.jpeg',
            '*.ly',
            '*.nb',
            '*.pdf',
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

        old, new = args.old, args.new
        length = len(args.old)
        difference = len(args.old) - len(args.new)
        changed_lines = 0

        with open(path, 'r') as f:
            lines = f.read().split('\n')

        results = []
        for i, line in enumerate(lines):


            changed = False
            index = line.find(old)
            while 0 <= index:

                if args.force:
                    line = line[:index] + new + line[index+length:]
                    index += length - difference
                    changed = True

                else:
                    carats = (' ' * index) + ('^' * length)
                    print ''
                    print '{}: {}'.format(path, i)
                    print '{}'.format(line)
            	    print '{}'.format(carats)
                    print ''
                    result = raw_input('Replace? [Y/n] > ').lower()
                    while result not in ('', 'y', 'yes', 'n', 'no'):
                        result = raw_input('Replace? [Y/n] > ').lower()
                    if result in ('', 'y', 'yes'):
                        line = line[:index] + new + line[index+length:]
                        index += length - difference
                        changed = True
                    else:
                        index += length

                index = line.find(old, index)

            results.append(line)
            if changed:
                changed_lines += 1

            if results != lines:
                with open(path, 'w') as f:
                    f.write('\n'.join(results))

        return changed_lines

    ### PUBLIC METHODS ###

    def process_args(self, args):

        print 'Replacing {!r} with {!r}...'.format(args.old, args.new)

        skipped_dirs_patterns = self.skipped_directories + args.without_dirs
        skipped_files_patterns = self.skipped_files + args.without_files

        changed_file_count = 0
        changed_line_count = 0

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

                changed_lines = self._process_file(args, os.path.join(root, file))
                if changed_lines:
                    changed_file_count += 1
                    changed_line_count += changed_lines

        print ''
        print 'Changed {} lines in {} files.'.format(changed_line_count, changed_file_count)

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
