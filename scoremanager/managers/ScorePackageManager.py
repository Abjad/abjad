# -*- encoding: utf-8 -*-
import functools
import os
from abjad.tools import indicatortools
from abjad.tools import systemtools
from scoremanager.managers.PackageManager import PackageManager


class ScorePackageManager(PackageManager):
    r'''Score package manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(ScorePackageManager, self)
        superclass.__init__(path=path, session=session)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        annotated_title = self._get_title(year=True)
        if self._session.is_in_score_setup_menu:
            return '{} - setup'.format(annotated_title)
        else:
            return annotated_title

    @property
    def _input_to_method(self):
        superclass = super(ScorePackageManager, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'fix': self.fix_package,
            'p': self._manage_setup,
            'pdfo': self.open_score_pdf,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        superclass = super(ScorePackageManager, self)
        superclass._enter_run()
        self._session._last_score_package_path = self._path

    def _exit_run(self):
        superclass = super(ScorePackageManager, self)
        result = superclass._exit_run()
        if self._session.is_backtracking_to_score:
            self._session._is_backtracking_to_score = False
            result = False
        elif self._session.is_autonavigating_within_score:
            result = False
        return result

    def _get_build_directory_path(self):
        return os.path.join(
            self._path,
            'build',
            )

    def _get_distribution_directory_path(self):
        return os.path.join(
            self._path,
            'distribution',
            )

    def _get_makers_directory_path(self):
        return os.path.join(
            self._path,
            'makers',
            )

    def _get_materials_directory_path(self):
        return os.path.join(
            self._path,
            'materials',
            )

    def _get_segments_directory_path(self):
        return os.path.join(
            self._path,
            'segments',
            )

    def _get_stylesheets_directory_path(self):
        return os.path.join(
            self._path,
            'stylesheets',
            )

    def _get_tempo_inventory(self):
        wrangler = self._session._score_manager._material_package_wrangler
        paths = wrangler._list_asset_paths()
        for path in paths:
            manager = wrangler._initialize_manager(path)
            output_material_class_name = manager._get_metadatum('output_material_class_name')
            if output_material_class_name == 'TempoInventory':
                output_material = manager._execute_output_py()
                return output_material

    def _get_title(self, year=False):
        if year and self._get_metadatum('year'):
            result = '{} ({})'
            result = result.format(
                self._get_title(),
                self._get_metadatum('year')
                )
            return result
        else:
            return self._get_metadatum('title') or '(untitled score)'

    def _get_top_level_directory_paths(self):
        return (
            self._get_build_directory_path(),
            self._get_distribution_directory_path(),
            self._get_makers_directory_path(),
            self._get_materials_directory_path(),
            self._get_segments_directory_path(),
            self._get_stylesheets_directory_path(),
            )

    # TODO: reimplement options as dictionary
    def _handle_setup_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'catalog number':
            self.edit_catalog_number()
        elif result == 'paper dimensions':
            self.edit_paper_dimensions()
        elif result == 'tagline':
            self.edit_forces_tagline()
        elif result == 'title':
            self.edit_title()
        elif result == 'year':
            self.edit_year()
        elif result == 'user entered lone return':
            pass
        else:
            raise ValueError(result)

    def _make_main_menu(self):
        superclass = super(ScorePackageManager, self)
        menu = superclass._make_main_menu()
        self._make_init_py_menu_section(menu)
        self._make_main_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_metadata_py_menu_section(menu)
        self._make_score_menu_section(menu)
        return menu

    def _make_main_menu_section(self, menu):
        commands = []
        commands.append(('build', 'u'))
        commands.append(('distribution', 'd'))
        commands.append(('makers', 'k'))
        commands.append(('materials', 'm'))
        commands.append(('segments', 'g'))
        commands.append(('stylesheets', 'y'))
        menu.make_navigation_section(
            commands=commands,
            name='main',
            )

    def _make_score_menu_section(self, menu):
        commands = []
        commands.append(('package - fix', 'fix'))
        commands.append(('package - score pdf - open', 'pdfo'))
        commands.append(('package - setup', 'p'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='score package',
            )

    def _make_setup_menu(self):
        menu = self._io_manager.make_menu(name='setup')
        self._make_setup_menu_section(menu)
        return menu

    def _make_setup_menu_entries(self):
        entries = []
        title = self._get_metadatum('title')
        entry = self._make_setup_menu_entry('title', title)
        entries.append(entry)
        forces_tagline = self._get_metadatum('forces_tagline')
        entry = self._make_setup_menu_entry('tagline', forces_tagline)
        entries.append(entry)
        year = self._get_metadatum('year')
        entry = self._make_setup_menu_entry('year', year)
        entries.append(entry)
        catalog_number = self._get_metadatum('catalog_number')
        entry = self._make_setup_menu_entry('catalog number', catalog_number)
        entries.append(entry)
        paper_dimensions = self._get_metadatum('paper_dimensions')
        entry = self._make_setup_menu_entry(
            'paper dimensions', 
            paper_dimensions,
            )
        entries.append(entry)
        return entries

    def _make_setup_menu_entry(self, display_string, prepopulated_value):
        from scoremanager import iotools
        return iotools.MenuEntry(
            display_string=display_string,
            prepopulated_value=prepopulated_value,
            explicit_return_value=display_string,
            )

    def _make_setup_menu_section(self, menu):
        menu_entries = self._make_setup_menu_entries()
        menu.make_attribute_section(
            menu_entries=menu_entries,
            name='setup',
            )

    def _manage_setup(self):
        self._session._is_in_score_setup_menu = True
        while True:
            annotated_title = self._get_title(year=True)
            menu = self._make_setup_menu()
            result = menu._run()
            if self._session.is_backtracking:
                break
            elif not result:
                continue
            self._handle_setup_menu_result(result)
            if self._session.is_backtracking:
                break
        self._session._is_in_score_setup_menu = False

    def _parse_paper_dimensions(self):
        string = self._get_metadatum('paper_dimensions') or '8.5 x 11 in'
        parts = string.split()
        assert len(parts) == 4
        width, _, height, units = parts
        width = eval(width)
        height = eval(height)
        return width, height, units

    def _remove(self):
        superclass = super(ScorePackageManager, self)
        superclass._remove()
        wrangler = self._session._score_manager._score_package_wrangler
        wrangler.write_cache(confirm=False, display=False)

    ### PUBLIC METHODS ###

    def edit_catalog_number(self):
        r'''Edits catalog number of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_string('catalog number')
        result = getter._run()
        if self._session.is_backtracking:
            return
        self._add_metadatum('catalog_number', result)

    def edit_forces_tagline(self):
        r'''Edits forces tagline of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_string('forces tagline')
        result = getter._run()
        if self._session.is_backtracking:
            return
        self._add_metadatum('forces_tagline', result)

    def edit_paper_dimensions(self):
        r'''Edits paper dimensions of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_string('paper dimensions')
        result = getter._run()
        if self._session.is_backtracking:
            return
        self._add_metadatum('paper_dimensions', result)

    def edit_title(self):
        r'''Edits title of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_string('new title')
        result = getter._run()
        if self._session.is_backtracking:
            return
        self._add_metadatum('title', result)
        wrangler = self._session._score_manager._score_package_wrangler
        wrangler.write_cache(confirm=False, display=False)

    def edit_year(self):
        r'''Edits year of completion of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_integer_in_range(
            'year of completion',
            start=1,
            allow_none=True,
            )
        result = getter._run()
        if self._session.is_backtracking:
            return
        self._add_metadatum('year', result)
        wrangler = self._session._score_manager._score_package_wrangler
        wrangler.write_cache(confirm=False, display=False)

    def fix_package(self, confirm=True, display=True):
        r'''Fixes score package.

        Returns none.
        '''
        package_needed_to_be_fixed = False
        for path in self._get_top_level_directory_paths():
            if not os.path.exists(path):
                package_needed_to_be_fixed = True
                if display:
                    messages = []
                    message = 'can not find {}.'.format(path)
                    messages.append(message)
                    message = 'create {}?'.format(path)
                    messages.append(message)
                    self._io_manager.display(messages)
                if confirm:
                    result = self._io_manager.confirm()
                    if self._session.is_backtracking:
                        return
                    if not result:
                        return
                    self._io_manager.display('')
                os.makedirs(path)
                gitignore_path = os.path.join(path, '.gitignore')
                with file(gitignore_path, 'w') as file_pointer:
                    file_pointer.write('')
        if not os.path.exists(self._init_py_file_path):
            package_needed_to_be_fixed = True
            if display:
                messages = []
                path = self._init_py_file_path
                message = 'can not find {}.'.format(path)
                messages.append(message)
                message = 'create {}?'.format(path)
                messages.append(message)
                self._io_manager.display(messages)
            if confirm:
                self._io_manager.display('')
                if self._session.is_backtracking:
                    return
                if not result:
                    return
                result = self._io_manager.confirm()
            self.write_stub_init_py(confirm=confirm, display=display)
        if not os.path.exists(self._metadata_py_path):
            package_needed_to_be_fixed = True
            if display:
                messages = []
                path = self._metadata_py_path
                message = 'can not find {}.'.format(path)
                messages.append(message)
                message = 'create {}?'.format(path)
                messages.append(message)
                self._io_manager.display(messages)
            if confirm:
                result = self._io_manager.confirm()
                if self._session.is_backtracking:
                    return
                if not result:
                    return
                self._io_manager.display('')
            self.rewrite_metadata_py(confirm=confirm, display=display)
        self._session._hide_next_redraw = False
        if display:
            if package_needed_to_be_fixed:
                message = 'Fixed package.'.format(self._path)
            else:
                message = 'No fixes required.'
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True
        return package_needed_to_be_fixed

    def open_score_pdf(self):
        r'''Opens score PDF.

        Returns none.
        '''
        wrangler = self._session._score_manager._build_file_wrangler
        wrangler._open_file_ending_with('score.pdf')