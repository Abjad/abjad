# -*- encoding: utf-8 -*-
import os
import subprocess
from abjad.tools import sequencetools
from scoremanager.managers.FilesystemAssetManager import FilesystemAssetManager


class DirectoryManager(FilesystemAssetManager):

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        from scoremanager import managers
        superclass = super(DirectoryManager, self)
        superclass.__init__(
            filesystem_path=filesystem_path,
            session=session,
            )
        self._asset_manager_class = managers.FileManager

    ### PRIVATE PROPERTIES ###

    @property
    def _repository_add_command(self):
        return 'cd {} && add'.format(self.filesystem_path)

    ### PRIVATE METHODS ###

    def _get_file_manager(self, file_path):
        from scoremanager import managers
        file_manager = managers.FileManager(
            file_path,
            session=self.session,
            )
        return file_manager

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            self._run_asset_manager(result)

    def _list_directory(self, public_entries_only=False):
        result = []
        if not os.path.exists(self.filesystem_path):
            return result
        if public_entries_only:
            for directory_entry in sorted(os.listdir(self.filesystem_path)):
                if directory_entry[0].isalpha() and \
                    not directory_entry.endswith('.pyc'):
                    result.append(directory_entry)
        else:
            for directory_entry in sorted(os.listdir(self.filesystem_path)):
                if not directory_entry.startswith('.') and \
                    not directory_entry.endswith('.pyc'):
                    result.append(directory_entry)
        return result

    def _make_asset_menu_entries(self):
        file_names = self._list_directory()
        file_names = [x for x in file_names if x[0].isalpha()]
        file_paths = []
        for file_name in file_names:
            file_path = os.path.join(self.filesystem_path, file_name)
            file_paths.append(file_path)
        display_strings = file_names[:]
        menu_entries = []
        if display_strings:
            sequences = [display_strings, [None], [None], file_paths]
            menu_entries = sequencetools.zip_sequences(sequences, cyclic=True)
        return menu_entries

    def _make_empty_asset(self, is_interactive=False):
        if not self.exists():
            os.mkdir(self.filesystem_path)
        self.session.io_manager.proceed(is_interactive=is_interactive)

    def _make_main_menu(self):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        self._main_menu = main_menu
        asset_section = main_menu.make_asset_section()
        main_menu._asset_section = asset_section
        menu_entries = self._make_asset_menu_entries()
        asset_section.menu_entries = menu_entries
        return main_menu

    def _run_asset_manager(
        self,
        filesystem_path,
        ):
        manager = self._asset_manager_class(
            filesystem_path=filesystem_path,
            session=self.session,
            )
        manager._run()

    ### PUBLIC METHODS ###

    def interactively_edit_asset(
        self,
        filesystem_path,
        pending_user_input=None,
        ):
        r'''Interactively edits directory asset.

        Returns none.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
        manager = self._asset_manager_class(
            filesystem_path=filesystem_path,
            session=self.session,
            )
        manager.interactively_edit()

    def interactively_get_filesystem_path(self):
        r'''Interactively gest filesystem path of directory manager.

        Returns none.
        '''
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('directory path')
        result = getter._run()
        if self.session.backtrack():
            return
        self.filesystem_path = result

    def interactively_list_directory(self):
        r'''Interactively lists directory.

        Returns none.
        '''
        lines = []
        for directory_entry in self._list_directory():
            filesystem_path = os.path.join(
                self.filesystem_path, 
                directory_entry,
                )
            if os.path.isdir(filesystem_path):
                line = directory_entry + '/'
            elif os.path.isfile(filesystem_path):
                line = directory_entry
            else:
                raise TypeError(directory_entry)
            lines.append(line)
        self.session.io_manager.display(
            lines,
            capitalize_first_character=False,
            )
        self.session.io_manager.display('')
        self.session.hide_next_redraw = True

    def interactively_run_tests(self, prompt=True):
        r'''Interactively runs tests.

        Returns none.
        '''
        command = 'pytest {}'.format(self.filesystem_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.session.io_manager.display(lines)
        line = 'tests run.'
        self.session.io_manager.proceed(line, is_interactive=prompt)

    ### UI MANIFEST ###

    user_input_to_action = FilesystemAssetManager.user_input_to_action.copy()
    user_input_to_action.update({
        'ls': interactively_list_directory,
        'pytest': interactively_run_tests,
        })
