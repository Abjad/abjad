# -*- encoding: utf-8 -*-
import os
from abjad.tools import stringtools
from scoremanager.idetools.Wrangler import Wrangler


class FileWrangler(Wrangler):
    r'''File wrangler.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_extension',
        )

    def __init__(self, session=None):
        superclass = super(FileWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = None
        self._asset_identifier = 'file'
        self._extension = ''
        self._human_readable = False
        self._include_extensions = True
        self._user_storehouse_path = None

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        superclass = super(FileWrangler, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'cp': self.copy_file,
            'new': self.make_file,
            'ren': self.rename_file,
            'rm': self.remove_files,
            #
            'ck*': self.check_every_file,
            })
        return result

    ### PRIVATE METHODS ###

    def _is_valid_directory_entry(self, directory_entry):
        superclass = super(FileWrangler, self)
        if superclass._is_valid_directory_entry(directory_entry):
            name, extension = os.path.splitext(directory_entry)
            if stringtools.is_dash_case(name):
                return True
        return False

    def _make_all_menu_section(self, menu):
        commands = []
        commands.append(('all files - check', 'ck*'))
        commands.append(('all files - repository - add', 'rad*'))
        commands.append(('all files - repository - clean', 'rcn*'))
        commands.append(('all files - repository - commit', 'rci*'))
        commands.append(('all files - repository - revert', 'rrv*'))
        commands.append(('all files - repository - status', 'rst*'))
        commands.append(('all files - repository - update', 'rup*'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='all',
            )

    def _make_files_menu_section(self, menu):
        commands = []
        commands.append(('files - copy', 'cp'))
        commands.append(('files - new', 'new'))
        commands.append(('files - rename', 'ren'))
        commands.append(('files - remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            name='files',
            )

    def _make_main_menu(self):
        superclass = super(FileWrangler, self)
        menu = superclass._make_main_menu()
        self._make_all_menu_section(menu)
        self._make_files_menu_section(menu)
        return menu

    ### PUBLIC METHODS ###

    def check_every_file(self):
        r'''Checks every file.

        Returns none.
        '''
        paths = self._list_asset_paths(valid_only=False)
        paths = [_ for _ in paths if os.path.basename(_)[0].isalpha()]
        paths = [_ for _ in paths if not _.endswith('.pyc')]
        current_directory = self._get_current_directory()
        if current_directory:
            paths = [_ for _ in paths if _.startswith(current_directory)]
        invalid_paths = []
        for path in paths:
            file_name = os.path.basename(path)
            if not self._is_valid_directory_entry(file_name):
                invalid_paths.append(path)
        messages = []
        if not invalid_paths:
            count = len(paths)
            message = '{} ({} files): OK'.format(self._breadcrumb, count)
            messages.append(message)
        else:
            message = '{}:'.format(self._breadcrumb)
            messages.append(message)
            identifier = 'file'
            count = len(invalid_paths)
            identifier = stringtools.pluralize(identifier, count)
            message = '{} unrecognized {} found:'
            message = message.format(count, identifier)
            tab = self._io_manager._tab
            message = tab + message
            messages.append(message)
            for invalid_path in invalid_paths:
                message = tab + tab + invalid_path
                messages.append(message)
        self._io_manager._display(messages)
        missing_files, missing_directories = [], []
        return messages, missing_files, missing_directories

    def copy_file(self):
        r'''Copies file.

        Returns none.
        '''
        self._copy_asset()

    def make_file(self):
        r'''Makes empty file.

        Returns none.
        '''
        self._make_file(message='file name')

    def remove_files(self):
        r'''Removes one or more files.

        Returns none.
        '''
        self._remove_assets()

    def rename_file(self):
        r'''Renames file.

        Returns none.
        '''
        self._rename_asset()