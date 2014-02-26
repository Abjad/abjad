# -*- encoding: utf-8 -*-
import os
from scoremanager.managers.PackageManager import PackageManager


class ScorePackageManager(PackageManager):

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        from scoremanager import managers
        from scoremanager import wranglers
        if filesystem_path is not None:
            assert os.path.sep in filesystem_path
        PackageManager.__init__(
            self, 
            filesystem_path=filesystem_path, 
            session=session,
            )
        package_path = self._configuration.path_to_package(filesystem_path)
        self._package_path = package_path
        filesystem_path = self._filesystem_path
        if filesystem_path is not None:
            filesystem_path = os.path.join(
                self._filesystem_path, 
                'build',
                )
        manager = managers.BuildDirectoryManager(
            filesystem_path=filesystem_path,
            session=self._session,
            )
        self._build_directory_manager = manager
        if filesystem_path is not None:
            filesystem_path = os.path.join(
                self._filesystem_path,
                'distribution',
                )
        manager = managers.DistributionDirectoryManager(
            filesystem_path=filesystem_path,
            session=self._session,
            )
        self._distribution_directory_manager = manager
        if self._filesystem_path is not None:
            instrumentation_module_file_path = os.path.join(
                self._filesystem_path,
                'instrumentation.py',
                )
        else:
            instrumentation_module_file_path = None
        self._instrumentation_module_manager = \
            managers.FileManager(
            instrumentation_module_file_path,
            session=self._session,
            )
        self._material_package_wrangler = \
            wranglers.MaterialPackageWrangler(
            session=self._session,
            )
        self._material_package_manager_wrangler = \
            wranglers.MaterialPackageManagerWrangler(
            session=self._session,
            )
        if self._filesystem_path is not None:
            filesystem_path = os.path.join(
                self._filesystem_path, 
                'templates',
                )
        else:
            filesystem_path = None
        self._score_template_directory_manager = \
            managers.DirectoryManager(
            filesystem_path=filesystem_path,
            session=self._session,
            )
        self._segment_package_wrangler = \
            wranglers.SegmentPackageWrangler(
            session=self._session,
            )
        self._stylesheet_wrangler = \
            wranglers.StylesheetFileWrangler(
            session=self._session,
            )
        #self._initialize_user_input_to_action()

    ### PRIVATE PROPERTIES ###

    @property
    def _backtracking_source(self):
        return 'score'

    @property
    def _breadcrumb(self):
        return self._get_annotated_title()

    ### PRIVATE METHODS ###

    def _get_annotated_title(self):
        if isinstance(self._get_metadatum('year_of_completion'), int):
            return self._get_title_with_year()
        else:
            return self._get_title()

    def _get_build_directory_path(self):
        return os.path.join(
            self._filesystem_path, 
            'build',
            )

    def _get_distribution_directory_path(self):
        return os.path.join(
            self._filesystem_path, 
            'distribution',
            )

    def _get_instrumentation(self):
        return self._import_instrumentation_from_instrumentation_module()

    def _get_instrumentation_module_file_path(self):
        file_path = os.path.join(
            self._filesystem_path,
            'instrumentation.py',
            )
        return file_path

    def _get_materials_directory_path(self):
        return os.path.join(
            self._filesystem_path, 
            'materials',
            )

    def _get_segments_directory_path(self):
        return os.path.join(
            self._filesystem_path, 
            'segments',
            )

    def _get_stylesheets_directory_path(self):
        return os.path.join(
            self._filesystem_path, 
            'stylesheets',
            )

    def _get_templates_directory_path(self):
        return os.path.join(
            self._filesystem_path, 
            'templates',
            )

    def _get_tempo_inventory(self):
        wrangler = self._material_package_wrangler
        for manager in wrangler._list_asset_managers(head=self._package_path):
            string = 'material_package_manager_class_name'
            class_name = manager._get_metadatum(string)
            if class_name == 'TempoInventoryMaterialPackageManager':
                return manager.output_material

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
        elif result == 'removescore':
            self.remove(),
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
            self._filesystem_path,
            'instrumentation.py',
            )
        manager = managers.FileManager(
            file_path,
            session=self._session,
            )
        instrumentation = manager._execute_file_lines(
            return_attribute_name='instrumentation',
            )
        return instrumentation

    def _make_main_menu(self):
        main_menu = self._io_manager.make_menu(where=self._where)
        command_section = main_menu.make_command_section()
        command_section.append(('build', 'u'))
        command_section.append(('makers', 'k'))
        command_section.append(('materials', 'm'))
        command_section.append(('segments', 'g'))
        command_section.append(('setup', 'p'))
        command_section.append(('templates', 't'))
        command_section.append(('stylesheets', 'y'))
        manager = self._build_directory_manager
        if manager._get_file_path_ending_with('score.pdf'):
            command_section = main_menu.make_command_section()
            command_section.append(('score pdf - view', 'pdfv'))
            command_section.default_index = len(command_section) - 1
        hidden_section = main_menu.make_command_section(is_secondary=True)
        hidden_section.append(('fix package structure', 'fix'))
        hidden_section.append(('list directory contents', 'ls'))
        hidden_section.append(('run pytest', 'pytest'))
        hidden_section.append(('remove score package', 'removescore'))
        hidden_section.append(('view initializer', 'inv'))
        hidden_section.append(('view instrumentation', 'instrumentation'))
        self._io_manager._make_metadata_menu_section(main_menu)
        self._io_manager._make_metadata_module_menu_section(main_menu)
        return main_menu

    def _make_setup_menu(self):
        menu = self._io_manager.make_menu(where=self._where)
        attribute_section = menu.make_attribute_section()
        menu_entries = self._make_setup_menu_entries()
        attribute_section.menu_entries = menu_entries
        command_section = menu.make_command_section()
        command_section.append(('instrumentation', 'instr'))
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
        file_path = self._get_instrumentation_module_file_path()
        file_pointer = file(file_path, 'w')
        file_pointer.write(''.join(lines))
        file_pointer.close()

    ### PUBLIC METHODS ###

    def edit_catalog_number(self):
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('Catalog number')
        result = getter._run()
        if self._session._backtrack():
            return
        self._add_metadatum('catalog_number', result)

    def edit_forces_tagline(self):
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('Forces tagline')
        result = getter._run()
        if self._session._backtrack():
            return
        self._add_metadatum('forces_tagline', result)

    def edit_instrumentation_specifier(self):
        from scoremanager import editors
        target = self._get_instrumentation()
        editor = editors.InstrumentationEditor(
            session=self._session, 
            target=target,
            )
        editor._run()
        self._write_instrumentation(editor.target)

    def edit_title(self):
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('new title')
        result = getter._run()
        if self._session._backtrack():
            return
        self._add_metadatum('title', result)
        self._io_manager._write_cache()

    def edit_year_of_completion(self):
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
        result = True
        for path in self._get_top_level_directory_paths():
            if not os.path.exists(path):
                result = False
                prompt = 'create {!r}? '.format(path)
                if not prompt or \
                    self._io_manager.confirm(prompt):
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
