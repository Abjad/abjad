# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from experimental.tools.scoremanagertools.proxies.DirectoryProxy \
    import DirectoryProxy


class ExergueDirectoryProxy(DirectoryProxy):

    ### INITIALIZER ###

    def __init__(self, score_package_path=None, session=None):
        score_directory_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            score_package_path)
        filesystem_path = os.path.join(score_directory_path, 'exergue')
        DirectoryProxy.__init__(
            self,
            filesystem_path=filesystem_path,
            session=session,
            )

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            self.interactively_edit_asset(result)

    def _make_asset_menu_entries(self):
        file_names = self.list_directory()
        file_paths = []
        for file_name in file_names:
            file_path = os.path.join(self.filesystem_path, file_name)
            file_paths.append(file_path)
        display_strings = file_names[:]
        menu_entries = []
        if display_strings:
            menu_entries = sequencetools.zip_sequences_cyclically(
                display_strings,
                [None],
                [None],
                file_paths,
                )
        return menu_entries

    def _make_main_menu(self):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        self._main_menu = main_menu
        asset_section = main_menu.make_asset_section()
        main_menu._asset_section = asset_section
        menu_entries = self._make_asset_menu_entries()
        asset_section.menu_entries = menu_entries
        command_section = main_menu.make_command_section()
        command_section.append(('rename', 'ren'))
        return main_menu

    ### PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        r'''Assset proxy class of exergue directory proxy.

        Returns class.
        '''
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.FileProxy

    ### PUBLIC METHODS ###

    def interactively_edit_asset(
        self,
        filesystem_path,
        pending_user_input=None,
        ):
        r'''Interactively edits exergue asset.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        proxy = self.asset_proxy_class(
            filesystem_path=filesystem_path,
            session=self.session,
            )
        proxy.interactively_edit()

    ### UI MANIFEST ###

    user_input_to_action = DirectoryProxy.user_input_to_action.copy()
    user_input_to_action.update({
        })
