# -*- encoding: utf-8 -*-
import os
import subprocess
from abjad.tools import sequencetools
from experimental.tools.scoremanagertools.proxies.DirectoryProxy \
    import DirectoryProxy


class ScoreTemplateDirectoryProxy(DirectoryProxy):

    ### INITIALIZER ###

    def __init__(self, score_package_path=None, session=None):
        score_directory_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            score_package_path)
        filesystem_path = os.path.join(
            score_directory_path, 
            'music',
            'templates',
            )
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
            self._run_asset_proxy(result)

    def _get_score_pdf_file_path(self):
        for file_name in self.list_directory():
            if file_name.endswith('score.pdf'):
                file_path = os.path.join(self.filesystem_path, file_name)
                return file_path

    def _get_score_tex_file_path(self):
        for file_name in self.list_directory():
            if file_name.endswith('score.tex'):
                file_path = os.path.join(self.filesystem_path, file_name)
                return file_path

    def _make_asset_menu_entries(self):
        file_names = self.list_directory()
        file_names = [x for x in file_names if x[0].isalpha()]
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
        if bool(self._get_score_tex_file_path()):
            command_section.append(('typeset score', 't'))
        if bool(self._get_score_pdf_file_path()):
            command_section.append(('view score', 's'))
        return main_menu

    def _run_asset_proxy(
        self,
        filesystem_path,
        ):
        proxy = self.asset_proxy_class(
            filesystem_path=filesystem_path,
            session=self.session,
            )
        proxy._run()

    ### PUBLIC PROPERTIES ###

    @property
    def asset_proxy_class(self):
        r'''Assset proxy class of score template directory proxy.

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
        r'''Interactively edits score template asset.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        proxy = self.asset_proxy_class(
            filesystem_path=filesystem_path,
            session=self.session,
            )
        proxy.interactively_edit()

    def interactively_view_score(self, pending_user_input=None):
        r'''Interactively views score.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        command = 'open {}/*score.pdf'.format(self.filesystem_path)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )

    def typeset_score(self):
        r'''Typesets score.

        Writes PDF to score template directory.

        Returns none.
        '''
        from experimental.tools import scoremanagertools
        score_tex_file_path = self._get_score_tex_file_path()
        proxy = scoremanagertools.proxies.FileProxy(
            filesystem_path=score_tex_file_path,
            session=self.session,
            )
        proxy.typeset_tex_file()

    ### UI MANIFEST ###

    user_input_to_action = DirectoryProxy.user_input_to_action.copy()
    user_input_to_action.update({
        's': interactively_view_score,
        't': typeset_score,
        })
