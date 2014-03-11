# -*- encoding: utf-8 -*-
import os
import shutil
import subprocess
from abjad.tools import sequencetools
from abjad.tools import systemtools
from scoremanager.managers.DirectoryManager import DirectoryManager


class BuildDirectoryManager(DirectoryManager):
    r'''Build directory manager.
    '''

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        if path is not None:
            assert path.endswith('build')
        DirectoryManager.__init__(
            self,
            path=path,
            session=session,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'build manager'

    @property
    def _user_input_to_action(self):
        superclass = super(BuildDirectoryManager, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'bce': self.edit_back_cover_latex,
            'bcg': self.generate_back_cover_latex,
            'bct': self.typeset_back_cover_latex,
            'bcv': self.view_back_cover_pdf,
            'fce': self.edit_front_cover_latex,
            'fcg': self.generate_front_cover_latex,
            'fct': self.typeset_front_cover_latex,
            'fcv': self.view_front_cover_pdf,
            'pfe': self.edit_preface_latex,
            'pfg': self.generate_preface_latex,
            'pft': self.typeset_preface_latex,
            'pfv': self.view_preface_pdf,
            'se': self.edit_score_latex,
            'sg': self.generate_score_latex,
            'st': self.typeset_score_latex,
            'sv': self.view_score_pdf,
            'lycp': self.copy_segment_lilypond_files,
            'pdfcp': self.copy_segment_pdfs,
            'sege': self.edit_segment_assembly_lilypond_file,
            'segly': self.interpret_segment_assembly_lilypond_file,
            'segv': self.view_segment_assembly_pdf,
            })
        return result

    ### PRIVATE METHODS ###

    def _call_lilypond_on_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            file_manager = self._get_file_manager(file_path)
            file_manager.call_lilypond()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager.proceed(message)

    def _edit_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            file_manager = self._get_file_manager(file_path)
            file_manager.edit()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager.proceed(message)

    def _get_file_path_ending_with(self, string):
        for file_name in self._list():
            if file_name.endswith(string):
                file_path = os.path.join(self._path, file_name)
                return file_path

    def _make_back_cover_menu_section(self, menu):
        section = menu.make_command_section(name='back cover')
        section.append(('back cover latex - edit', 'bce'))
        section.append(('back cover latex - generate', 'bcg'))
        section.append(('back cover latex - typeset', 'bct'))
        section.append(('back cover pdf - view', 'bcv'))
        return menu

    def _make_front_cover_menu_section(self, menu):
        section = menu.make_command_section(name='front cover')
        section.append(('front cover latex - edit', 'fce'))
        section.append(('front cover latex - generate', 'fcg'))
        section.append(('front cover latex - typeset', 'fct'))
        section.append(('front cover pdf - view', 'fcv'))
        return section

    def _make_main_menu(self):
        menu = self._io_manager.make_menu(where=self._where)
        self._make_back_cover_menu_section(menu)
        self._make_directory_menu_section(menu, is_permanent=True)
        self._make_front_cover_menu_section(menu)
        self._make_preface_menu_section(menu)
        self._make_score_menu_sections(menu)
        return menu

    def _make_preface_menu_section(self, menu):
        section = menu.make_command_section(name='preface')
        section.append(('preface latex - edit', 'pfe'))
        section.append(('preface latex - generate', 'pfg'))
        section.append(('preface latex - typeset', 'pft'))
        section.append(('preface pdf - view', 'pfv'))
        return menu

    def _make_score_menu_sections(self, menu):
        section = menu.make_command_section(name='segments?')
        section.append(('segment lys - copy', 'lycp'))
        section.append(('segment pdfs - copy', 'pdfcp'))
        section = menu.make_command_section(name='segment assembly?')
        section.append(('segment assembly ly - edit', 'sege'))
        section.append(('segment assembly ly - lilypond', 'segly'))
        section.append(('segment assembly pdf - view', 'segv'))
        section = menu.make_command_section(name='score')
        section.append(('score latex - edit', 'se'))
        section.append(('score latex - generate', 'sg'))
        section.append(('score latex - typeset', 'st'))
        section.append(('score pdf - view', 'sv'))
        return menu

    def _open_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            file_manager = self._get_file_manager(file_path)
            file_manager.open()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager.proceed(message)

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

    def _typeset_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            file_manager = self._get_file_manager(file_path)
            file_manager.typeset_tex_file()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager.proceed(message)

    ### PUBLIC METHODS ###

    def copy_segment_lilypond_files(
        self,
        pending_user_input=None,
        ):
        r'''Copies segment LilyPond files from segment
        package directories to build directory.

        Trims top-level comments, includes and directives from each LilyPond
        file.

        Trims header and paper block from each LilyPond file.

        Leaves score block in each LilyPond file.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        segments_directory_path = self._session.current_segments_directory_path
        build_directory_path = self._session.current_build_directory_path
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
            score_path = self._session.current_score_directory_path
            score_package = self._configuration.path_to_package_path(
                score_path)
            score_name = score_package.replace('_', '-')
            directory_entry = directory_entry.replace('_', '-')
            target_file_name = '{}-{}.ly'
            target_file_name = target_file_name.format(
                score_name,
                directory_entry,
                )
            target_file_path = os.path.join(
                self._path,
                target_file_name,
                )
            if not os.path.exists(build_directory_path):
                os.mkdir(build_directory_path)
            shutil.copyfile(source_file_path, target_file_path)
            self._trim_lilypond_file(target_file_path)
            message = 'segment {} LilyPond file copied & trimmed.'
            message = message.format(directory_entry)
            self._io_manager.display(message)
        self._io_manager.proceed('')

    def copy_segment_pdfs(self, pending_user_input=None):
        r'''Copies segment PDFs from segment
        package directories to build directory.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        segments_directory_path = self._session.current_segments_directory_path
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
            score_package_path = self._session.current_score_package_path
            directory_entry = directory_entry.replace('_', '-')
            target_file_name = '{}-segment-{}.pdf'
            target_file_name = target_file_name.format(
                score_package_path,
                directory_entry,
                )
            target_file_path = os.path.join(
                self._path,
                target_file_name,
                )
            shutil.copyfile(source_file_path, target_file_path)
            message = 'Segment {} PDF copied.'
            message = message.format(directory_entry)
            self._io_manager.display(message)
        self._io_manager.proceed('')

    def edit_back_cover_latex(self):
        r'''Edits back cover LaTeX file.

        Returns none.
        '''
        self._edit_file_ending_with('back-cover.tex')

    def edit_front_cover_latex(self):
        r'''Edits front cover LaTeX file.

        Returns none.
        '''
        self._edit_file_ending_with('front-cover.tex')

    def edit_preface_latex(self):
        r'''Edits preface LaTeX file.

        Returns none.
        '''
        self._edit_file_ending_with('preface.tex')

    def edit_score_latex(self):
        r'''Edits score LaTeX file.

        Returns none.
        '''
        self._edit_file_ending_with('score.tex')

    def edit_segment_assembly_lilypond_file(self):
        r'''Edits segment assembly LilyPond file.

        Returns none.
        '''
        self._edit_file_ending_with('score-segments.ly')

    def generate_back_cover_latex(self):
        r'''Generates back cover LaTeX file.

        Returns none.
        '''
        self._io_manager.print_not_yet_implemented()

    def generate_front_cover_latex(self):
        r'''Generates front cover LaTeX file.

        Returns none.
        '''
        self._io_manager.print_not_yet_implemented()

    def generate_preface_latex(self):
        r'''Generates preface LaTeX file.

        Returns none.
        '''
        self._io_manager.print_not_yet_implemented()

    def generate_score_latex(self):
        r'''Generates score LaTeX file.

        Returns none.
        '''
        self._io_manager.print_not_yet_implemented()

    def interpret_segment_assembly_lilypond_file(self):
        r'''Interprets segment assembly LilyPond file.

        Returns none.
        '''
        self._call_lilypond_on_file_ending_with('score-segments.ly')

    def typeset_back_cover_latex(self):
        r'''Typesets back cover LaTeX file.

        Returns none.
        '''
        self._typeset_file_ending_with('back-cover.tex')

    def typeset_front_cover_latex(self):
        r'''Typesets front cover LaTeX file.

        Retunrs none.
        '''
        self._typeset_file_ending_with('front-cover.tex')

    def typeset_preface_latex(self):
        r'''Typesets preface LaTeX file.

        Returns none.
        '''
        self._typeset_file_ending_with('preface.tex')

    def typeset_score_latex(self):
        r'''Typesets score LaTeX file.

        Returns none.
        '''
        self._typeset_file_ending_with('score.tex')

    def view_back_cover_pdf(self):
        r'''Views back cover PDF.
        
        Returns none.
        '''
        self._open_file_ending_with('back-cover.pdf')

    def view_front_cover_pdf(self):
        r'''Views front cover PDF.

        Returns none.
        '''
        self._open_file_ending_with('front-cover.pdf')

    def view_preface_pdf(self):
        r'''Views preface PDF.

        Returns none.
        '''
        self._open_file_ending_with('preface.pdf')

    def view_score_pdf(self):
        r'''Views score PDF.

        Returns none.
        '''
        self._open_file_ending_with('score.pdf')

    def view_segment_assembly_pdf(self):
        r''''Views segment assembly PDF.

        Returns none.
        '''
        self._open_file_ending_with('score-segments.pdf')
