# -*- encoding: utf-8 -*-
import os
from experimental.tools.scoremanagertools.managers.PackageManager \
    import PackageManager


class ScorePackageManager(PackageManager):

    ### INITIALIZER ###

    def __init__(self, packagesystem_path=None, session=None):
        from experimental.tools import scoremanagertools
        PackageManager.__init__(
            self, 
            packagesystem_path, 
            session=session,
            )
        self._build_directory_manager = \
            scoremanagertools.managers.BuildDirectoryManager(
            score_package_path=packagesystem_path, 
            session=self.session,
            )
        self._distribution_directory_manager = \
            scoremanagertools.managers.DistributionDirectoryManager(
            score_package_path=packagesystem_path, 
            session=self.session,
            )
        #package_path = '{}.instrumentation'.format(self.package_path)
        instrumentation_module_file_path = os.path.join(
            self.filesystem_path,
            'instrumentation.py',
            )
        self._instrumentation_module_manager = \
            scoremanagertools.managers.FileManager(
            #package_path,
            instrumentation_module_file_path,
            session=self.session,
            )
        self._material_package_wrangler = \
            scoremanagertools.wranglers.MaterialPackageWrangler(
            session=self.session,
            )
        self._material_package_maker_wrangler = \
            scoremanagertools.wranglers.MaterialPackageMakerWrangler(
            session=self.session,
            )
        filesystem_path = os.path.join(self.filesystem_path, 'score_templates')
        self._score_template_directory_manager = \
            scoremanagertools.managers.DirectoryManager(
            filesystem_path=filesystem_path,
            session=self.session,
            )
        self._segment_wrangler = \
            scoremanagertools.wranglers.SegmentPackageWrangler(
            session=self.session,
            )
        self._stylesheet_wrangler = \
            scoremanagertools.wranglers.StylesheetFileWrangler(
            session=self.session,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _backtracking_source(self):
        return 'score'

    @property
    def _breadcrumb(self):
        return self._get_annotated_title()

    ### PRIVATE METHODS ###

    def _get_annotated_title(self):
        if isinstance(self._get_metadata('year_of_completion'), int):
            return self._get_title_with_year()
        else:
            return self._get_title()

    def _get_build_directory_path(self):
        return os.path.join(
            self.filesystem_path, 
            'build',
            )

    def _get_distribution_directory_path(self):
        return os.path.join(
            self.filesystem_path, 
            'distribution',
            )

    def _get_instrumentation(self):
        return self._import_instrumentation_from_instrumentation_module()

    def _get_instrumentation_module_file_path(self):
        file_path = os.path.join(
            self.filesystem_path,
            'instrumentation.py',
            )
        return file_path

    def _get_materials_directory_path(self):
        return os.path.join(
            self.filesystem_path, 
            'materials',
            )

    def _get_score_templates_directory_path(self):
        return os.path.join(
            self.filesystem_path, 
            'score_templates',
            )

    def _get_segments_directory_path(self):
        return os.path.join(
            self.filesystem_path, 
            'segments',
            )

    def _get_stylesheets_directory_path(self):
        return os.path.join(
            self.filesystem_path, 
            'stylesheets',
            )

    def _get_tempo_inventory(self):
        wrangler = self.material_package_wrangler
        for manager in wrangler.list_asset_managers(head=self.package_path):
            class_name = manager._get_metadata('material_package_maker_class_name')
            if class_name == 'TempoInventoryMaterialPackageMaker':
                return manager.output_material

    def _get_title(self):
        return self._get_metadata('title') or '(untitled score)'

    def _get_title_with_year(self):
        if self._get_metadata('year_of_completion'):
            result = '{} ({})'
            result = result.format(
                self._get_title(), 
                self._get_metadata('year_of_completion')
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
            self._get_score_templates_directory_path(),
            self._get_stylesheets_directory_path(),
            )

    def _handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        elif result == 'user entered lone return':
            pass
        else:
            message = 'unknown user input: {!r}.'
            message = message.format(result)
            raise ValueError(message)

    def _handle_repository_menu_result(self, result):
        if result == 'add':
            self.repository_add(is_interactive=True)
        elif result == 'ci':
            self.repository_ci(is_interactive=True)
            return True
        elif result == 'st':
            self.repository_st(is_interactive=True)
        elif result == 'up':
            self.repository_up(is_interactive=True)
        else:
            raise ValueError(result)

    def _handle_setup_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'catalog number':
            self.interactively_edit_catalog_number()   
        elif result == 'instr':
            self.interactively_edit_instrumentation_specifier()
        elif result == 'tagline':
            self.interactively_edit_forces_tagline()
        elif result == 'title':
            self.interactively_edit_title()
        elif result == 'year':
            self.interactively_edit_year_of_completion()
        elif result == 'user entered lone return':
            pass
        else:
            raise ValueError(result)

    def _import_instrumentation_from_instrumentation_module(self):
        from experimental.tools import scoremanagertools
        file_path = os.path.join(
            self.filesystem_path,
            'instrumentation.py',
            )
        manager = scoremanagertools.managers.FileManager(
            file_path,
            session=self.session,
            )
        instrumentation = manager._execute_file_lines(
            return_attribute_name='instrumentation',
            )
        return instrumentation
    
    def _make_main_menu(self):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        command_section = main_menu.make_command_section()
        command_section.append(('build directory', 'u'))
        #command_section.append(('callables', 'c'))
        command_section.append(('materials', 'm'))
        command_section.append(('score segments', 'g'))
        command_section.append(('score setup', 's'))
        command_section.append(('score templates', 't'))
        command_section.append(('stylesheets', 'y'))
        manager = self.build_directory_manager
        if manager._get_file_path_ending_with('score.pdf'):
            command_section = main_menu.make_command_section()
            command_section.append(('score pdf - view', 'pdfv'))
            command_section.default_index = len(command_section) - 1
        hidden_section = main_menu.make_command_section(is_hidden=True)
        hidden_section.append(('fix package structure', 'fix'))
        hidden_section.append(('list directory contents', 'ls'))
        hidden_section.append(('manage repository', 'rep'))
        hidden_section.append(('manage tags', 'tags'))
        hidden_section.append(('profile package structure', 'profile'))
        hidden_section.append(('run pytest', 'pytest'))
        hidden_section.append(('remove score package', 'removescore'))
        hidden_section.append(('view initializer', 'inv'))
        hidden_section.append(('view instrumentation', 'instrumentation'))
        hidden_section.append(('view metadata', 'metadata'))
        return main_menu

    def _make_repository_menu(self):
        menu = self.session.io_manager.make_menu(where=self._where)
        command_section = menu.make_command_section()
        command_section.append(('add', 'add'))
        command_section.append(('commit', 'ci'))
        command_section.append(('status', 'st'))
        command_section.append(('update', 'up'))
        return menu

    def _make_setup_menu(self):
        menu = self.session.io_manager.make_menu(where=self._where)
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
        forces_tagline = self._get_metadata('forces_tagline')
        prepopulated_value = None
        return_value = 'tagline'
        if forces_tagline:
            prepopulated_value = forces_tagline
        result.append((return_value, None, prepopulated_value, return_value))
        return_value = 'year'
        prepopulated_value = None
        year_of_completion = self._get_metadata('year_of_completion')
        if year_of_completion:
            prepopulated_value = str(year_of_completion)
        result.append((return_value, None, prepopulated_value, return_value))
        catalog_number = self._get_metadata('catalog_number')
        prepopulated_value = None
        return_value = 'catalog number'
        if catalog_number:
            prepopulated_value = catalog_number
        result.append((return_value, None, prepopulated_value, return_value))
        return result

    def _write_instrumentation_to_disk(self, instrumentation):
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

    ### PUBLIC PROPERTIES ###

    @property
    def build_directory_manager(self):
        return self._build_directory_manager

    @property
    def distribution_directory_manager(self):
        return self._distribution_directory_manager

    @property
    def instrumentation_module_manager(self):
        return self._instrumentation_module_manager

    @property
    def material_package_maker_wrangler(self):
        return self._material_package_maker_wrangler

    @property
    def material_package_wrangler(self):
        return self._material_package_wrangler

    @property
    def score_template_directory_manager(self):
        return self._score_template_directory_manager

    @property
    def segment_wrangler(self):
        return self._segment_wrangler

    @property
    def stylesheet_wrangler(self):
        return self._stylesheet_wrangler

    ### PUBLIC METHODS ###

    def interactively_edit_catalog_number(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('Catalog number')
        result = getter._run()
        if self.session.backtrack():
            return
        self._add_metadata('catalog_number', result)

    def interactively_edit_forces_tagline(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('Forces tagline')
        result = getter._run()
        if self.session.backtrack():
            return
        self._add_metadata('forces_tagline', result)

    def interactively_edit_instrumentation_specifier(self):
        from experimental.tools import scoremanagertools
        target = self._get_instrumentation()
        editor = scoremanagertools.editors.InstrumentationEditor(
            session=self.session, 
            target=target,
            )
        editor._run()
        self._write_instrumentation_to_disk(editor.target)

    def interactively_edit_title(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('new title')
        result = getter._run()
        if self.session.backtrack():
            return
        self._add_metadata('title', result)

    def interactively_edit_year_of_completion(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_integer_in_range(
            'year of completion', 
            start=1, 
            allow_none=True,
            )
        result = getter._run()
        if self.session.backtrack():
            return
        self._add_metadata('year_of_completion', result)

    def interactively_fix(self, is_interactive=True):
        result = True
        for path in self._get_top_level_directory_paths():
            if not os.path.exists(path):
                result = False
                prompt = 'create {!r}? '.format(path)
                if not is_interactive or \
                    self.session.io_manager.confirm(prompt):
                    os.mkdir(path)
        if not os.path.exists(self.initializer_file_name):
            result = False
            prompt = 'create {}? '.format(self.initializer_file_name)
            if not is_interactive or self.session.io_manager.confirm(prompt):
                initializer = file(self.initializer_file_name, 'w')
                initializer.write('')
                initializer.close()
        lines = []
        if not os.path.exists(self.metadata_module_name):
            result = False
            prompt = 'create {}? '.format(self.metadata_module_name)
            if not is_interactive or self.session.io_manager.confirm(prompt):
                metadata_module = file(self.metadata_module_name, 'w')
                metadata_module.write('# -*- encoding: utf-8 -*-\n')
                metadata_module.write('from abjad import *\n')
                metadata_module.write('import collections\n')
                metadata_module.write('\n')
                metadata_module.write('\n')
                metadata_module.write('tags = collections.OrderedDict([])\n')
                metadata_module.close()
        if not os.path.exists(self._get_materials_directory_path()):
            result = False
            prompt = 'create {}'.format(self._get_materials_directory_path())
            if not is_interactive or self.session.io_manager.confirm(prompt):
                os.mkdir(self._get_materials_directory_path())
        if not os.path.exists(self._get_segments_directory_path()):
            result = False
            prompt = 'create {}'.format(self._get_segments_directory_path())
            if not is_interactive or self.session.io_manager.confirm(prompt):
                os.mkdir(self._get_segments_directory_path())
        if not os.path.exists(self._get_stylesheets_directory_path()):
            result = False
            prompt = 'create {}'.format(self._get_stylesheets_directory_path())
            if not is_interactive or self.session.io_manager.confirm(prompt):
                os.mkdir(self._get_stylesheets_directory_path())
        message = 'packaged structure fixed.'
        self.session.io_manager.proceed(message, is_interactive=is_interactive)
        return result

    def interactively_profile(self, prompt=True):
        if not os.path.exists(self.filesystem_path):
            message = 'directory {!r} does not exist.'
            message = message.format(self.filesystem_path)
            raise OSError(message)
        lines = []
        for directory_path in self._get_top_level_directory_paths():
            if os.path.exists(directory_path):
                result = 'exists'
            else:
                result = "doesn't exist"
            line = '{} {}.'
            directory_path = directory_path.replace(
                self.configuration.user_score_packages_directory_path,
                '...',
                )
            directory_path = directory_path.replace(
                self.configuration.built_in_score_packages_directory_path,
                '...',
                )
            line = line.format(directory_path, result)
            lines.append(line)
        lines.append('')
        self.session.io_manager.display(lines)
        self.session.io_manager.proceed(is_interactive=prompt)

    def interactively_remove(self):
        line = 'WARNING! Score package {!r} will be completely removed.'
        line = line.format(self.package_path)
        self.session.io_manager.display([line, ''])
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string("type 'clobberscore' to proceed")
        with self.backtracking:
            should_clobber = getter._run()
        if self.session.backtrack():
            return
        if should_clobber == 'clobberscore':
            with self.backtracking:
                self._remove()
            if self.session.backtrack():
                return
            self.session.is_backtracking_locally = True

    def interactively_view_instrumentation_module(self):
        #return self.instrumentation_module_manager.interactively_view()
        return self.instrumentation_module_manager.interactively_edit()

    def interactively_view_score(self, pending_user_input=None):
        self.build_directory_manager._interactively_open_file_ending_with(
            'score.pdf',
            )

    def manage_build_directory(self):
        self.build_directory_manager._run()

    def manage_materials(self):
        self.material_package_wrangler._run(head=self.package_path)

    def manage_repository(self, clear=True, cache=False):
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb('repository commands')
            menu = self._make_repository_menu()
            result = menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self._handle_repository_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    def manage_score_templates(self):
        self.score_template_directory_manager._run()

    def manage_segments(self):
        self.segment_wrangler._run(head=self.package_path)

    def manage_setup(self, clear=True, cache=True):
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            annotated_title = self._get_annotated_title()
            breadcrumb = '{} - setup'.format(annotated_title)
            self.session.push_breadcrumb(breadcrumb)
            setup_menu = self._make_setup_menu()
            result = setup_menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self._handle_setup_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    def manage_stylesheets(self):
        self.stylesheet_wrangler._run(head=self.package_path)

    ### UI MANIFEST ###

    user_input_to_action = PackageManager.user_input_to_action.copy()
    user_input_to_action.update({
        'fix': interactively_fix,
        'g': manage_segments,
        'instrumentation': interactively_view_instrumentation_module,
        'm': manage_materials,
        'pdfv': interactively_view_score,
        'profile': interactively_profile,
        'removescore': interactively_remove,
        'rep': manage_repository,
        's': manage_setup,
        't': manage_score_templates,
        'u': manage_build_directory,
        'y': manage_stylesheets,
        })
