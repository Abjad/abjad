# -*- encoding: utf-8 -*-
import os
import shutil
import subprocess
from abjad.tools import systemtools
from abjad.tools import sequencetools
from scoremanager.managers.DirectoryManager \
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
        return 'build manager'

    ### PRIVATE METHODS ###

    def _get_file_path_ending_with(self, string):
        for file_name in self._list_directory():
            if file_name.endswith(string):
                file_path = os.path.join(self.filesystem_path, file_name)
                return file_path

    def _handle_back_cover_menu_result(self, result):
        if result == 'e':
            self._interactively_edit_file_ending_with('back-cover.tex')
        elif result == 'g':
            self.session.io_manager.print_not_yet_implemented()
        elif result == 'pdfv':
            self._interactively_open_file_ending_with('back-cover.pdf')
        elif result == 'ts':
            self._interactively_typeset_file_ending_with('back-cover.tex')

    def _handle_front_cover_menu_result(self, result):
        if result == 'e':
            self._interactively_edit_file_ending_with('front-cover.tex')
        elif result == 'g':
            self.session.io_manager.print_not_yet_implemented()
        elif result == 'pdfv':
            self._interactively_open_file_ending_with('front-cover.pdf')
        elif result == 'ts':
            self._interactively_typeset_file_ending_with('front-cover.tex')

    def _handle_preface_menu_result(self, result):
        if result == 'e':
            self._interactively_edit_file_ending_with('preface.tex')
        elif result == 'g':
            self.session.io_manager.print_not_yet_implemented()
        elif result == 'pdfv':
            self._interactively_open_file_ending_with('preface.pdf')
        elif result == 'ts':
            self._interactively_typeset_file_ending_with('preface.tex')

    def _handle_score_menu_result(self, result):
        if result == 'e':
            self._interactively_edit_file_ending_with('score.tex')
        elif result == 'g':
            self.session.io_manager.print_not_yet_implemented()
        elif result == 'lycp':
            self.interactively_copy_segment_lilypond_files()
        elif result == 'pdfcp':
            self.interactively_copy_segment_pdfs()
        elif result == 'pdfv':
            self._interactively_open_file_ending_with('score.pdf')
        elif result == 'seged':
            self._interactively_edit_file_ending_with('score-segments.ly')
        elif result == 'segly':
            self._interactively_call_lilypond_on_file_ending_with(
                'score-segments.ly')
        elif result == 'segv':
            self._interactively_open_file_ending_with('score-segments.pdf')
        elif result == 'ts':
            self._interactively_typeset_file_ending_with('score.tex')

    def _interactively_call_lilypond_on_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            file_manager = self._get_file_manager(file_path)
            file_manager.interactively_call_lilypond()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self.session.io_manager.proceed(message)

    def _interactively_edit_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            file_manager = self._get_file_manager(file_path)
            file_manager.interactively_edit()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self.session.io_manager.proceed(message)

    def _interactively_open_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            file_manager = self._get_file_manager(file_path)
            file_manager.interactively_open()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self.session.io_manager.proceed(message)

    def _interactively_typeset_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            file_manager = self._get_file_manager(file_path)
            file_manager.interactively_typeset_tex_file()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self.session.io_manager.proceed(message)

    def _make_back_cover_menu(self):
        menu = self.session.io_manager.make_menu(where=self._where)
        command_section = menu.make_command_section()
        command_section.append(('source - edit', 'e'))
        command_section.append(('source - generate', 'g'))
        command_section.append(('source - typeset', 'ts'))
        command_section = menu.make_command_section()
        command_section.append(('pdf - view', 'pdfv'))
        command_section.default_index = len(command_section) - 1
        return menu

    def _make_front_cover_menu(self):
        menu = self.session.io_manager.make_menu(where=self._where)
        command_section = menu.make_command_section()
        command_section.append(('source - edit', 'e'))
        command_section.append(('source - generate', 'g'))
        command_section.append(('source - typeset', 'ts'))
        command_section = menu.make_command_section()
        command_section.append(('pdf - view', 'pdfv'))
        command_section.default_index = len(command_section) - 1
        return menu

    def _make_main_menu(self):
        menu = self.session.io_manager.make_menu(where=self._where)
        command_section = menu.make_command_section()
        command_section.append(('back cover - manage', 'bc'))
        command_section.append(('front cover - manage', 'fc'))
        command_section.append(('preface - manage', 'pf'))
        command_section.append(('score - manage', 'sc'))
        hidden_section = menu.make_command_section(is_hidden=True)
        hidden_section.append(('list directory', 'ls'))
        return menu

    def _make_preface_menu(self):
        menu = self.session.io_manager.make_menu(where=self._where)
        command_section = menu.make_command_section()
        command_section.append(('source - edit', 'e'))
        command_section.append(('source - generate', 'g'))
        command_section.append(('source - typeset', 'ts'))
        command_section = menu.make_command_section()
        command_section.append(('pdf - view', 'pdfv'))
        command_section.default_index = len(command_section) - 1
        return menu

    def _make_score_menu(self):
        menu = self.session.io_manager.make_menu(where=self._where)
        command_section = menu.make_command_section()
        command_section.append(('segment lys - copy', 'lycp'))
        command_section.append(('segment pdfs - copy', 'pdfcp'))
        command_section = menu.make_command_section()
        command_section.append(('segment assembly ly - edit', 'seged'))
        command_section.append(('segment assembly ly - lilypond', 'segly'))
        command_section.append(('segment assembly pdf - view', 'segv'))
        command_section = menu.make_command_section()
        command_section.append(('source - edit', 'e'))
        command_section.append(('source - generate', 'g'))
        command_section.append(('source - typeset', 'ts'))
        command_section = menu.make_command_section()
        command_section.append(('pdf - view', 'pdfv'))
        command_section.default_index = len(command_section) - 1
        return menu

    def _trim_lilypond_file(self, file_path):
        lines = []
        with open(file_path, 'r') as file_pointer:
            found_score_block = False
            for line in file_pointer.readlines()[:-1]:
                if line.startswith(r'\score'):
                    found_score_block = True
                    continue
                if found_score_block:
                    lines.append(line)
        lines = ''.join(lines)
        with open(file_path, 'w') as file_pointer:
            file_pointer.write(lines)

    ### PUBLIC METHODS ###

    def interactively_copy_segment_lilypond_files(
        self,
        pending_user_input=None,
        ):
        r'''Interactively copies segment LilyPond files from segment
        package directories to build directory.

        Trims top-level comments, includes and directives from each LilyPond
        file.

        Trims header and paper block from each LilyPond file.

        Leaves score block in each LilyPond file.

        Returns none.
        '''
        from experimental.tools import scoremanager
        self.session.io_manager._assign_user_input(pending_user_input)
        segments_directory_path = self.session.current_segments_directory_path
        for directory_entry in sorted(os.listdir(segments_directory_path)):
            segment_directory_path = os.path.join(
                segments_directory_path,
                directory_entry,
                )
            if not os.path.isdir(segment_directory_path):
                continue
            source_file_path = os.path.join(
                segment_directory_path,
                'output.ly',
                )
            if not os.path.isfile(source_file_path):
                continue
            score_package_path = self.session.current_score_package_path
            score_name = score_package_path.replace('_', '-')
            directory_entry = directory_entry.replace('_', '-')
            target_file_name = '{}-segment-{}.ly'
            target_file_name = target_file_name.format(
                score_name,
                directory_entry,
                )
            target_file_path = os.path.join(
                self.filesystem_path,
                target_file_name,
                )
            shutil.copyfile(source_file_path, target_file_path)
            self._trim_lilypond_file(target_file_path)
            message = 'Segment {} LilyPond file copied & trimmed.'
            message = message.format(directory_entry)
            self.session.io_manager.display(message)
        self.session.io_manager.proceed('')

    def interactively_copy_segment_pdfs(self, pending_user_input=None):
        r'''Interactively copies segment PDFs from segment
        package directories to build directory.

        Returns none.
        '''
        from experimental.tools import scoremanager
        self.session.io_manager._assign_user_input(pending_user_input)
        segments_directory_path = self.session.current_segments_directory_path
        for directory_entry in sorted(os.listdir(segments_directory_path)):
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
            message = 'Segment {} PDF copied.'
            message = message.format(directory_entry)
            self.session.io_manager.display(message)
        self.session.io_manager.proceed('')

    def manage_back_cover(self, clear=True, cache=False):
        r'''Manages back cover.

        Returns none.
        '''
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb('back cover')
            menu = self._make_back_cover_menu()
            result = menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self._handle_back_cover_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    def manage_front_cover(self, clear=True, cache=False):
        r'''Manages front cover.

        Returns none.
        '''
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb('front cover')
            menu = self._make_front_cover_menu()
            result = menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self._handle_front_cover_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    def manage_preface(self, clear=True, cache=False):
        r'''Manages preface.

        Returns none.
        '''
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb('preface')
            menu = self._make_preface_menu()
            result = menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self._handle_preface_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    def manage_score(self, clear=True, cache=False):
        r'''Manages score.

        Returns none.
        '''
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb('score')
            menu = self._make_score_menu()
            result = menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self._handle_score_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    ### UI MANIFEST ###

    user_input_to_action = DirectoryManager.user_input_to_action.copy()
    user_input_to_action.update({
        'bc': manage_back_cover,
        'fc': manage_front_cover,
        'pf': manage_preface,
        'sc': manage_score,
        })
