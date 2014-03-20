# -*- encoding: utf-8 -*-
import os
import subprocess
from abjad.tools import sequencetools
from scoremanager.managers.Manager import Manager


class DirectoryManager(Manager):
    r'''Directory manager.
    '''

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        from scoremanager import managers
        superclass = super(DirectoryManager, self)
        superclass.__init__(
            path=path,
            session=session,
            )
        self._asset_manager_class = managers.FileManager

    ### PRIVATE PROPERTIES ###

    @property
    def _user_input_to_action(self):
        superclass = super(DirectoryManager, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'pwd': self.pwd,
            })
        return result

    ### PRIVATE METHODS ###

    def _get_file_manager(self, file_path):
        from scoremanager import managers
        file_manager = managers.FileManager(
            file_path,
            session=self._session,
            )
        return file_manager

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self._run_asset_manager(result)

    def _list_visible_asset_paths(self):
        file_names = self._list()
        file_names = [x for x in file_names if x[0].isalpha()]
        file_paths = []
        for file_name in file_names:
            file_path = os.path.join(self._path, file_name)
            file_paths.append(file_path)
        return file_paths

    def _make_asset_menu_section(self, menu):
        asset_section = menu.make_asset_section()
        menu._asset_section = asset_section
        menu_entries = self._make_asset_menu_entries()
        for menu_entry in menu_entries:
            asset_section.append(menu_entry)
        return menu

    def _make_empty_asset(self, prompt=False):
        if not os.path.exists(self._path):
            os.makedirs(self._path)
            if self._is_in_git_repository(self._path):
                file_path = os.path.join(self._path, '.gitignore')
                file_pointer = file(file_path, 'w')
                file_pointer.write('')
                file_pointer.close()
        self._io_manager.proceed(prompt=prompt)

    def _make_main_menu(self, name='directory manager'):
        menu = self._io_manager.make_menu(
            where=self._where,
            name=name,
            )
        self._main_menu = menu
        self._make_asset_menu_section(menu)
        return menu

    def _run_asset_manager(
        self,
        path,
        ):
        manager = self._asset_manager_class(
            path=path,
            session=self._session,
            )
        manager._run()

    ### PUBLIC METHODS ###

    def pwd(self):
        '''Displays path of current working directory.

        Returns none.
        '''
        lines = []
        lines.append(self._path)
        lines.append('')
        self._io_manager.display(lines)
        self._session._hide_next_redraw = True