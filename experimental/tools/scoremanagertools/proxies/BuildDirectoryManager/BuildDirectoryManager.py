# -*- encoding: utf-8 -*-
import os
import subprocess
from abjad.tools import iotools
from abjad.tools import sequencetools
from experimental.tools.scoremanagertools.proxies.DirectoryProxy \
    import DirectoryProxy


class BuildDirectoryManager(DirectoryProxy):

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

    def _get_file_path_ending_with(self, string):
        for file_name in self.list_directory():
            if file_name.endswith(string):
                file_path = os.path.join(self.filesystem_path, file_name)
                return file_path

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

    def _make_main_menu(self):
        superclass = super(BuildDirectoryManager, self)
        main_menu = superclass._make_main_menu()
        command_section = main_menu.make_command_section()
        if self._get_file_path_ending_with('back-cover.pdf'):
            command_section.append(('back cover - view', 'bc'))
        if self._get_file_path_ending_with('front-cover.pdf'):
            command_section.append(('front cover - view', 'fc'))
        if self._get_file_path_ending_with('preface.pdf'):
            command_section.appned(('preface - view', 'p'))
        if self._get_file_path_ending_with('score.pdf'):
            command_section.append(('score - view', 's'))
            command_section.default_index = len(command_section) - 1
        command_section = main_menu.make_command_section()
        if self._get_file_path_ending_with('score.tex'):
            command_section.append(('typeset score', 't'))
        return main_menu

    ### PUBLIC METHODS ###

    def interactively_view_back_cover(self, pending_user_input=None):
        r'''Interactively views back cover.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        file_path = self._get_file_path_ending_with('back-cover.pdf')
        iotools.open_file(file_path)

    def interactively_view_front_cover(self, pending_user_input=None):
        r'''Interactively views front cover.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        file_path = self._get_file_path_ending_with('front-cover.pdf')
        iotools.open_file(file_path)

    def interactively_view_preface(self, pending_user_input=None):
        r'''Interactively views preface.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        file_path = self._get_file_path_ending_with('preface.pdf')
        iotools.open_file(file_path)

    def interactively_view_score(self, pending_user_input=None):
        r'''Interactively views score.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        file_path = self._get_file_path_ending_with('score.pdf')
        iotools.open_file(file_path)

    def typeset_score(self):
        r'''Typesets score.

        Writes PDF to build directory.

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
        'bc': interactively_view_back_cover,
        'fc': interactively_view_front_cover,
        'p': interactively_view_preface,
        's': interactively_view_score,
        't': typeset_score,
        })
