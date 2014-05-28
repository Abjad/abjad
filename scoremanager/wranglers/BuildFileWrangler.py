# -*- encoding: utf-8 -*-
import os
import shutil
from abjad.tools import lilypondfiletools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools import systemtools
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
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(BuildFileWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = None
        self._user_storehouse_path = None
        self._score_storehouse_path_infix_parts = ('build',)
        self._basic_breadcrumb = 'build files'
        self._human_readable = False
        self._include_extensions = True
        self._asset_identifier = 'file'

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_method(self):
        superclass = super(BuildFileWrangler, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'bce': self.edit_back_cover_source,
            'bcg': self.generate_back_cover_source,
            'bci': self.interpret_back_cover,
            'bco': self.open_back_cover_pdf,
            'cp': self.copy_file,
            'dc': self.collect_segment_pdfs,
            'de': self.edit_draft_source,
            'dg': self.generate_draft_source,
            'di': self.interpret_draft,
            'do': self.open_draft_pdf,
            'fce': self.edit_front_cover_source,
            'fceio': self.edit_interpret_open_front_cover_source,
            'fcg': self.generate_front_cover_source,
            'fci': self.interpret_front_cover,
            'fco': self.open_front_cover_pdf,
            'mc': self.collect_segment_lilypond_files,
            'me': self.edit_music_source,
            'mg': self.generate_music_source,
            'mi': self.interpret_music,
            'mo': self.open_music_pdf,
            'new': self.make_file,
            'pe': self.edit_preface_source,
            'pg': self.generate_preface_source,
            'pi': self.interpret_preface,
            'po': self.open_preface_pdf,
            'se': self.edit_score_source,
            'sg': self.generate_score_source,
            'si': self.interpret_score,
            'so': self.open_score_pdf,
            'ren': self.rename_file,
            'rm': self.remove_files,
            })
        return result

    ### PRIVATE METHODS ###

    def _call_lilypond_on_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            self._io_manager.run_lilypond(file_path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)

    def _collect_segment_files(self, file_name):
        segments_directory = self._session.current_segments_directory
        build_directory = self._get_current_directory()
        directory_entries = sorted(os.listdir(segments_directory))
        source_file_paths, target_file_paths = [], []
        _, extension = os.path.splitext(file_name)
        for directory_entry in directory_entries:
            segment_directory = os.path.join(
                segments_directory,
                directory_entry,
                )
            if not os.path.isdir(segment_directory):
                continue
            source_file_path = os.path.join(
                segment_directory,
                file_name,
                )
            if not os.path.isfile(source_file_path):
                continue
            score_path = self._session.current_score_directory
            score_package = self._configuration.path_to_package_path(
                score_path)
            score_name = score_package.replace('_', '-')
            directory_entry = directory_entry.replace('_', '-')
            if 'segment' in directory_entry:
                target_file_name = directory_entry + extension
            else:
                target_file_name = '{}-{}{}'.format(
                    score_name,
                    directory_entry,
                    extension
                    )
            target_file_path = os.path.join(
                build_directory,
                target_file_name,
                )
            source_file_paths.append(source_file_path)
            target_file_paths.append(target_file_path)
        if source_file_paths:
            messages = []
            messages.append('will copy ...')
            pairs = zip(source_file_paths, target_file_paths)
            for source_file_path, target_file_path in pairs:
                message = ' FROM: {}'.format(source_file_path)
                messages.append(message)
                message = '   TO: {}'.format(target_file_path)
                messages.append(message)
            self._io_manager._display(messages)
            if not self._io_manager._confirm():
                return
            if self._session.is_backtracking:
                return
        if not os.path.exists(build_directory):
            os.mkdir(build_directory)
        pairs = zip(source_file_paths, target_file_paths)
        return pairs

    def _edit_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            self._io_manager.edit(file_path)
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)

    def _enter_run(self):
        self._session._is_navigating_to_score_build_files = False

    def _generate_latex_source(self, file_name):
        manager = self._session.current_score_package_manager
        assert manager is not None
        width, height, unit = manager._parse_paper_dimensions()
        destination_path = os.path.join(
            manager._path,
            'build',
            file_name,
            )
        previously_existed = False
        if os.path.exists(destination_path):
            previously_existed = True
            messages = []
            message = 'overwrite {}?'
            message = message.format(destination_path)
            result = self._io_manager._confirm(message)
            if self._session.is_backtracking or not result:
                return
        source_path = os.path.join(
            self._configuration.score_manager_directory,
            'boilerplate',
            file_name,
            )
        shutil.copyfile(source_path, destination_path)
        old = '{PAPER_SIZE}'
        new = '{{{}{}, {}{}}}'
        new = new.format(width, unit, height, unit)
        self._replace_in_file(destination_path, old, new)
        if previously_existed:
            message = 'overwrote {}.'.format(destination_path)
            self._io_manager._display(message)

    def _make_back_cover_menu_section(self, menu):
        commands = []
        commands.append(('back cover - edit latex source', 'bce'))
        commands.append(('back cover - generate latex source', 'bcg'))
        commands.append(('back cover - interpret latex source', 'bci'))
        commands.append(('back cover - open pdf', 'bco'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='back cover',
            )

    def _make_draft_menu_section(self, menu):
        commands = []
        commands.append(('draft - collect segment files', 'dc'))
        commands.append(('draft - edit latex source', 'de'))
        commands.append(('draft - generate latex source', 'dg'))
        commands.append(('draft - interpret latex source', 'di'))
        commands.append(('draft - open pdf', 'do'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='draft',
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
        commands.append(('front cover - edit latex source', 'fce'))
        commands.append(('front cover - edit; interpret; open', 'fceio'))
        commands.append(('front cover - generate latex source', 'fcg'))
        commands.append(('front cover - interpret latex source', 'fci'))
        commands.append(('front cover - open pdf', 'fco'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='front cover',
            )

    def _make_main_menu(self):
        superclass = super(BuildFileWrangler, self)
        menu = superclass._make_main_menu()
        self._make_files_menu_section(menu)
        if self._session.is_in_score:
            self._make_back_cover_menu_section(menu)
            self._make_draft_menu_section(menu)
            self._make_front_cover_menu_section(menu)
            self._make_music_menu_section(menu)
            self._make_preface_menu_section(menu)
            self._make_score_menu_section(menu)
        return menu

    def _make_music_menu_section(self, menu):
        commands = []
        commands.append(('music - collect segment files', 'mc'))
        commands.append(('music - edit lilypond source', 'me'))
        commands.append(('music - generate lilypond source', 'mg'))
        commands.append(('music - interpret lilypond source', 'mi'))
        commands.append(('music - open pdf', 'mo'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='music',
            )

    def _make_preface_menu_section(self, menu):
        commands = []
        commands.append(('preface - edit latex source', 'pe'))
        commands.append(('preface - generate latex source', 'pg'))
        commands.append(('preface - interpret latex source', 'pi'))
        commands.append(('preface - open pdf', 'po'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='preface',
            )

    def _make_score_menu_section(self, menu):
        commands = []
        commands.append(('score - edit latex source', 'se'))
        commands.append(('score - generate latex source', 'sg'))
        commands.append(('score - interpret latex source', 'si'))
        commands.append(('score - open pdf', 'so'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='score',
            )

    def _trim_lilypond_file(self, file_path):
        lines = []
        with open(file_path, 'r') as file_pointer:
            found_score_block = False
            for line in file_pointer.readlines():
                if line.startswith(r'\score'):
                    found_score_block = True
                    continue
                if line.startswith('}'):
                    found_score_block = False
                    lines.append('\n')
                    continue
                if found_score_block:
                    lines.append(line)
        if lines and lines[-1] == '\n':
            lines.pop()
        lines = ''.join(lines)
        with open(file_path, 'w') as file_pointer:
            file_pointer.write(lines)

    def _interpret_file_ending_with(self, string):
        r'''Typesets TeX file.
        Calls ``pdflatex`` on file TWICE.
        Some LaTeX packages like ``tikz`` require two passes.
        '''
        file_path = self._get_file_path_ending_with(string)
        if not file_path:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager._display(message)
            return
        input_directory = os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        input_file_name_stem, extension = os.path.splitext(basename)
        output_directory = input_directory
        command = 'pdflatex --jobname={} -output-directory={} {}/{}.tex'
        command = command.format(
            input_file_name_stem,
            output_directory,
            input_directory,
            input_file_name_stem,
            )
        command_called_twice = '{}; {}'.format(command, command)
        with systemtools.TemporaryDirectoryChange(input_directory):
            self._io_manager.spawn_subprocess(command_called_twice)
            command = 'rm {}/*.aux'.format(output_directory)
            self._io_manager.spawn_subprocess(command)
            command = 'rm {}/*.log'.format(output_directory)
            self._io_manager.spawn_subprocess(command)

    ### PUBLIC METHODS ###

    def collect_segment_lilypond_files(self):
        r'''Copies LilyPond files from segment packages to build directory.

        Trims top-level comments, includes and directives from each LilyPond
        file.

        Trims header and paper block from each LilyPond file.

        Leaves score block in each LilyPond file.

        Returns none.
        '''
        pairs = self._collect_segment_files('output.ly')
        if not pairs:
            return
        for source_file_path, target_file_path in pairs:
            shutil.copyfile(source_file_path, target_file_path)
            self._trim_lilypond_file(target_file_path)

    def collect_segment_pdfs(self):
        r'''Copies segment PDFs from segment packages to build directory.

        Returns none.
        '''
        pairs = self._collect_segment_files('output.pdf')
        if not pairs:
            return
        for source_file_path, target_file_path in pairs:
            shutil.copyfile(source_file_path, target_file_path)

    def copy_file(self):
        r'''Copies build file.

        Returns none.
        '''
        self._copy_asset(force_lowercase=False)

    def edit_back_cover_source(self):
        r'''Edits back cover LaTeX source.

        Returns none.
        '''
        self._edit_file_ending_with('back-cover.tex')

    def edit_draft_source(self):
        r'''Edits draft LaTeX source.

        Returns none.
        '''
        self._edit_file_ending_with('draft.tex')

    def edit_front_cover_source(self):
        r'''Edits front cover LaTeX source.

        Returns none.
        '''
        self._edit_file_ending_with('front-cover.tex')

    def edit_interpret_open_front_cover_source(self):
        r'''Edits front cover LaTeX source;
        interprets front cover LaTeX source;
        opens front cover PDF.

        Returns none.
        '''
        self.edit_front_cover_source()
        self.interpret_front_cover()
        self.open_front_cover_pdf()

    def edit_music_source(self):
        r'''Edits music LilyPond source.

        Returns none.
        '''
        self._edit_file_ending_with('music.ly')

    def edit_preface_source(self):
        r'''Edits preface LaTeX source.

        Returns none.
        '''
        self._edit_file_ending_with('preface.tex')

    def edit_score_source(self):
        r'''Edits score LaTeX source.

        Returns none.
        '''
        self._edit_file_ending_with('score.tex')

    def generate_back_cover_source(self):
        r'''Generates back cover LaTeX source.

        Returns none.
        '''
        self._generate_latex_source('back-cover.tex')

    # TODO: factor our code shared with self.generate_music_source()
    def generate_draft_source(self):
        r'''Generates draft LaTeX source.

        Returns none.
        '''
        manager = self._session.current_score_package_manager
        width, height, unit = manager._parse_paper_dimensions()
        build_directory = self._get_current_directory()
        assert width and height and unit
        assert build_directory
        destination_path = os.path.join(
            manager._path,
            'build',
            'draft.tex',
            )
        previously_existed = False
        if os.path.exists(destination_path):
            previously_existed = True
            messages = []
            message = 'overwrite {}?'
            message = message.format(destination_path)
            result = self._io_manager._confirm(message)
            if self._session.is_backtracking or not result:
                return
        wrangler = self._session._score_manager._segment_package_wrangler
        view_name = wrangler._read_view_name()
        view_inventory = wrangler._read_view_inventory()
        if not view_inventory or view_name not in view_inventory:
            view_name = None
        segment_paths = wrangler._list_visible_asset_paths()
        segment_paths = segment_paths or []
        segment_names = []
        for segment_path in segment_paths:
            segment_name = os.path.basename(segment_path)
            segment_names.append(segment_name)
        pdf_names = []
        for segment_name in segment_names:
            pdf_name = segment_name.replace('_', '-')
            pdf_names.append(pdf_name)
        messages = []
        if view_name:
            message = 'the {!r} segment view is currently selected.'
            message = message.format(view_name)
            messages.append(message)
        if pdf_names:
            message = 'will assemble segments in this order:'
            messages.append(message)
            for segment_name in segment_names:
                message = '    ' + segment_name
                messages.append(message)
        else:
            message = 'no segments found:'
            message += ' will generate source without segments.'
            messages.append(message)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        source_path = os.path.join(
            self._configuration.score_manager_directory,
            'boilerplate',
            'draft.tex',
            )
        shutil.copyfile(source_path, destination_path)
        old = '{PAPER_SIZE}'
        new = '{{{}{}, {}{}}}'
        new = new.format(width, unit, height, unit)
        self._replace_in_file(destination_path, old, new)
        lines = []
        for pdf_name in pdf_names:
            line = r'\includepdf[pages=-]{{{}.pdf}}'
            line = line.format(pdf_name)
            lines.append(line)
        if lines:
            new = '\n'.join(lines)
            old = '%%% SEGMENTS %%%'
            self._replace_in_file(destination_path, old, new)
        else:
            line_to_remove = '%%% SEGMENTS %%%\n'
            self._remove_file_line(destination_path, line_to_remove)
        if previously_existed:
            message = 'Overwrote {}.'.format(destination_path)
            self._io_manager._display(message)

    def generate_front_cover_source(self):
        r'''Generates front cover LaTeX source.

        Returns none.
        '''
        self._generate_latex_source('front-cover.tex')
        
    # TODO: factor our code shared with self.generate_draft_source()
    def generate_music_source(self):
        r'''Generates music LilyPond source.

        Returns none.
        '''
        manager = self._session.current_score_package_manager
        #width, height, unit = manager._parse_paper_dimensions()
        build_directory = self._get_current_directory()
        #assert width and height and unit
        assert build_directory
        destination_path = os.path.join(
            manager._path,
            'build',
            'music.ly',
            )
        previously_existed = False
        if os.path.exists(destination_path):
            previously_existed = True
            messages = []
            message = 'overwrite {}?'
            message = message.format(destination_path)
            result = self._io_manager._confirm(message)
            if self._session.is_backtracking or not result:
                return
        wrangler = self._session._score_manager._segment_package_wrangler
        view_name = wrangler._read_view_name()
        view_inventory = wrangler._read_view_inventory()
        if not view_inventory or view_name not in view_inventory:
            view_name = None
        segment_paths = wrangler._list_visible_asset_paths()
        segment_paths = segment_paths or []
        segment_names = []
        for segment_path in segment_paths:
            segment_name = os.path.basename(segment_path)
            segment_names.append(segment_name)
        lilypond_names = []
        for segment_name in segment_names:
            lilypond_name = segment_name.replace('_', '-')
            lilypond_names.append(lilypond_name)
        messages = []
        if view_name:
            message = 'the {!r} segment view is currently selected.'
            message = message.format(view_name)
            messages.append(message)
        if lilypond_names:
            message = 'will assemble segments in this order:'
            messages.append(message)
            for segment_name in segment_names:
                message = '    ' + segment_name
                messages.append(message)
        else:
            message = 'no segments found:'
            message += ' will generate source without segments.'
            messages.append(message)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        source_path = os.path.join(
            self._configuration.score_manager_directory,
            'boilerplate',
            'music.ly',
            )
        shutil.copyfile(source_path, destination_path)
        lines = []
        for lilypond_name in lilypond_names:
            file_name = lilypond_name + '.ly'
            #path = file_name
            line = r'   \include "{}"'
            #line = line.format(path)
            line = line.format(file_name)
            lines.append(line)
        if lines:
            new = '\n'.join(lines)
            old = '%%% SEGMENTS %%%'
            self._replace_in_file(destination_path, old, new)
        else:
            line_to_remove = '%%% SEGMENTS %%%\n'
            self._remove_file_line(destination_path, line_to_remove)
        stylesheet_path = self._session.current_stylesheet_path
        if stylesheet_path:
            old = '% STYLESHEET_INCLUDE_STATEMENT'
            #new = r'\include "{}"'.format(stylesheet_path)
            new = r'\include "../stylesheets/stylesheet.ily"'
            self._replace_in_file(destination_path, old, new)
        language_token = lilypondfiletools.LilyPondLanguageToken()
        lilypond_language_directive = format(language_token)
        old = '% LILYPOND_LANGUAGE_DIRECTIVE'
        new = lilypond_language_directive
        self._replace_in_file(destination_path, old, new)
        version_token = lilypondfiletools.LilyPondVersionToken()
        lilypond_version_directive = format(version_token)
        old = '% LILYPOND_VERSION_DIRECTIVE'
        new = lilypond_version_directive
        self._replace_in_file(destination_path, old, new)
        score_title = manager._get_title()
        if score_title:
            old = 'SCORE_NAME'
            new = score_title
            self._replace_in_file(destination_path, old, new)
        annotated_title = manager._get_title(year=True)
        if annotated_title:
            old = 'SCORE_TITLE'
            new = annotated_title
            self._replace_in_file(destination_path, old, new)
        forces_tagline = manager._get_metadatum('forces_tagline')
        if forces_tagline:
            old = 'FORCES_TAGLINE'
            new = forces_tagline
            self._replace_in_file(destination_path, old, new)
        if previously_existed:
            message = 'overwrote {}.'.format(destination_path)
            self._io_manager._display(message)

    def generate_preface_source(self):
        r'''Generates preface LaTeX source.

        Returns none.
        '''
        self._generate_latex_source('preface.tex')

    def generate_score_source(self):
        r'''Generates score LaTeX source.

        Returns none.
        '''
        self._generate_latex_source('score.tex')

    def interpret_back_cover(self):
        r'''Interprets back cover LaTeX source.

        Returns none.
        '''
        self._interpret_file_ending_with('back-cover.tex')

    def interpret_draft(self):
        r'''Interprets draft score LaTeX source.

        Returns none.
        '''
        self._interpret_file_ending_with('draft.tex')

    def interpret_front_cover(self):
        r'''Interprets front cover LaTeX source.

        Returns none.
        '''
        self._interpret_file_ending_with('front-cover.tex')

    def interpret_music(self):
        r'''Interprets music LilyPond source.

        Returns none.
        '''
        self._call_lilypond_on_file_ending_with('music.ly')
        
    def interpret_preface(self):
        r'''Interprets preface LaTeX source.

        Returns none.
        '''
        self._interpret_file_ending_with('preface.tex')

    def interpret_score(self):
        r'''Interprets score LaTeX source.

        Returns none.
        '''
        self._interpret_file_ending_with('score.tex')

    def make_file(self):
        r'''Makes empty file in build directory.

        Returns none.
        '''
        self._make_file(
            prompt_string='file name', 
            )

    def open_back_cover_pdf(self):
        r'''Opens back cover PDF.

        Returns none.
        '''
        self._open_file_ending_with('back-cover.pdf')

    def open_draft_pdf(self):
        r'''Opens draft score PDF.

        Return none.
        '''
        self._open_file_ending_with('draft.pdf')

    def open_front_cover_pdf(self):
        r'''Opens front cover PDF.

        Returns none.
        '''
        self._open_file_ending_with('front-cover.pdf')

    def open_music_pdf(self):
        r'''Opens music PDF.

        Returns none.
        '''
        self._open_file_ending_with('music.pdf')

    def open_preface_pdf(self):
        r'''Opens preface PDF.

        Returns none.
        '''
        self._open_file_ending_with('preface.pdf')

    def open_score_pdf(self):
        r'''Opens score PDF.

        Returns none.
        '''
        self._open_file_ending_with('score.pdf')

    def remove_files(self):
        r'''Removes one or more build files.

        Returns none.
        '''
        self._remove_assets()

    def rename_file(self):
        r'''Renames build file.

        Returns none.
        '''
        self._rename_asset()