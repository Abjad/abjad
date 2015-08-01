# -*- encoding: utf-8 -*-
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
        for file in files[:]:
            if file.startswith('__'):
                files.remove(file)
            elif not file.endswith('.py'):
                files.remove(file)
        files.sort()
        # process files
        for file in files:
            path = os.path.join(current_root, file).replace('.py', '')
            parts = path.split(os.path.sep)
            #object_name = parts[-1]
            module_name = []
            for part in reversed(parts):
                module_name.append(part)
                if part == root_package_name:
                    break
            module_name = '.'.join(reversed(module_name))
            module = importlib.import_module(module_name)
            #module = __import__(module_name, fromlist=['*'])
            yield module