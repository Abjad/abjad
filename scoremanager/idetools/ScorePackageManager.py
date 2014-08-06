# -*- encoding: utf-8 -*-
import os
from abjad.tools import indicatortools
from abjad.tools import systemtools
from scoremanager.idetools.PackageManager import PackageManager


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
        self._annotate_year = True
        self._include_asset_name = False
        optional_directories = list(self._optional_directories)
        optional_directories.extend([
            'etc',
            ])
        self._optional_directories = tuple(optional_directories)
        required_directories = list(self._required_directories)
        required_directories.extend([
            'build',
            'distribution',
            'makers',
            'materials',
            'segments',
            'stylesheets',
            ])
        self._required_directories = tuple(required_directories)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        annotated_title = self._get_title(year=True)
        if self._session.is_in_score_setup_menu:
            return '{} - setup'.format(annotated_title)
        else:
            return annotated_title

    @property
    def _command_to_method(self):
        superclass = super(ScorePackageManager, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'p': self.go_to_setup,
            'so': self.open_score_pdf,
            })
        return result

    @property
    def _setup_command_to_method(self):
        result = {
            'catalog number': self.edit_catalog_number,
            'paper dimensions': self.edit_paper_dimensions,
            'price': self.edit_price,
            'tagline': self.edit_forces_tagline,
            'title': self.edit_title,
            'year': self.edit_year,
            }
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        superclass = super(ScorePackageManager, self)
        superclass._enter_run()
        self._session._last_score_path = self._path

    def _exit_run(self):
        superclass = super(ScorePackageManager, self)
        result = superclass._exit_run()
        if self._session.is_backtracking_to_score:
            self._session._is_backtracking_to_score = False
            result = False
        elif self._session.is_autonavigating_within_score:
            if self._session.is_backtracking_to_score_manager:
                result = True
            else:
                result = False
        return result

    def _get_build_directory(self):
        return os.path.join(
            self._path,
            'build',
            )

    def _get_distribution_directory(self):
        return os.path.join(
            self._path,
            'distribution',
            )

    def _get_makers_directory(self):
        return os.path.join(
            self._path,
            'makers',
            )

    def _get_materials_directory(self):
        return os.path.join(
            self._path,
            'materials',
            )

    def _get_segments_directory(self):
        return os.path.join(
            self._path,
            'segments',
            )

    def _get_stylesheets_directory(self):
        return os.path.join(
            self._path,
            'stylesheets',
            )

    def _get_tempo_inventory(self):
        wrangler = self._session._ide._material_package_wrangler
        paths = wrangler._list_asset_paths()
        for path in paths:
            manager = wrangler._initialize_manager(path)
            output_material_class_name = manager._get_metadatum(
                'output_material_class_name')
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

    def _get_top_level_directories(self):
        return (
            self._get_build_directory(),
            self._get_distribution_directory(),
            self._get_makers_directory(),
            self._get_materials_directory(),
            self._get_segments_directory(),
            self._get_stylesheets_directory(),
            )

    def _get_top_level_wranglers(self):
        return (
            self._session._ide._build_file_wrangler,
            self._session._ide._distribution_file_wrangler,
            self._session._ide._maker_file_wrangler,
            self._session._ide._material_package_wrangler,
            self._session._ide._segment_package_wrangler,
            self._session._ide._stylesheet_wrangler,
            )

    def _handle_setup_menu_result(self, result):
        assert isinstance(result, str)
        if result == '<return>':
            pass
        elif result in self._setup_command_to_method:
            self._setup_command_to_method[result]()
        else:
            raise ValueError(result)

    def _make_main_menu(self):
        superclass = super(ScorePackageManager, self)
        menu = superclass._make_main_menu()
        self._make_init_py_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_package_menu_section(menu)
        return menu

    def _make_package(self):
        assert not os.path.exists(self._path)
        os.mkdir(self._path)
        with self._io_manager._silent():
            self.check_package(
                return_supply_messages=True,
                supply_missing=True,
                )

    def _make_package_menu_section(self, menu):
        superclass = super(ScorePackageManager, self)
        commands = superclass._make_package_menu_section(
            menu, commands_only=True)
        commands.append(('package - score.pdf - open', 'so'))
        commands.append(('package - setup', 'p'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='package',
            )

    def _make_setup_menu(self):
        menu = self._io_manager._make_menu(name='setup')
        self._make_setup_menu_section(menu)
        return menu

    def _make_setup_menu_entries(self):
        entries = []
        catalog_number = self._get_metadatum('catalog_number')
        entry = self._make_setup_menu_entry('catalog number', catalog_number)
        entries.append(entry)
        paper_dimensions = self._get_metadatum('paper_dimensions')
        entry = self._make_setup_menu_entry(
            'paper dimensions', 
            paper_dimensions,
            )
        entries.append(entry)
        forces_tagline = self._get_metadatum('forces_tagline')
        entry = self._make_setup_menu_entry('tagline', forces_tagline)
        entries.append(entry)
        price = self._get_metadatum('price')
        entry = self._make_setup_menu_entry('price', price)
        entries.append(entry)
        title = self._get_metadatum('title')
        entry = self._make_setup_menu_entry('title', title)
        entries.append(entry)
        year = self._get_metadatum('year')
        entry = self._make_setup_menu_entry('year', year)
        entries.append(entry)
        return entries

    def _make_setup_menu_entry(self, display_string, prepopulated_value):
        from scoremanager import idetools
        return idetools.MenuEntry(
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
        wrangler = self._session._ide._score_package_wrangler
        with self._io_manager._silent():
            wrangler.write_cache()

    ### PUBLIC METHODS ###

    def edit_catalog_number(self):
        r'''Edits catalog number.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        getter.append_string('catalog number')
        result = getter._run()
        if self._session.is_backtracking or result is None:
            return
        self._add_metadatum('catalog_number', result)

    def edit_forces_tagline(self):
        r'''Edits forces tagline.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        getter.append_string('forces tagline')
        result = getter._run()
        if self._session.is_backtracking or result is None:
            return
        self._add_metadatum('forces_tagline', result)

    def edit_paper_dimensions(self):
        r'''Edits paper dimensions.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        getter.append_paper_dimensions('paper dimensions')
        result = getter._run()
        if self._session.is_backtracking or result is None:
            return
        self._add_metadatum('paper_dimensions', result)

    def edit_price(self):
        r'''Edits price.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        getter.append_string('price')
        result = getter._run()
        if self._session.is_backtracking or result is None:
            return
        self._add_metadatum('price', result)

    def edit_title(self):
        r'''Edits title.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        getter.append_string('new title')
        result = getter._run()
        if self._session.is_backtracking or result is None:
            return
        self._add_metadatum('title', result)
        wrangler = self._session._ide._score_package_wrangler
        with self._io_manager._silent():
            wrangler.write_cache()

    def edit_year(self):
        r'''Edits year.

        Returns none.
        '''
        getter = self._io_manager._make_getter()
        getter.append_integer_in_range(
            'year of completion',
            start=1,
            allow_none=True,
            )
        result = getter._run()
        if self._session.is_backtracking or result is None:
            return
        self._add_metadatum('year', result)
        wrangler = self._session._ide._score_package_wrangler
        with self._io_manager._silent():
            wrangler.write_cache()

    def go_to_setup(self):
        r'''Goes to setup.

        Returns none.
        '''
        self._session._is_in_score_setup_menu = True
        self._session._pending_redraw = True
        while True:
            menu = self._make_setup_menu()
            result = menu._run()
            self._session._pending_redraw = True
            if self._session.is_backtracking:
                break
            elif not result:
                continue
            self._handle_setup_menu_result(result)
            if self._session.is_backtracking or result is None:
                break
        self._session._is_in_score_setup_menu = False

    def open_score_pdf(self, dry_run=False):
        r'''Opens ``score.pdf``.

        Returns none.
        '''
        with self._io_manager._make_interaction(dry_run=dry_run):
            file_name = 'score.pdf'
            directory = self._get_distribution_directory()
            manager = self._io_manager._make_package_manager(directory)
            path = manager._get_file_path_ending_with(file_name)
            if not path:
                directory = self._get_build_directory()
                manager = self._io_manager._make_package_manager(directory)
                path = manager._get_file_path_ending_with(file_name)
            if dry_run:
                inputs, outputs = [], []
                if path:
                    inputs = [path]
                return inputs, outputs
            if path:
                self._io_manager.open_file(path)
            else:
                message = "no score.pdf file found"
                message += ' in either distribution/ or build/ directories.'
                self._io_manager._display(message)