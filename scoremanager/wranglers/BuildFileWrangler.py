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
        self._asset_identifier = 'file'
        self._manager_class = managers.FileManager

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        breadcrumb = 'build files'
        view_name = self._read_view_name()
        if not view_name:
            return breadcrumb
        view_inventory = self._read_view_inventory()
        if view_name in view_inventory:
            breadcrumb = '{} ({})'.format(breadcrumb, view_name)
        return breadcrumb

    @property
    def _user_input_to_action(self):
        superclass = super(BuildFileWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'bce': self.edit_back_cover_source,
            'bcg': self.generate_back_cover_source,
            'bci': self.interpret_back_cover,
            'bco': self.view_back_cover_pdf,
            'cp': self.copy_file,
            'de': self.edit_draft_source,
            'dg': self.generate_draft_source,
            'di': self.interpret_draft,
            'do': self.view_draft_pdf,
            'fce': self.edit_front_cover_source,
            'fcg': self.generate_front_cover_source,
            'fci': self.interpret_front_cover,
            'fco': self.view_front_cover_pdf,
            'me': self.edit_music_source,
            'mg': self.generate_music_source,
            'mi': self.interpret_music_lilypond_file,
            'mo': self.view_music_pdf,
            'new': self.make_file,
            'pfe': self.edit_preface_source,
            'pfg': self.generate_preface_source,
            'pfi': self.interpret_preface,
            'pfo': self.view_preface_pdf,
            'se': self.edit_score_source,
            'sg': self.generate_score_source,
            'st': self.interpret_score,
            'so': self.view_score_pdf,
            'lycp': self.copy_segment_lilypond_files,
            'pdfcp': self.copy_segment_pdfs,
            'ren': self.rename_file,
            'rm': self.remove_files,
            })
        return result

    ### PRIVATE METHODS ###

    # TODO: migrate to IOManager
    def _call_lilypond_on_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            file_manager = self._initialize_manager(file_path)
            file_manager.call_lilypond()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)

    # TODO: migrate to IOManager
    def _edit_file_ending_with(self, string):
        file_path = self._get_file_path_ending_with(string)
        if file_path:
            file_manager = self._initialize_manager(file_path)
            file_manager.edit()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)

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
        commands.append(('back cover - edit latex source', 'bce'))
        commands.append(('back cover - generate latex source', 'bcg'))
        commands.append(('back cover - interpret latex source', 'bci'))
        commands.append(('back cover - open pdf', 'bco'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
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
        commands.append(('front cover - edit latex source', 'fce'))
        commands.append(('front cover - generate latex source', 'fcg'))
        commands.append(('front cover - interpret latex source', 'fci'))
        commands.append(('front cover - open pdf', 'fco'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='front cover',
            )

    def _make_main_menu(self, name='build wrangler'):
        superclass = super(BuildFileWrangler, self)
        menu = superclass._make_main_menu(name=name)
        self._make_files_menu_section(menu)
        if self._session.is_in_score:
            self._make_back_cover_menu_section(menu)
            self._make_directory_menu_section(menu, is_permanent=True)
            self._make_draft_menu_section(menu)
            self._make_front_cover_menu_section(menu)
            self._make_music_menu_section(menu)
            self._make_preface_menu_section(menu)
            self._make_score_menu_section(menu)
            self._make_segments_menu_section(menu)
        return menu

    def _make_music_menu_section(self, menu):
        commands = []
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
        commands.append(('preface - edit latex source', 'pfe'))
        commands.append(('preface - generate latex source', 'pfg'))
        commands.append(('preface - interpret latex source', 'pfi'))
        commands.append(('preface - open pdf', 'pfo'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='preface',
            )

    def _make_segments_menu_section(self, menu):
        commands = []
        commands.append(('segment lys - copy', 'lycp'))
        commands.append(('segment pdfs - copy', 'pdfcp'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='segments?',
            )

    def _make_draft_menu_section(self, menu):
        commands = []
        commands.append(('draft - edit latex source', 'de'))
        commands.append(('draft - generate latex source', 'dg'))
        commands.append(('draft - interpret latex source', 'di'))
        commands.append(('draft - open pdf', 'do'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='draft',
            )

    def _make_score_menu_section(self, menu):
        commands = []
        commands.append(('score - edit latex source', 'se'))
        commands.append(('score - generate latex source', 'sg'))
        commands.append(('score - interpret latex source', 'st'))
        commands.append(('score - open pdf', 'so'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
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
            file_manager = self._initialize_manager(file_path)
            file_manager.typeset_tex_file()
        else:
            message = 'file ending in {!r} not found.'
            message = message.format(string)
            self._io_manager.display([message, ''])
        self._session._hide_next_redraw = True

    ### PUBLIC METHODS ###

    def copy_file(self):
        r'''Copies build file.

        Returns none.
        '''
        self._copy_asset(force_lowercase=False)

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
            target_file_name = directory_entry + '.ly'
            target_file_path = os.path.join(
                build_directory_path,
                target_file_name,
                )
            if not os.path.exists(build_directory_path):
                os.mkdir(build_directory_path)
            shutil.copyfile(source_file_path, target_file_path)
            self._trim_lilypond_file(target_file_path)
            message = 'segment {} LilyPond file copied & trimmed.'
            message = message.format(directory_entry)
            self._io_manager.display(message)
        self._io_manager.display('')
        self._session._hide_next_redraw = True

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
            if 'segment' in directory_entry:
                target_file_name = directory_entry + '.pdf'
            else:
                target_file_name = '{}-{}.pdf'.format(
                    score_name,
                    directory_entry,
                    )
            target_file_name = target_file_name.replace('_', '-')
            target_file_path = os.path.join(
                build_directory_path,
                target_file_name,
                )
            shutil.copyfile(source_file_path, target_file_path)
            message = 'segment {} PDF copied.'
            message = message.format(directory_entry)
            self._io_manager.display(message)
        self._io_manager.proceed('')

    def edit_back_cover_source(self):
        r'''Edits back cover LaTeX file.

        Returns none.
        '''
        self._edit_file_ending_with('back-cover.tex')

    def edit_draft_source(self):
        r'''Edits draft score LaTeX file.

        Returns none.
        '''
        self._edit_file_ending_with('draft.tex')

    def edit_front_cover_source(self):
        r'''Edits front cover LaTeX file.

        Returns none.
        '''
        self._edit_file_ending_with('front-cover.tex')

    def edit_music_source(self):
        r'''Edits music LilyPond file.

        Returns none.
        '''
        self._edit_file_ending_with('music.ly')

    def edit_preface_source(self):
        r'''Edits preface LaTeX file.

        Returns none.
        '''
        self._edit_file_ending_with('preface.tex')

    def edit_score_source(self):
        r'''Edits score LaTeX file.

        Returns none.
        '''
        self._edit_file_ending_with('score.tex')

    def generate_back_cover_source(self):
        r'''Generates back cover LaTeX file.

        Returns none.
        '''
        manager = self._session.current_score_package_manager
        assert manager is not None
        width, height, unit = manager._parse_paper_dimensions()
        destination_path = os.path.join(
            manager._path,
            'build',
            'back-cover.tex',
            )
        previously_existed = False
        if os.path.exists(destination_path):
            previously_existed = True
            messages = []
            message = 'overwrite {}?'
            message = message.format(destination_path)
            if not self._io_manager.confirm(message):
                return
        source_path = os.path.join(
            self._configuration.score_manager_directory_path,
            'latex',
            'back-cover.tex',
            )
        shutil.copyfile(source_path, destination_path)
        old = '{PAPER_DIMENSIONS}'
        new = '{{{}{}, {}{}}}'
        new = new.format(width, unit, height, unit)
        self._replace_in_file(destination_path, old, new)
        if previously_existed:
            message = 'Overwrote {}.'.format(destination_path)
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True

    def generate_draft_source(self):
        r'''Generates draft LaTeX file.

        Returns none.
        '''
        manager = self._session.current_score_package_manager
        width, height, unit = manager._parse_paper_dimensions()
        build_directory = self._get_current_directory_path()
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
            if not self._io_manager.confirm(message):
                return
        wrangler = self._session._score_manager._segment_package_wrangler
        #print repr(wrangler), 'WR'
        view_name = wrangler._read_view_name()
        #print repr(view_name), 'VN'
        segment_paths = wrangler._get_visible_asset_paths()
        segment_paths = segment_paths or []
        segment_names = []
        for segment_path in segment_paths:
            segment_name = os.path.basename(segment_path)
            segment_names.append(segment_name)
        messages = []
        messages.append('')
        if view_name:
            message = 'the {!r} segment view is currently selected.'
            message = message.format(view_name)
            messages.append(message)
            messages.append('')
        message = 'will assemble segments in this order:'
        messages.append(message)
        messages.append('')
        for segment_name in segment_names:
            message = '    ' + segment_name
            messages.append(message)
        messages.append('')
        self._io_manager.display(messages)
        self._io_manager.confirm()
        if self._should_backtrack():
            return
        source_path = os.path.join(
            self._configuration.score_manager_directory_path,
            'latex',
            'draft.tex',
            )
        shutil.copyfile(source_path, destination_path)
        old = '{PAPER_DIMENSIONS}'
        new = '{{{}{}, {}{}}}'
        new = new.format(width, unit, height, unit)
        self._replace_in_file(destination_path, old, new)
        old = '{BUILD_DIRECTORY}'
        new = '{{{}}}'.format(build_directory)
        self._replace_in_file(destination_path, old, new)
        if previously_existed:
            message = 'Overwrote {}.'.format(destination_path)
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True

    def generate_front_cover_source(self):
        r'''Generates front cover LaTeX file.

        Returns none.
        '''
        self._io_manager.print_not_yet_implemented()

    def generate_music_source(self):
        r'''Generates music LilyPond file.

        Returns none.
        '''
        self._io_manager.print_not_yet_implemented()

    def generate_preface_source(self):
        r'''Generates preface LaTeX file.

        Returns none.
        '''
        self._io_manager.print_not_yet_implemented()

    def generate_score_source(self):
        r'''Generates score LaTeX file.

        Returns none.
        '''
        self._io_manager.print_not_yet_implemented()

    def interpret_music_lilypond_file(self):
        r'''Interprets music LilyPond file.

        Returns none.
        '''
        self._call_lilypond_on_file_ending_with('music.ly')
        
    def make_file(self):
        r'''Makes build file.

        Returns none.
        '''
        self._io_manager.print_not_yet_implemented()

    def open_file(self, result):
        r'''Opens build file.

        Returns none.
        '''
        if result.endswith('.pdf'):
            self._io_manager.open_file(result)
        else:
            self._io_manager.edit(result)

    def remove_files(self):
        r'''Removes build file.

        Returns none.
        '''
        self._remove_assets()

    def rename_file(self):
        r'''Renames build file.

        Returns none.
        '''
        self._rename_asset()

    def interpret_back_cover(self):
        r'''Typesets back cover LaTeX file.

        Returns none.
        '''
        self._typeset_file_ending_with('back-cover.tex')

    def interpret_draft(self):
        r'''Typesets draft score LaTeX file.

        Returns none.
        '''
        self._typeset_file_ending_with('draft.tex')

    def interpret_front_cover(self):
        r'''Typesets front cover LaTeX file.

        Retunrs none.
        '''
        self._typeset_file_ending_with('front-cover.tex')

    def interpret_preface(self):
        r'''Typesets preface LaTeX file.

        Returns none.
        '''
        self._typeset_file_ending_with('preface.tex')

    def interpret_score(self):
        r'''Typesets score LaTeX file.

        Returns none.
        '''
        self._typeset_file_ending_with('score.tex')

    def view_back_cover_pdf(self):
        r'''Views back cover PDF.

        Returns none.
        '''
        self._open_file_ending_with('back-cover.pdf')

    def view_draft_pdf(self):
        r'''Views draft score PDF.

        Return none.
        '''
        self._open_file_ending_with('draft.pdf')

    def view_front_cover_pdf(self):
        r'''Views front cover PDF.

        Returns none.
        '''
        self._open_file_ending_with('front-cover.pdf')

    def view_music_pdf(self):
        r'''Views music PDF.

        Returns none.
        '''
        self._open_file_ending_with('music.pdf')

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