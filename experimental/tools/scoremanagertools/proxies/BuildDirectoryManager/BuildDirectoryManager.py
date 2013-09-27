# -*- encoding: utf-8 -*-
import os
import shutil
import subprocess
from abjad.tools import iotools
from abjad.tools import sequencetools
from experimental.tools.scoremanagertools.proxies.DirectoryManager \
    import DirectoryManager


class BuildDirectoryManager(DirectoryManager):

    ### INITIALIZER ###

    def __init__(self, score_package_path=None, session=None):
        score_directory_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            score_package_path)
        filesystem_path = os.path.join(score_directory_path, 'build')
        DirectoryManager.__init__(
            self,
            filesystem_path=filesystem_path,
            session=session,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'build directory'

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
        command_section.append(('back cover - manage', 'bc'))
        command_section = main_menu.make_command_section()
        if self._get_file_path_ending_with('back-cover.pdf'):
            command_section.append(('back cover - view', 'bcv'))
        if self._get_file_path_ending_with('front-cover.pdf'):
            command_section.append(('front cover - view', 'fcv'))
        if self._get_file_path_ending_with('preface.pdf'):
            command_section.appned(('preface - view', 'p'))
        if self._get_file_path_ending_with('score.pdf'):
            command_section.append(('score - view', 's'))
            command_section.default_index = len(command_section) - 1
        command_section = main_menu.make_command_section()
        command_section.append(('segments - copy ', 'cp'))
        if self._get_file_path_ending_with('score.tex'):
            command_section.append(('score - typeset', 'ts'))
        hidden_section = main_menu.make_command_section(is_hidden=True)
        hidden_section.append(('list directory', 'ls'))
        return main_menu

    ### PUBLIC METHODS ###

    def interactively_copy_segment_pdfs(self, pending_user_input=None):
        r'''Interactively copies segment PDFs from segment
        package directories to build directory.

        Returns none.
        '''
        from experimental.tools import scoremanagertools
        self.session.io_manager.assign_user_input(pending_user_input)
        segments_directory_path = self.session.current_segments_directory_path
        for directory_entry in os.listdir(segments_directory_path):
            segment_directory_path = os.path.join(
                segments_directory_path,
                directory_entry,
                )
            if not os.path.isdir(segment_directory_path):
                continue
            source_file_path = os.path.join(
                segment_directory_path,
                'output.pdf',
                )
            if not os.path.isfile(source_file_path):
                continue
            score_package_path = self.session.current_score_package_path
            directory_entry = directory_entry.replace('_', '-')
            target_file_name = '{}-segment-{}.pdf'
            target_file_name = target_file_name.format(
                score_package_path,
                directory_entry,
                )
            target_file_path = os.path.join(
                self.filesystem_path,
                target_file_name,
                )
            shutil.copyfile(source_file_path, target_file_path)
            message = 'Segment {} copied.'
            message = message.format(directory_entry)
            self.session.io_manager.display(message)
        self.session.io_manager.proceed('')

    def interactively_manage_back_cover(self, pending_user_input=None):
        r'''Interactively manages back cover.

        Returns none.
        '''
        #self.session.io_manager.assign_user_input(pending_user_input)
        self.session.io_manager.print_not_yet_implemented()

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
        proxy = scoremanagertools.proxies.FileManager(
            filesystem_path=score_tex_file_path,
            session=self.session,
            )
        proxy.interactively_typeset_tex_file()

    ### UI MANIFEST ###

    user_input_to_action = DirectoryManager.user_input_to_action.copy()
    user_input_to_action.update({
        'bc': interactively_manage_back_cover,
        'bcv': interactively_view_back_cover,
        'cp': interactively_copy_segment_pdfs,
        'fcv': interactively_view_front_cover,
        'p': interactively_view_preface,
        's': interactively_view_score,
        'ts': typeset_score,
        })
