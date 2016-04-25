#! /usr/bin/env python
import os
from abjad.tools import systemtools


def iterate():
    for directory, subdirectory_names, file_names in os.walk('.'):
        for file_name in file_names:
            if file_name.endswith(('.py', '.ly', '.raw', '.rst')):
                file_path = os.path.join(directory, file_name)
                yield file_path


def ensure_source_file_terminal_blank_lines():
    total_source_file_names_without_blank_lines = 0
    for file_path in iterate():
        with open(file_path, 'r') as file_pointer:
            contents = file_pointer.read()
            if not contents:
                continue
            elif contents[-1] == '\n':
                continue
            total_source_file_names_without_blank_lines += 1
            contents = '{}\n'.format(contents)
            with open(file_path, 'w') as file_pointer:
                file_pointer.write(contents)
    message = 'Total source file_names with terminal blank lines: {}'
    message = message.format(total_source_file_names_without_blank_lines)
    print(message)
    print()


if __name__ == '__main__':
    systemtools.IOManager.clear_terminal()
    print('Ensuring source file-terminal blank lines ...')
    print()
    ensure_source_file_terminal_blank_lines()
