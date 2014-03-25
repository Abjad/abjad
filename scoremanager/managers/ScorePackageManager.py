# -*- encoding: utf-8 -*-
import functools
import os
from abjad.tools import systemtools
from scoremanager.managers.PackageManager import PackageManager


class ScorePackageManager(PackageManager):
    r'''Score package manager.
    '''

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
        annotated_title = self._get_annotated_title()
        if self._session.is_in_score_setup_menu:
            return '{} - setup'.format(annotated_title)
        else:
            return annotated_title

    @property
    @systemtools.Memoize
    def _build_directory_manager(self):
        from scoremanager import managers
        if self._path is None:
            return
        path = os.path.join(self._path, 'build')
        manager = managers.BuildDirectoryManager(
            path=path,
            session=self._session,
            )
        return manager

    @property
    @systemtools.Memoize
    def _distribution_directory_manager(self):
        from scoremanager import managers
        if self._path is None:
            return
        path = os.path.join(self._path, 'distribution')
        manager = managers.DistributionDirectoryManager(
            path=path,
            session=self._session,
            )
        return manager

    @property
    @systemtools.Memoize
    def _instrumentation_module_manager(self):
        from scoremanager import managers
        if self._path is None:
            return
        path = os.path.join(self._path, 'instrumentation.py')
        manager = managers.FileManager(
            path,
            session=self._session,
            )
        return manager

    @property
    @systemtools.Memoize
    def _maker_module_wrangler(self):
        from scoremanager import wranglers
        if self._path is None:
            return
        wrangler = wranglers.MakerModuleWrangler(session=self._session)
        return wrangler

    @property
    @systemtools.Memoize
    def _material_manager_wrangler(self):
        from scoremanager import wranglers
        if self._path is None:
            return
        wrangler = wranglers.MaterialManagerWrangler(session=self._session)
        return wrangler

    @property
    @systemtools.Memoize
    def _material_package_wrangler(self):
        from scoremanager import wranglers
        if self._path is None:
            return
        wrangler = wranglers.MaterialPackageWrangler(session=self._session)
        return wrangler

    @property
    @systemtools.Memoize
    def _score_package_wrangler(self):
        from scoremanager import wranglers
        if self._path is None:
            return
        wrangler = wranglers.ScorePackageWrangler(session=self._session)
        return wrangler

    @property
    @systemtools.Memoize
    def _segment_package_wrangler(self):
        from scoremanager import wranglers
        if self._path is None:
            return
        wrangler = wranglers.SegmentPackageWrangler(session=self._session)
        return wrangler

    @property
    @systemtools.Memoize
    def _stylesheet_wrangler(self):
        from scoremanager import wranglers
        if self._path is None:
            return
        wrangler = wranglers.StylesheetWrangler(session=self._session)
        return wrangler

    @property
    def _user_input_to_action(self):
        superclass = super(ScorePackageManager, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'd': self._distribution_directory_manager._run,
            'g': self._segment_package_wrangler._run,
            'fix': self.fix,
            'imro': self._instrumentation_module_manager.view,
            'k': self._maker_module_wrangler._run,
            'm': self._material_package_wrangler._run,
            'p': self._manage_setup,
            'pdfo': self.view_score_pdf,
            'rad': self.add_to_repository,
            'rci': self.commit_to_repository,
            'ren': self.rename_score_package,
            'rm': self.remove_score_package,
            'rrv': self.revert_to_repository,
            'rst': self.repository_status,
            'rua': self.remove_unadded_assets,
            'rup': self.update_from_repository,
            'u': self._build_directory_manager._run,
            'y': self._stylesheet_wrangler._run,
            'Y': self._io_manager.edit_score_stylesheet,
            })
        return result

    ### PRIVATE METHODS ###

    def _get_annotated_title(self):
        if isinstance(self._get_metadatum('year_of_completion'), int):
            return self._get_title_with_year()
        else:
            return self._get_title()

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

    def _get_instrumentation(self):
        return self._import_instrumentation_from_instrumentation_module()

    def _get_instrumentation_module_path(self):
        file_path = os.path.join(
            self._path,
            'instrumentation.py',
            )
        return file_path

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
        wrangler = self._material_package_wrangler
        paths = wrangler._list_asset_paths()
        for path in paths:
            manager = wrangler._initialize_asset_manager(path)
            string = 'material_manager_class_name'
            class_name = manager._get_metadatum(string)
            if class_name == 'TempoInventoryMaterialManager':
                output_material = manager._execute_output_module()
                return output_material

    def _get_title(self):
        return self._get_metadatum('title') or '(untitled score)'

    def _get_title_with_year(self):
        if self._get_metadatum('year_of_completion'):
            result = '{} ({})'
            result = result.format(
                self._get_title(), 
                self._get_metadatum('year_of_completion')
                )
            return result
        else:
            return self._get_title()

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

    def _handle_setup_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'catalog number':
            self.edit_catalog_number()   
        elif result == 'instr':
            self.edit_instrumentation_specifier()
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

    def _import_instrumentation_from_instrumentation_module(self):
        from scoremanager import managers
        file_path = os.path.join(
            self._path,
            'instrumentation.py',
            )
        manager = managers.FileManager(
            file_path,
            session=self._session,
            )
        result = manager._execute(
            attribute_names=('instrumentation',),
            )
        assert len(result) == 1
        instrumentation = result[0]
        return instrumentation

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

    def _make_instrumentation_menu_section(self, menu):
        section = menu.make_navigation_section(name='instrumentation')
        section.append(('instrumentation', 'instr'))
        return section

    def _make_instrumentation_module_menu_section(self, menu):
        section = menu.make_command_section(
            name='instrumentation',
            is_hidden=True,
            )
        section.append(('instrumentation module - read only', 'imro'))
        return section

    def _make_main_menu(self, name='score package manager'):
        menu = self._io_manager.make_menu(
            where=self._where,
            name=name,
            )
        self._make_main_menu_section(menu)
        self._make_directory_menu_section(menu, is_permanent=True)
        self._make_initializer_menu_section(menu)
        self._make_instrumentation_module_menu_section(menu)
        self._make_score_pdf_menu_section(menu)
        self._make_metadata_module_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_score_menu_section(menu)
        return menu

    def _make_main_menu_section(self, menu):
        section = menu.make_navigation_section(name='main')
        section.append(('build', 'u'))
        section.append(('distribution', 'd'))
        section.append(('makers', 'k'))
        section.append(('materials', 'm'))
        section.append(('segments', 'g'))
        section.append(('setup', 'p'))
        section.append(('stylesheets', 'y'))
        return section

    def _make_score_menu_section(self, menu):
        section = menu.make_command_section(
            name='score',
            is_hidden=True,
            )
        section.append(('score package - fix', 'fix'))
        section.append(('score package - remove', 'rm'))
        section.append(('score package - remove unadded assets', 'rua'))
        section.append(('score package - rename', 'ren'))
        return section

    def _make_score_pdf_menu_section(self, menu):
        manager = self._build_directory_manager
        if manager._get_file_path_ending_with('score.pdf'):
            section = menu.make_command_section(
                name='score pdf',
                default_index=0,
                )
            section.append(('score pdf - open', 'pdfo'))

    def _make_setup_menu(self):
        menu = self._io_manager.make_menu(
            where=self._where,
            name='setup',
            )
        self._make_setup_menu_section(menu)
        self._make_instrumentation_menu_section(menu)
        return menu

    def _make_setup_menu_entries(self):
        result = []
        return_value = 'title'
        prepopulated_value = None
        prepopulated_value = self._get_title() or None
        result.append((return_value, None, prepopulated_value, return_value))
        forces_tagline = self._get_metadatum('forces_tagline')
        prepopulated_value = None
        return_value = 'tagline'
        if forces_tagline:
            prepopulated_value = forces_tagline
        result.append((return_value, None, prepopulated_value, return_value))
        return_value = 'year'
        prepopulated_value = None
        year_of_completion = self._get_metadatum('year_of_completion')
        if year_of_completion:
            prepopulated_value = str(year_of_completion)
        result.append((return_value, None, prepopulated_value, return_value))
        catalog_number = self._get_metadatum('catalog_number')
        prepopulated_value = None
        return_value = 'catalog number'
        if catalog_number:
            prepopulated_value = catalog_number
        result.append((return_value, None, prepopulated_value, return_value))
        return result

    def _make_setup_menu_section(self, menu):
        section = menu.make_attribute_section(name='setup')
        menu_entries = self._make_setup_menu_entries()
        for menu_entry in menu_entries:
            section.append(menu_entry)
        return section

    def _manage_setup(self, clear=True):
        self._session._is_navigating_to_score_setup = False
        self._session._is_in_score_setup_menu = True
        while True:
            annotated_title = self._get_annotated_title()
            menu = self._make_setup_menu()
            result = menu._run(clear=clear)
            if self._session._break_io_loop():
                break
            elif not result:
                continue
            self._handle_setup_menu_result(result)
            if self._session._break_io_loop():
                break
        self._session._is_in_score_setup_menu = False

    def _remove(self):
        superclass = super(ScorePackageManager, self)
        superclass._remove()
        self._io_manager.write_cache(prompt=False)

    def _write_instrumentation(self, instrumentation):
        assert instrumentation is not None
        lines = []
        lines.append(self._unicode_directive + '\n')
        lines.append(self._abjad_import_statement + '\n')
        lines.append('\n\n')
        line = 'instrumentation={}'
        line = line.format(format(instrumentation))
        lines.append(line)
        file_path = self._get_instrumentation_module_path()
        contents = ''.join(lines)
        with file(file_path, 'w') as file_pointer:
            file_pointer.write(contents)

    ### PUBLIC METHODS ###

    def edit_catalog_number(self):
        r'''Edits catalog number of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('catalog number')
        result = getter._run()
        if self._session._break_io_loop():
            return
        self._add_metadatum('catalog_number', result)

    def edit_forces_tagline(self):
        r'''Edits forces tagline of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('Forces tagline')
        result = getter._run()
        if self._session._break_io_loop():
            return
        self._add_metadatum('forces_tagline', result)

    def edit_instrumentation_specifier(self):
        r'''Edits instrumentation specifier of score.

        Returns none.
        '''
        from scoremanager import editors
        target = self._get_instrumentation()
        editor = editors.InstrumentationEditor(
            session=self._session, 
            target=target,
            )
        editor._run()
        self._write_instrumentation(editor.target)

    def edit_title(self):
        r'''Edits title of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('new title')
        result = getter._run()
        if self._session._break_io_loop():
            return
        self._add_metadatum('title', result)
        self._io_manager.write_cache(prompt=False)

    def edit_year_of_completion(self):
        r'''Edits year of completion of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_integer_in_range(
            'year of completion', 
            start=1, 
            allow_none=True,
            )
        result = getter._run()
        if self._session._break_io_loop():
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
                    os.mkdir(path)
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
                with file(self._metadata_module_path, 'w') as file_pointer:
                    file_pointer.write(self._unicode_directive + '\n')
                    file_pointer.write(self._abjad_import_statement + '\n')
                    file_pointer.write('import collections\n')
                    file_pointer.write('\n')
                    file_pointer.write('\n')
                    string = 'metadata = collections.OrderedDict([])\n'
                    file_pointer.write(string)
        return package_needed_to_be_fixed

    def remove_score_package(self):
        r'''Removes score package.

        Returns none.
        '''
        line = 'WARNING! Score package {!r} will be completely removed.'
        line = line.format(self._package_name)
        self._io_manager.display([line, ''])
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string("type 'clobber' to proceed")
        with self._backtrack:
            should_clobber = getter._run()
        if self._session._break_io_loop():
            return
        if should_clobber == 'clobber':
            with self._backtrack:
                self._remove()
            if self._session._break_io_loop():
                return
            self._session._is_backtracking_locally = True

    def rename_score_package(self):
        r'''Renames score package.

        Returns none.
        '''
        pass
        with self._backtrack:
            prompt_string = 'new package name'
            new_path = self._score_package_wrangler.get_available_path(
                prompt_string=prompt_string)
        if self._session._break_io_loop():
            return
        lines = ['']
        line = 'current path: {!r}.'.format(self._path)
        lines.append(line)
        line = 'new path: {!r}.'.format(new_path)
        lines.append(line)
        lines.append('')
        self._io_manager.display(lines)
        with self._backtrack:
            confirm = self._io_manager.confirm()
        if self._session._break_io_loop():
            return
        if not confirm:
            return
        self._rename(new_path)
        self._io_manager.proceed()

    def view_score_pdf(self):
        r'''Views score PDF.

        Returns none.
        '''
        self._build_directory_manager._open_file_ending_with('score.pdf')