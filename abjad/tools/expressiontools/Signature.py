# -*- coding: utf-8 -*-
import string


class Signature(object):
    r'''Signature decorator.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    _allowable_sections = (
        'back-home-quit',
        'basic',
        'build',
        'build-edit',
        'build-generate',
        'build-interpret',
        'build-open',
        'build-preliminary',
        'definition_file',
        'display navigation',
        'git',
        'global files',
        'illustrate_file',
        'ly',
        'ly & pdf',
        'pdf',
        'navigation',
        'sibling navigation',
        'star',
        'system',
        'tests',
        )

    _navigation_section_names = (
        'back-home-quit',
        'display navigation',
        'comparison',
        'navigation',
        'sibling navigation',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        command_name=None, 
        argument_name=None,
        description=None, 
        directories=None,
        forbidden_directories=(),
        is_hidden=True,
        section=None,
        ):
        assert isinstance(argument_name, (str, type(None)))
        self.argument_name = argument_name
        if command_name is not None:
            assert isinstance(command_name, str), repr(command_name)
        self.command_name = command_name
        self.description = description
        directories = directories or ()
        if isinstance(directories, str):
            directories = (directories,)
        self.directories = directories
        self.forbidden_directories = forbidden_directories
        assert isinstance(is_hidden, bool), repr(is_hidden)
        self.is_hidden = is_hidden
        self.section = section

    ### SPECIAL METHODS ###

    def __call__(self, method):
        r'''Calls command decorator on `method`.

        Returns `method` with metadata attached.
        '''
        method.argument_name = self.argument_name
        method.command_name = self.command_name
        if self.description is not None:
            method.description = self.description
        else:
            method.description = method.__name__.replace('_', ' ')
        method.directories = self.directories
        method.forbidden_directories = self.forbidden_directories
        method.is_hidden = self.is_hidden
        method.is_navigation = self.section in self._navigation_section_names
        method.section = self.section
        return method
