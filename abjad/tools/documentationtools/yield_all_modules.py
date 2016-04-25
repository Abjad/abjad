# -*- coding: utf-8 -*-
import importlib
import os


def yield_all_modules(
    code_root=None,
    ignored_directory_names=(
        '__pycache__',
        '.git',
        '.svn',
        'test',
        'docs',
        ),
    ignored_file_names=(
        '__init__.py',
        ),
    root_package_name=None,
    visit_private_modules=False,
    ):
    r'''Yields all modules encountered in `code_root whose name begins with
    `root_package_name`.

    Returns generator.
    '''
    from abjad import abjad_configuration
    if code_root is None:
        code_root = abjad_configuration.abjad_directory
    assert os.path.exists(code_root)
    if not os.path.exists(os.path.join(code_root, '__init__.py')):
        message = '{} is not a Python package directory.'
        message = message.format(code_root)
        raise ValueError(message)
    code_root = os.path.abspath(code_root)
    if root_package_name is None:
        parts = code_root.split(os.path.sep)
        root_package_name = parts[-1]
        while os.path.exists(os.path.join(
            os.path.sep.join(parts), '__init__.py')):
            root_package_name = parts.pop()
    visit_private_modules = bool(visit_private_modules)
    for current_root, directories, files in os.walk(code_root):
        # filter directories
        for directory in directories[:]:
            if directory in ignored_directory_names:
                directories.remove(directory)
            elif (directory.startswith('_') and
                not visit_private_modules):
                directories.remove(directory)
            elif not os.path.exists(os.path.join(
                current_root, directory, '__init__.py')):
                directories.remove(directory)
        directories.sort()
        # filter files
        for file_name in files[:]:
            if file_name in ignored_file_names:
                files.remove(file_name)
            elif not file_name.endswith('.py'):
                files.remove(file_name)
        files.sort()
        # process files
        for file_name in files:
            if file_name == '__init__.py':
                path = current_root
            else:
                path = os.path.join(current_root, file_name).replace('.py', '')
            parts = path.split(os.path.sep)
            module_name = []
            for part in reversed(parts):
                module_name.append(part)
                if part == root_package_name:
                    break
            module_name = '.'.join(reversed(module_name))
            module = importlib.import_module(module_name)
            #module = __import__(module_name, fromlist=['*'])
            yield module
