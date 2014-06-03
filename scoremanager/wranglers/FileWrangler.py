# -*- encoding: utf-8 -*-
import os
from scoremanager.wranglers.Wrangler import Wrangler


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
    def _input_to_method(self):
        superclass = super(FileWrangler, self)
        result = superclass._input_to_method
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
        self._make_files_menu_section(menu)
        return menu

    ### PUBLIC METHODS ###

    def check_every_file(self):
        r'''Checks every file.

        Returns none.
        '''
        paths = self._list_visible_asset_paths()
        invalid_paths = []
        for path in paths:
            file_name = os.path.basename(path)
            if not self._is_valid_directory_entry(file_name):
                invalid_paths.append(path)
        directory = self._get_current_directory()
        directory = os.path.basename(directory)
        messages = []
        if not invalid_paths:
            count = len(paths)
            message = '{} ({} files): OK'.format(directory, count)
            messages.append(message)
        else:
            
            message = '{}:'.format(directory)
            messages.append(message)
            tab = self._io_manager._make_tab()
            for invalid_path in invalid_paths:
                message = tab + invalid_path
                messages.append(message)
        self._io_manager._display(messages)
        return invalid_paths

    def copy_file(self):
        r'''Copies file.

        Returns none.
        '''
        self._copy_asset()

    def make_file(self):
        r'''Makes empty file.

        Returns none.
        '''
        self._make_file(prompt_string='file name')

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