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
        PackageManager.__init__(
            self,
            path=path,
            session=session,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        annotated_title = self._get_title(year=True)
        if self._session.is_in_score_setup_menu:
            return '{} - setup'.format(annotated_title)
        else:
            return annotated_title

    @property
    def _user_input_to_action(self):
        superclass = super(ScorePackageManager, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'd': self._session._score_manager._distribution_file_wrangler._run,
            'g': self._session._score_manager._segment_package_wrangler._run,
            'fix': self.fix,
            'k': self._session._score_manager._maker_module_wrangler._run,
            'm': self._session._score_manager._material_package_wrangler._run,
            'p': self._manage_setup,
            'pdf': self.view_score_pdf,
            'rad': self.add_to_repository,
            'rci': self.commit_to_repository,
            'rrv': self.revert_to_repository,
            'rst': self.repository_status,
            'rua': self.remove_unadded_assets,
            'rup': self.update_from_repository,
            'u': self._session._score_manager._build_file_wrangler._run,
            'y': self._session._score_manager._stylesheet_wrangler._run,
            'Y': self._io_manager.edit_score_stylesheet,
            })
        return result

    ### PRIVATE METHODS ###

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
                output_material = manager._execute_output_module()
                return output_material

    def _get_title(self, year=False):
        if year and self._get_metadatum('year_of_completion'):
            result = '{} ({})'
            result = result.format(
                self._get_title(),
                self._get_metadatum('year_of_completion')
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

    def _handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            message = 'unknown user input: {!r}.'
            message = message.format(result)
            raise ValueError(message)

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
            self.edit_year_of_completion()
        elif result == 'user entered lone return':
            pass
        else:
            raise ValueError(result)

    def _is_visible(self):
        scores_to_display = self._session.scores_to_display
        metadata = self._get_metadata()
        if scores_to_display == 'all':
            return metadata
        is_mothballed = metadata.get('is_mothballed')
        is_example = metadata.get('is_example')
        if scores_to_display == 'active':
            if not is_mothballed:
                if not is_example:
                    return metadata
        elif scores_to_display == 'user':
            if not is_example:
                return metadata
        elif scores_to_display == 'example':
            if is_example:
                if not is_mothballed:
                    return metadata
        elif scores_to_display == 'mothballed':
            if is_mothballed:
                return metadata
        return False

    def _make_main_menu(self, name='score package manager'):
        menu = self._io_manager.make_menu(name=name)
        self._make_main_menu_section(menu)
        self._make_metadata_menu_section(menu)
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
        commands.append(('score package - fix', 'fix'))
        commands.append(('score package - score pdf', 'pdf'))
        commands.append(('score package - remove unadded assets', 'rua'))
        commands.append(('score package - setup', 'p'))
        commands.append(('score package - view initializer', 'inro'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='score',
            )

    def _make_setup_menu(self):
        menu = self._io_manager.make_menu(name='setup')
        self._make_setup_menu_section(menu)
        return menu

    def _make_setup_menu_entry(self, display_string, prepopulated_value):
        from scoremanager import iotools
        return iotools.MenuEntry(
            display_string=display_string,
            prepopulated_value=prepopulated_value,
            explicit_return_value=display_string,
            )

    def _make_setup_menu_entries(self):
        entries = []
        title = self._get_metadatum('title')
        entry = self._make_setup_menu_entry('title', title)
        entries.append(entry)
        forces_tagline = self._get_metadatum('forces_tagline')
        entry = self._make_setup_menu_entry('tagline', forces_tagline)
        entries.append(entry)
        year_of_completion = self._get_metadatum('year_of_completion')
        entry = self._make_setup_menu_entry('year', year_of_completion)
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
            if self._should_backtrack():
                break
            elif not result:
                continue
            self._handle_setup_menu_result(result)
            if self._should_backtrack():
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
        self._io_manager.write_cache(prompt=False)

    ### PUBLIC METHODS ###

    def edit_catalog_number(self):
        r'''Edits catalog number of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_string('catalog number')
        result = getter._run()
        if self._should_backtrack():
            return
        self._add_metadatum('catalog_number', result)

    def edit_forces_tagline(self):
        r'''Edits forces tagline of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_string('forces tagline')
        result = getter._run()
        if self._should_backtrack():
            return
        self._add_metadatum('forces_tagline', result)

    def edit_paper_dimensions(self):
        r'''Edits paper dimensions of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_string('paper dimensions')
        result = getter._run()
        if self._should_backtrack():
            return
        self._add_metadatum('paper_dimensions', result)

    def edit_title(self):
        r'''Edits title of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_string('new title')
        result = getter._run()
        if self._should_backtrack():
            return
        self._add_metadatum('title', result)
        self._io_manager.write_cache(prompt=False)

    def edit_year_of_completion(self):
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
        if self._should_backtrack():
            return
        self._add_metadatum('year_of_completion', result)

    def fix(self, prompt=True):
        r'''Fixes score package structure.

        Returns none.
        '''
        package_needed_to_be_fixed = False
        for path in self._get_top_level_directory_paths():
            if not os.path.exists(path):
                package_needed_to_be_fixed = True
                message = 'create {!r}?'.format(path)
                if not prompt or self._io_manager.confirm(message):
                    os.makedirs(path)
                    gitignore_path = os.path.join(path, '.gitignore')
                    with file(gitignore_path, 'w') as file_pointer:
                        file_pointer.write('')
        if not os.path.exists(self._initializer_file_path):
            package_needed_to_be_fixed = True
            message = 'create {}?'.format(self._initializer_file_path)
            if not prompt or self._io_manager.confirm(message):
                with file(self._initializer_file_path, 'w') as initializer:
                    initializer.write('')
        lines = []
        if not os.path.exists(self._metadata_module_path):
            package_needed_to_be_fixed = True
            message = 'create {}?'.format(self._metadata_module_path)
            if not prompt or self._io_manager.confirm(message):
                lines = []
                lines.append(self._unicode_directive)
                lines.append(self._abjad_import_statement)
                lines.append('import collections')
                lines.append('')
                lines.append('')
                line = 'metadata = collections.OrderedDict([])'
                lines.append(line)
                contents = '\n'.join(lines)
                with file(self._metadata_module_path, 'w') as file_pointer:
                    file_pointer.write(contents)
        return package_needed_to_be_fixed

    def view_score_pdf(self):
        r'''Views score PDF.

        Returns none.
        '''
        wrangler = self._session._score_manager._build_file_wrangler
        wrangler._open_file_ending_with('score.pdf')