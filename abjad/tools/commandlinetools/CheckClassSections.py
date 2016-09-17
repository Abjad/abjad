#! /usr/bin/env python
'''
Validate ### ... ### header order and section contents in classes.

Could be extended to check for other similar errors as needed.
'''

import os
import sys
from abjad.tools.commandlinetools.CommandlineScript import CommandlineScript


class CheckClassSections(CommandlineScript):
    r'''Checks the order and contents of class sections in a path.

    .. shell::

        ajv check-class-sections --help

    '''

    ### CLASS VARIABLES ###

    alias = 'check-class-sections'
    short_description = (
        'Check the order and contents of class sections in a path.'
        )
    long_description = ('''
Finds and lists errors in class section order,
as well as cases where methods and properties appear
under incorrect section headers

If no `path` is given, the current directory is searched.

Checks that where they appear in classes, the following
comment headers appear in the given order:

    ### CLASS VARIABLES ###
    ### CONSTRUCTOR ###
    ### INITIALIZER ###
    ### SPECIAL METHODS ###
    ### PRIVATE METHODS ###
    ### PUBLIC METHODS ###
    ### PRIVATE PROPERTIES ###
    ### PUBLIC PROPERTIES ###

Additionally, this finds cases where methods appear
under PROPERTIES sections, and vice-versa.'''
        )

    ### PRIVATE METHODS ###

    def _setup_argument_parser(self, parser):
        parser.add_argument(
            'path',
            default=os.getcwd(),
            help='directory tree to be recursed over',
            nargs='?',
            type=self._validate_path,
            )

    def _process_args(self, args):
        if not args.path:
            check_path = '.'
        else:
            check_path = args.path
        failed_files = 0
        checked_files = 0
        print('Recursively scanning {} for errors...'.format(check_path))
        line_divider = '=' * 79
        for path, dirs, files in os.walk(check_path):
            for f in files:
                test_file = os.path.abspath(os.path.join(path, f))
                # Skip links and non-.py files
                if (os.path.islink(test_file) or
                    (not test_file.endswith('.py'))
                    ):
                    continue
                errors = self._check_class_sections(test_file)
                checked_files += 1
                if any(e for e in errors.values()):
                    failed_files += 1
                    print('Errors in {}:'.format(test_file))
                    for error in errors.items():
                        if not error[1]:
                            continue
                        print('Lines {}: {}'.format(error[1], error[0]))
                        print(line_divider)
        # Done
        print(
            '{} total files checked.\n'
            '{} passed.\n'
            '{} failed.\n'.format(
                checked_files,
                checked_files - failed_files,
                failed_files
                )
            )
        if failed_files:
            sys.exit(1)
        else:
            sys.exit(0)

    @staticmethod
    def _check_class_sections(file_path):
        r'''Check a file for a small subset of code-quality errors.

        Returns a dict of form {'ERROR TYPE': [line_numbers]}.
        '''
        headers = [
            '[no header]',
            '    ### CLASS VARIABLES ###\n',
            '    ### CONSTRUCTOR ###\n',
            '    ### INITIALIZER ###\n',
            '    ### SPECIAL METHODS ###\n',
            '    ### PRIVATE METHODS ###\n',
            '    ### PUBLIC METHODS ###\n',
            '    ### PRIVATE PROPERTIES ###\n',
            '    ### PUBLIC PROPERTIES ###\n'
            ]
        current_header = ''
        current_header_index = 0
        # Dict of error classes with a list of violating line numbers
        errors = {
            'BAD HEADER ORDER': [],
            'PROPERTY IN METHODS SECTION': [],
            'METHOD IN PROPERTIES SECTION': []
            }
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for line_num in range(0, len(lines)):
            if lines[line_num].startswith('    ### '):
                # This looks like a header - compare against known headers
                for header_index, header in enumerate(headers):
                    if lines[line_num] == header:
                        # We recognize this header: check if its order
                        if header_index < current_header_index:
                            errors['BAD HEADER ORDER'].append(line_num)
                        current_header_index = header_index
                        current_header = header
                        break
                else:
                    # Even if we don't recognize this header, we can still
                    # use it when detecting certain out-of-place
                    # methods / properties, so keep track of it
                    current_header_index = 0
                    current_header = lines[line_num]
            # Check that other contents make sense under the last-seen header
            elif 'METHODS' in current_header:
                if (
                    lines[line_num].startswith('    @') and not (
                    # Whitelist known non-property decorators
                    lines[line_num] == '    @staticmethod\n' or
                    lines[line_num] == '    @classmethod\n' or
                    lines[line_num] == '    @abc.abstractmethod\n'
                    )):
                    errors['PROPERTY IN METHODS SECTION'].append(line_num)
            elif 'PROPERTIES' in current_header:
                if (
                    lines[line_num].startswith('    def ') and
                    not lines[line_num - 1].startswith('    @')
                    ):
                    errors['METHOD IN PROPERTIES SECTION'].append(line_num)
            elif lines[line_num].startswith('class '):
                # Reset header after running into a new class
                current_header = '[no header]'
                current_header_index = 0
        return errors
