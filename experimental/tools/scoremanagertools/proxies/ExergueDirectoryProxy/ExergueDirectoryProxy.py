# -*- encoding: utf-8 -*-
import os
import subprocess
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
        superclass = super(ExergueDirectoryProxy, self)
        main_menu = superclass._make_main_menu()
        command_section = main_menu.make_command_section()
        if bool(self._get_score_tex_file_path()):
            command_section.append(('typeset score', 't'))
        if bool(self._get_score_pdf_file_path()):
            command_section.append(('view score', 's'))
        return main_menu

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

        Writes PDF to exergue directory.

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
