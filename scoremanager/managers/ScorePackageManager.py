# -*- encoding: utf-8 -*-
import os
from scoremanager.managers.PackageManager import PackageManager


class ScorePackageManager(PackageManager):

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        PackageManager.__init__(
            self, 
            path=path, 
            session=session,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _backtracking_source(self):
        return 'score'

    @property
    def _breadcrumb(self):
        return self._get_annotated_title()

    @property
    def _build_directory_manager(self):
        from scoremanager import managers
        if self._path is None:
            return
        if not hasattr(self, '_cached_build_directory_manager'):
            path = os.path.join(self._path, 'build')
            manager = managers.BuildDirectoryManager(
                path=path,
                session=self._session,
                )
            self._cached_build_directory_manager = manager
        return self._cached_build_directory_manager

    @property
    def _distribution_directory_manager(self):
        from scoremanager import managers
        if self._path is None:
            return
        if not hasattr(self, '_cached_distribution_directory_manager'):
            path = os.path.join(self._path, 'distribution')
            manager = managers.DistributionDirectoryManager(
                path=path,
                session=self._session,
                )
            self._cached_distribution_directory_manager = manager
        return self._cached_distribution_directory_manager

    @property
    def _instrumentation_module_manager(self):
        from scoremanager import managers
        if self._path is None:
            return
        if not hasattr(self, '_cached_instrumentation_module_manager'):
            path = os.path.join(self._path, 'instrumentation.py')
            manager = managers.FileManager(
                path,
                session=self._session,
                )
            self._cached_instrumentation_module_manager = manager
        return self._cached_instrumentation_module_manager

    @property
    def _material_package_wrangler(self):
        from scoremanager import wranglers
        if self._path is None:
            return
        if not hasattr(self, '_cached_material_package_wrangler'):
            wrangler = wranglers.MaterialPackageWrangler(session=self._session)
            self._cached_material_package_wrangler = wrangler
        return self._cached_material_package_wrangler

    @property
    def _material_manager_wrangler(self):
        from scoremanager import wranglers
        if self._path is None:
            return
        if not hasattr(self, '_cached_material_manager_wrangler'):
            wrangler = wranglers.MaterialManagerWrangler(session=self._session)
            self._cached_material_manager_wrangler = wrangler
        return self._cached_material_manager_wrangler

    @property
    def _score_template_directory_manager(self):
        from scoremanager import managers
        if self._path is None:
            return
        if not hasattr(self, '_cached_score_template_directory_manager'):
            path = os.path.join(self._path, 'templates')
            manager = managers.DirectoryManager(
                path=path,
                session=self._session,
            )
            self._cached_score_template_directory_manager = manager
        return self._cached_score_template_directory_manager


    @property
    def _segment_package_wrangler(self):
        from scoremanager import wranglers
        if self._path is None:
            return
        if not hasattr(self, '_cached_segment_package_wrangler'):
            wrangler = wranglers.SegmentPackageWrangler(session=self._session)
            self._cached_segment_package_wrangler = wrangler
        return self._cached_segment_package_wrangler

    @property
    def _stylesheet_wrangler(self):
        from scoremanager import wranglers
        if self._path is None:
            return
        if not hasattr(self, '_cached_stylesheet_wrangler'):
            wrangler = wranglers.StylesheetWrangler(session=self._session)
            self._cached_stylesheet_wrangler = wrangler
        return self._cached_stylesheet_wrangler

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

    def _get_templates_directory_path(self):
        return os.path.join(
            self._path, 
            'templates',
            )

    def _get_tempo_inventory(self):
        wrangler = self._material_package_wrangler
        for manager in wrangler._list_asset_managers(head=self._package_path):
            string = 'material_manager_class_name'
            class_name = manager._get_metadatum(string)
            if class_name == 'TempoInventoryMaterialManager':
                output_material = manager._execute_output_material_module()
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
            self._get_materials_directory_path(),
            self._get_segments_directory_path(),
            self._get_templates_directory_path(),
            self._get_stylesheets_directory_path(),
            )

    # TODO: change back to implementation with instance dictionary
    def _handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'fix':
            self.fix(),
        elif result == 'g':
            self._segment_package_wrangler._run(head=self._package_path)
        elif result == 'instrumentation':
            self._instrumentation_module_manager.edit()
        elif result == 'k':
            self._io_manager.print_not_yet_implemented()
            #self._maker_module_wrangler._run(head=self._package_path)
        elif result == 'm':
            self._material_package_wrangler._run(head=self._package_path)
        elif result == 'p':
            self._manage_setup(),
        elif result == 'pdfv':
            self._build_directory_manager._open_file_ending_with(
                'score.pdf',
                )
        elif result == 'radd':
            self.add()
        elif result == 'rci':
            self.commit()
        elif result == 'removescore':
            self.remove(),
        elif result == 'rst':
            self.status()
        elif result == 'rup':
            self.update()
        elif result == 't':
            self._score_template_directory_manager._run()
        elif result == 'u':
            self._build_directory_manager._run()
        elif result == 'y':
            self._stylesheet_wrangler._run(head=self._package_path)
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
        instrumentation = manager._execute(
            return_attribute_name='instrumentation',
            )
        return instrumentation

    def _make_main_menu(self):
        menu = self._io_manager.make_menu(where=self._where)
        section = menu.make_command_section()
        section.append(('build', 'u'))
        section.append(('makers', 'k'))
        section.append(('materials', 'm'))
        section.append(('segments', 'g'))
        section.append(('setup', 'p'))
        section.append(('templates', 't'))
        section.append(('stylesheets', 'y'))
        manager = self._build_directory_manager
        if manager._get_file_path_ending_with('score.pdf'):
            section = menu.make_command_section()
            section.append(('score pdf - view', 'pdfv'))
            section.default_index = len(section) - 1
        # TODO: restructure with encapsulated methods
        section = menu.make_command_section(is_secondary=True)
        section.append(('package - fix', 'fix'))
        section.append(('directory - list', 'ls'))
        section.append(('Python - test', 'pyt'))
        section.append(('score - remove', 'removescore'))
        section.append(('initializer - view', 'inv'))
        section.append(('instrumentation - view', 'instrumentation'))
        self._io_manager._make_metadata_menu_section(menu)
        self._io_manager._make_metadata_module_menu_section(menu)
        return menu

    def _make_setup_menu(self):
        menu = self._io_manager.make_menu(where=self._where)
        attribute_section = menu.make_attribute_section()
        menu_entries = self._make_setup_menu_entries()
        attribute_section.menu_entries = menu_entries
        section = menu.make_command_section()
        section.append(('instrumentation', 'instr'))
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

    def _manage_setup(self, clear=True, cache=True):
        self._session._cache_breadcrumbs(cache=cache)
        while True:
            annotated_title = self._get_annotated_title()
            breadcrumb = '{} - setup'.format(annotated_title)
            self._session._push_breadcrumb(breadcrumb)
            setup_menu = self._make_setup_menu()
            result = setup_menu._run(clear=clear)
            if self._session._backtrack():
                break
            elif not result:
                self._session._pop_breadcrumb()
                continue
            self._handle_setup_menu_result(result)
            if self._session._backtrack():
                break
            self._session._pop_breadcrumb()
        self._session._pop_breadcrumb()
        self._session._restore_breadcrumbs(cache=cache)

    def _write_instrumentation(self, instrumentation):
        assert instrumentation is not None
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('from abjad import *\n')
        lines.append('\n\n')
        line = 'instrumentation={}'
        line = line.format(format(instrumentation))
        lines.append(line)
        file_path = self._get_instrumentation_module_path()
        file_pointer = file(file_path, 'w')
        file_pointer.write(''.join(lines))
        file_pointer.close()

    ### PUBLIC METHODS ###

    def edit_catalog_number(self):
        r'''Edits catalog number of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('catalog number')
        result = getter._run()
        if self._session._backtrack():
            return
        self._add_metadatum('catalog_number', result)

    def edit_forces_tagline(self):
        r'''Edits forces tagline of score.

        Returns none.
        '''
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('Forces tagline')
        result = getter._run()
        if self._session._backtrack():
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
        if self._session._backtrack():
            return
        self._add_metadatum('title', result)
        self._io_manager._write_cache()

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
        if self._session._backtrack():
            return
        self._add_metadatum('year_of_completion', result)

    def fix(self, prompt=True):
        r'''Fixes score package structure.

        Returns none.
        '''
        result = True
        for path in self._get_top_level_directory_paths():
            if not os.path.exists(path):
                result = False
                prompt = 'create {!r}? '.format(path)
                if not prompt or self._io_manager.confirm(prompt):
                    os.mkdir(path)
        if not os.path.exists(self._initializer_file_path):
            result = False
            prompt = 'create {}? '.format(self._initializer_file_path)
            if not prompt or self._io_manager.confirm(prompt):
                initializer = file(self._initializer_file_path, 'w')
                initializer.write('')
                initializer.close()
        lines = []
        if not os.path.exists(self._metadata_module_path):
            result = False
            prompt = 'create {}? '.format(self._metadata_module_path)
            if not prompt or self._io_manager.confirm(prompt):
                metadata_module = file(self._metadata_module_path, 'w')
                metadata_module.write('# -*- encoding: utf-8 -*-\n')
                metadata_module.write('from abjad import *\n')
                metadata_module.write('import collections\n')
                metadata_module.write('\n')
                metadata_module.write('\n')
                metadata_module.write('metadata = collections.OrderedDict([])\n')
                metadata_module.close()
        if not os.path.exists(self._get_materials_directory_path()):
            result = False
            prompt = 'create {}'.format(self._get_materials_directory_path())
            if not prompt or self._io_manager.confirm(prompt):
                os.mkdir(self._get_materials_directory_path())
        if not os.path.exists(self._get_segments_directory_path()):
            result = False
            prompt = 'create {}'.format(self._get_segments_directory_path())
            if not prompt or self._io_manager.confirm(prompt):
                os.mkdir(self._get_segments_directory_path())
        if not os.path.exists(self._get_stylesheets_directory_path()):
            result = False
            prompt = 'create {}'.format(self._get_stylesheets_directory_path())
            if not prompt or self._io_manager.confirm(prompt):
                os.mkdir(self._get_stylesheets_directory_path())
        message = 'packaged structure fixed.'
        self._io_manager.proceed(message, prompt=prompt)
        return result

    def remove(self):
        r'''Removes score package.

        Returns none.
        '''
        line = 'WARNING! Score package {!r} will be completely removed.'
        line = line.format(self._package_path)
        self._io_manager.display([line, ''])
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string("type 'clobberscore' to proceed")
        with self._backtracking:
            should_clobber = getter._run()
        if self._session._backtrack():
            return
        if should_clobber == 'clobberscore':
            with self._backtracking:
                self._remove()
            if self._session._backtrack():
                return
            self._session._is_backtracking_locally = True
