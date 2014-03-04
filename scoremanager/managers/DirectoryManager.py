# -*- encoding: utf-8 -*-
import os
import subprocess
from abjad.tools import sequencetools
from scoremanager.managers.Manager import Manager


class DirectoryManager(Manager):

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

#    @property
#    def _repository_add_command(self):
#        return 'cd {} && add'.format(self._path)

    @property
    def _user_input_to_action(self):
        superclass = super(DirectoryManager, self)
        _user_input_to_action = superclass._user_input_to_action
        _user_input_to_action = _user_input_to_action.copy()
        _user_input_to_action.update({
#            'ls': self.list,
#            'll': self.list_long,
            'pwd': self.pwd,
            })
        return _user_input_to_action

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
        else:
            self._run_asset_manager(result)

    def _make_asset_menu_entries(self):
        file_names = self._list()
        file_names = [x for x in file_names if x[0].isalpha()]
        file_paths = []
        for file_name in file_names:
            file_path = os.path.join(self._path, file_name)
            file_paths.append(file_path)
        display_strings = file_names[:]
        menu_entries = []
        if display_strings:
            sequences = [display_strings, [None], [None], file_paths]
            menu_entries = sequencetools.zip_sequences(sequences, cyclic=True)
        return menu_entries

    def _make_empty_asset(self, prompt=False):
        if not self.exists():
            os.mkdir(self._path)
        self._io_manager.proceed(prompt=prompt)

    def _make_main_menu(self):
        main_menu = self._io_manager.make_menu(where=self._where)
        self._main_menu = main_menu
        asset_section = main_menu.make_asset_section()
        main_menu._asset_section = asset_section
        menu_entries = self._make_asset_menu_entries()
        asset_section.menu_entries = menu_entries
        return main_menu

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
