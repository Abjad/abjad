# -*- encoding: utf-8 -*-
import os
import shutil
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class BuildFileWrangler(Wrangler):
    r'''Build wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.BuildFileWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            BuildFileWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_include_extensions',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(BuildFileWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = None
        self._user_storehouse_path = None
        self._score_storehouse_path_infix_parts = ('build',)
        self._include_extensions = True
        self._manager_class = managers.FileManager

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            breadcrumb = 'build directory'
        else:
            breadcrumb = 'build file library'
        view_name = self._read_view_name()
        if view_name:
            breadcrumb = '{} ({} view)'.format(breadcrumb, view_name)
        return breadcrumb

    @property
    def _user_input_to_action(self):
        superclass = super(BuildFileWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'bce': self.edit_back_cover_latex,
            'bcg': self.generate_back_cover_latex,
            'bct': self.typeset_back_cover_latex,
            'bco': self.view_back_cover_pdf,
            'cp': self.copy_file,
            'fce': self.edit_front_cover_latex,
            'fcg': self.generate_front_cover_latex,
            'fct': self.typeset_front_cover_latex,
            'fco': self.view_front_cover_pdf,
            'pfe': self.edit_preface_latex,
            'pfg': self.generate_preface_latex,
            'pft': self.typeset_preface_latex,
            'pfo': self.view_preface_pdf,
            'se': self.edit_score_latex,
            'sg': self.generate_score_latex,
            'st': self.typeset_score_latex,
            'so': self.view_score_pdf,
            'lycp': self.copy_segment_lilypond_files,
            'pdfcp': self.copy_segment_pdfs,
            'sege': self.edit_segment_assembly_lilypond_file,
            'segly': self.interpret_segment_assembly_lilypond_file,
            'sego': self.view_segment_assembly_pdf,
            })
        return result

    ### PRIVATE METHODS ###

    # TODO: migrate to IOManager
    def _call_lilypond_on_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            file_manager = self._get_file_manager(file_path)
            file_manager.call_lilypond()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager.proceed(message)

    # TODO: migrate to IOManager
    def _edit_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            file_manager = self._get_file_manager(file_path)
            file_manager.edit()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager.proceed(message)

    def _enter_run(self):
        self._session._is_navigating_to_score_build_files = False

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self.open_file(result)

    def _make_asset_menu_entries(
        self,
        apply_view=True,
        include_annotation=True,
        include_extensions=True,
        include_asset_name=True,
        include_year=False,
        human_readable=False,
        packages_instead_of_paths=False,
        sort_by_annotation=True,
        ):
        superclass = super(BuildFileWrangler, self)
        menu_entries = superclass._make_asset_menu_entries(
            apply_view=apply_view,
            include_annotation=include_annotation,
            include_extensions=include_extensions,
            include_asset_name=include_asset_name,
            include_year=include_year,
            human_readable=human_readable,
            packages_instead_of_paths=packages_instead_of_paths,
            sort_by_annotation=sort_by_annotation,
            )
        return menu_entries

    def _make_asset_menu_section(self, menu):
        include_annotation = not self._session.is_in_score
        menu_entries = self._make_asset_menu_entries(
            human_readable=False,
            include_annotation=include_annotation,
            include_extensions=True,
            )
        if not menu_entries:
            return
        section = menu.make_asset_section(
            menu_entries=menu_entries,
            )
        menu._asset_section = section

    def _make_back_cover_menu_section(self, menu):
        commands = []
        commands.append(('back cover latex - edit', 'bce'))
        commands.append(('back cover latex - generate', 'bcg'))
        commands.append(('back cover latex - typeset', 'bct'))
        commands.append(('back cover pdf - open', 'bco'))
        menu.make_command_section(
            commands=commands,
            name='back cover',
            )

    def _make_files_menu_section(self, menu):
        commands = []
        commands.append(('files - copy', 'cp'))
        commands.append(('files - new', 'new'))
        commands.append(('files - rename', 'ren'))
        commands.append(('files - remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            name='files',
            )

    def _make_front_cover_menu_section(self, menu):
        commands = []
        commands.append(('front cover latex - edit', 'fce'))
        commands.append(('front cover latex - generate', 'fcg'))
        commands.append(('front cover latex - typeset', 'fct'))
        commands.append(('front cover pdf - open', 'fco'))
        menu.make_command_section(
            commands=commands,
            name='front cover',
            )

    def _make_main_menu(self, name='build wrangler'):
        superclass = super(BuildFileWrangler, self)
        menu = superclass._make_main_menu(name=name)
        self._make_files_menu_section(menu)
        if self._session.is_in_score:
            self._make_back_cover_menu_section(menu)
            self._make_directory_menu_section(menu, is_permanent=True)
            self._make_front_cover_menu_section(menu)
            self._make_preface_menu_section(menu)
            self._make_score_menu_sections(menu)
        return menu

    def _make_preface_menu_section(self, menu):
        commands = []
        commands.append(('preface latex - edit', 'pfe'))
        commands.append(('preface latex - generate', 'pfg'))
        commands.append(('preface latex - typeset', 'pft'))
        commands.append(('preface pdf - open', 'pfo'))
        menu.make_command_section(
            commands=commands,
            name='preface',
            )

    # TODO: divide into three methods
    def _make_score_menu_sections(self, menu):
        commands = []
        commands.append(('segment lys - copy', 'lycp'))
        commands.append(('segment pdfs - copy', 'pdfcp'))
        menu.make_command_section(
            commands=commands,
            name='segments?',
            )
        commands = []
        commands.append(('segment assembly ly - edit', 'sege'))
        commands.append(('segment assembly ly - lilypond', 'segly'))
        commands.append(('segment assembly pdf - open', 'sego'))
        menu.make_command_section(
            commands=commands,
            name='segment assembly?',
            )
        commands = []
        commands.append(('score latex - edit', 'se'))
        commands.append(('score latex - generate', 'sg'))
        commands.append(('score latex - typeset', 'st'))
        commands.append(('score pdf - open', 'so'))
        menu.make_command_section(
            commands=commands,
            name='score',
            )

    def _open_file_ending_with(self, string):
        path = self._get_file_path_ending_with(string)
        if path:
            manager = self._io_manager.make_file_manager(path)
            manager.open()
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

    def copy_file(self):
        r'''Copies build file.

        Returns none.
        '''
        self._copy_asset(
            force_lowercase=False,
            item_identifier='file',
            )

    def copy_segment_lilypond_files(self):
        r'''Copies segment LilyPond files from segment
        package directories to build directory.

        Trims top-level comments, includes and directives from each LilyPond
        file.

        Trims header and paper block from each LilyPond file.

        Leaves score block in each LilyPond file.

        Returns none.
        '''
        segments_directory_path = self._session.current_segments_directory_path
        build_directory_path = self._get_current_directory_path()
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
                build_directory_path,
                target_file_name,
                )
            #if not os.path.exists(self._current_build_directory_path):
            #    os.mkdir(self._current_build_directory_path)
            if not os.path.exists(build_directory_path):
                os.mkdir(build_directory_path)
            shutil.copyfile(source_file_path, target_file_path)
            self._trim_lilypond_file(target_file_path)
            message = 'segment {} LilyPond file copied & trimmed.'
            message = message.format(directory_entry)
            self._io_manager.display(message)
        self._io_manager.proceed('')

    def copy_segment_pdfs(self):
        r'''Copies segment PDFs from segment
        package directories to build directory.

        Returns none.
        '''
        segments_directory_path = self._session.current_segments_directory_path
        build_directory_path = self._get_current_directory_path()
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
            manager = self._session.current_score_package_manager
            score_name = manager._package_name
            directory_entry = directory_entry.replace('_', '-')
            target_file_name = '{}-segment-{}.pdf'
            target_file_name = target_file_name.format(
                score_name,
                directory_entry,
                )
            target_file_path = os.path.join(
                build_directory_path,
                target_file_name,
                )
            shutil.copyfile(source_file_path, target_file_path)
            message = 'segment {} PDF copied.'
            message = message.format(directory_entry)
            self._io_manager.display(message)
        self._io_manager.proceed('')

    def edit_back_cover_latex(self):
        r'''Edits back cover LaTeX file.

        Returns none.
        '''
        self._edit_file_ending_with('back-cover.tex')

    def open_file(self, result):
        r'''Opens build file.

        Returns none.
        '''
        if result.endswith('.pdf'):
            self._io_manager.open_file(result)
        else:
            self._io_manager.edit(result)

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

    def remove_build_files(self):
        r'''Removes build file.

        Returns none.
        '''
        self._remove_assets(
            item_identifier='build file',
            )

    def rename_build_file(self):
        r'''Renames build file.

        Returns none.
        '''
        self._rename_asset(
            item_identifier='build file',
            )

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