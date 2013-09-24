# -*- encoding: utf-8 -*-
import os
from experimental.tools.scoremanagertools.proxies.PackageProxy \
    import PackageProxy


class ScorePackageProxy(PackageProxy):

    ### INITIALIZER ###

    def __init__(self, packagesystem_path=None, session=None):
        from experimental.tools import scoremanagertools
        PackageProxy.__init__(self, packagesystem_path, session=session)
        self._build_directory_manager = \
            scoremanagertools.proxies.BuildDirectoryManager(
            score_package_path=packagesystem_path, 
            session=self.session,
            )
        self._distribution_proxy = \
            scoremanagertools.proxies.DistributionDirectoryManager(
            score_package_path=packagesystem_path, 
            session=self.session,
            )
        package_path = '{}.instrumentation'.format(self.package_path)
        self._instrumentation_module_proxy = \
            scoremanagertools.proxies.ModuleProxy(
            package_path,
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
        self._score_template_directory_proxy = \
            scoremanagertools.proxies.DirectoryManager(
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

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        elif result == 'user entered lone return':
            pass
        else:
            message = 'unknown user input: {!r}.'.format(result)
            raise ValueError(message)

    def _make_main_menu(self):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        command_section = main_menu.make_command_section()
        command_section.append(('build directory', 'u'))
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
        hidden_section.append(('manage repository', 'svn'))
        hidden_section.append(('manage tags', 'tags'))
        hidden_section.append(('profile package structure', 'profile'))
        hidden_section.append(('run py.test', 'py.test'))
        hidden_section.append(('remove score package', 'removescore'))
        hidden_section.append(('view initializer', 'inv'))
        hidden_section.append(('view instrumentation', 'instrumentation'))
        hidden_section.append(('view metadata', 'metadata'))
        return main_menu

    ### PRIVATE PROPERTIES ###

    @property
    def _backtracking_source(self):
        return 'score'

    @property
    def _breadcrumb(self):
        return self.annotated_title

    ### PRIVATE METHODS ###

    def _get_instrumentation(self):
        instrumentation = self.get_tag('instrumentation')
        if instrumentation is None:
            instrumentation = \
                self._import_instrumentation_from_instrumentation_module()
        return instrumentation

    def _get_instrumentation_module_file_path(self):
        file_path = os.path.join(
            self.filesystem_path,
            'instrumentation.py',
            )
        return file_path

    def _import_instrumentation_from_instrumentation_module(self):
        from experimental.tools import scoremanagertools
        packagesystem_path = '.'.join([
            self.package_path,
            'instrumentation',
            ])
        proxy = scoremanagertools.proxies.ModuleProxy(
            packagesystem_path,
            session=self.session,
            )
        instrumentation = proxy.execute_file_lines(
            return_attribute_name='instrumentation',
            )
        return instrumentation
    
    def _make_setup_menu_entries(self):
        result = []
        return_value = 'title'
        prepopulated_value = None
        prepopulated_value = self.title or None
        result.append((return_value, None, prepopulated_value, return_value))
        return_value = 'year'
        prepopulated_value = None
        if self.year_of_completion:
            prepopulated_value = str(self.year_of_completion)
        result.append((return_value, None, prepopulated_value, return_value))
        forces_tagline = self.forces_tagline
        prepopulated_value = None
        return_value = 'tagline'
        if forces_tagline:
            prepopulated_value = self.forces_tagline
        result.append((return_value, None, prepopulated_value, return_value))
        return_value = 'performers'
        prepopulated_value = None
        instrumentation = self._get_instrumentation()
        if instrumentation:
            string = instrumentation.performer_name_string
            prepopulated_value = string
        result.append((return_value, None, prepopulated_value, return_value))
        return result

    def _write_instrumentation_to_disk(self, instrumentation):
        assert instrumentation is not None
        if self.get_tag('instrumentation') is not None:
            self.add_tag('instrumentation', instrumentation)
        else:
            lines = []
            lines.append('# -*- encoding: utf-8 -*-\n')
            lines.append('from abjad import *\n')
            lines.append('\n\n')
            line = 'instrumentation={}'
            line = line.format(instrumentation._storage_format)
            lines.append(line)
            file_path = self._get_instrumentation_module_file_path()
            file_pointer = file(file_path, 'w')
            file_pointer.write(''.join(lines))
            file_pointer.close()

    ### PUBLIC PROPERTIES ###

    @property
    def annotated_title(self):
        if isinstance(self.year_of_completion, int):
            return self.title_with_year
        else:
            return self.title

    @property
    def composer(self):
        return self.get_tag('composer')

    @property
    def distribution_pdf_directory_path(self):
        return os.path.join(self.distribution_proxy.filesystem_path, 'pdf')

    @property
    def distribution_proxy(self):
        return self._distribution_proxy

    @property
    def build_directory_manager(self):
        return self._build_directory_manager

    @apply
    def forces_tagline():
        def fget(self):
            return self.get_tag('forces_tagline')
        def fset(self, forces_tagline):
            return self.add_tag('forces_tagline', forces_tagline)
        return property(**locals())

    @property
    def has_correct_directory_structure(self):
        return all(os.path.exists(name) 
            for name in self.top_level_directory_paths)

    @property
    def has_correct_initializers(self):
        return all(os.path.exists(initializer) 
            for initializer in self.score_initializer_file_names)

    @property
    def has_correct_package_structure(self):
        if self.has_correct_directory_structure:
            if self.has_correct_initializers:
                return True
        return False

    @property
    def instrumentation(self):
        return self._get_instrumentation()

    @property
    def instrumentation_module_proxy(self):
        return self._instrumentation_module_proxy

    @property
    def material_package_maker_wrangler(self):
        return self._material_package_maker_wrangler

    @property
    def material_package_wrangler(self):
        return self._material_package_wrangler

    @property
    def materials_directory_path(self):
        return os.path.join(self.filesystem_path, 'materials')

    @property
    def materials_package_initializer_file_name(self):
        return os.path.join(self.materials_directory_path, '__init__.py')

    @property
    def materials_package_path(self):
        return '.'.join([self.package_path, 'materials'])

    @property
    def score_initializer_file_names(self):
        return (
            self.initializer_file_name,
            )

    @property
    def score_package_wranglers(self):
        return (
            self.segment_wrangler,
            self.material_package_wrangler,
            )

    @property
    def score_template_directory_proxy(self):
        return self._score_template_directory_proxy

    @property
    def segment_wrangler(self):
        return self._segment_wrangler

    @property
    def segments_directory_path(self):
        return os.path.join(self.filesystem_path, 'segments')

    @property
    def segments_package_initializer_file_name(self):
        return os.path.join(self.segments_directory_path, '__init__.py')

    @property
    def segments_package_path(self):
        return '.'.join([self.package_path, 'segments'])

    @property
    def stylesheet_wrangler(self):
        return self._stylesheet_wrangler

    @property
    def stylesheets_directory_path(self):
        return os.path.join(self.filesystem_path, 'stylesheets')

    @property
    def tempo_inventory(self):
        for proxy in self.material_package_wrangler.list_asset_proxies(
            head=self.package_path):
            if proxy.get_tag('material_package_maker_class_name') == \
                'TempoMarkInventoryMaterialPackageMaker':
                return proxy.output_material

    @property
    def title(self):
        return self.get_tag('title') or self.untitled_indicator

    @property
    def title_with_year(self):
        if self.year_of_completion:
            return '{} ({})'.format(self.title, self.year_of_completion)
        else:
            return self.title

    @property
    def top_level_directory_paths(self):
        return tuple([x.filesystem_path 
            for x in self.top_level_directory_proxies])

    @property
    def top_level_directory_proxies(self):
        return (
            self.distribution_proxy,
            self.build_directory_manager,
            )

    @property
    def untitled_indicator(self):
        return '(untitled score)'

    @apply
    def year_of_completion():
        def fget(self):
            return self.get_tag('year_of_completion')
        def fset(self, year_of_completion):
            return self.add_tag('year_of_completion', year_of_completion)
        return property(**locals())

    ### PUBLIC METHODS ###

    def fix(self, is_interactive=True):
        result = True
        for path in self.top_level_directory_paths:
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
        if not os.path.exists(self.tags_file_name):
            result = False
            prompt = 'create {}? '.format(self.tags_file_name)
            if not is_interactive or self.session.io_manager.confirm(prompt):
                tags_file = file(self.tags_file_name, 'w')
                tags_file.write('# -*- encoding: utf-8 -*-\n')
                tags_file.write('from abjad import *\n')
                tags_file.write('import collections\n')
                tags_file.write('\n')
                tags_file.write('\n')
                tags_file.write('tags = collections.OrderedDict([])\n')
                tags_file.close()
        if not os.path.exists(self.materials_directory_path):
            result = False
            prompt = 'create {}'.format(self.materials_directory_path)
            if not is_interactive or self.session.io_manager.confirm(prompt):
                os.mkdir(self.materials_directory_path)
        if not os.path.exists(self.materials_package_initializer_file_name):
            result = False
            file(self.materials_package_initializer_file_name, 'w').write('')
        if not os.path.exists(self.segments_directory_path):
            result = False
            prompt = 'create {}'.format(self.segments_directory_path)
            if not is_interactive or self.session.io_manager.confirm(prompt):
                os.mkdir(self.segments_directory_path)
        if not os.path.exists(self.segments_package_initializer_file_name):
            result = False
            file(self.segments_package_initializer_file_name, 'w').write('')
        if not os.path.exists(self.stylesheets_directory_path):
            result = False
            prompt = 'create {}'.format(self.stylesheets_directory_path)
            if not is_interactive or self.session.io_manager.confirm(prompt):
                os.mkdir(self.stylesheets_directory_path)
        self.session.io_manager.proceed('packaged structure fixed.', 
            is_interactive=is_interactive)
        return result

    def handle_setup_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'title':
            self.interactively_edit_title()
        elif result == 'year':
            self.interactively_edit_year_of_completion()
        elif result == 'tagline':
            self.interactively_edit_forces_tagline()
        elif result == 'performers':
            self.interactively_edit_instrumentation_specifier()
        elif result == 'user entered lone return':
            pass
        else:
            raise ValueError(result)

    def handle_svn_menu_result(self, result):
        if result == 'add':
            self.svn_add(is_interactive=True)
        elif result == 'ci':
            self.svn_ci(is_interactive=True)
            return True
        elif result == 'st':
            self.svn_st(is_interactive=True)
        else:
            raise ValueError

    def interactively_edit_forces_tagline(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('Forces tagline')
        result = getter._run()
        if self.session.backtrack():
            return
        self.add_tag('forces_tagline', result)

    def interactively_edit_instrumentation_specifier(self):
        from experimental.tools import scoremanagertools
        target = self._get_instrumentation()
        editor = scoremanagertools.editors.InstrumentationEditor(
            session=self.session, 
            target=target,
            )
        editor._run() # maybe check for backtracking after this?
        self._write_instrumentation_to_disk(editor.target)

    def interactively_edit_title(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('new title')
        result = getter._run()
        if self.session.backtrack():
            return
        self.add_tag('title', result)

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
        self.add_tag('year_of_completion', result)

    def interactively_make_score(self):
        self.session.io_manager.print_not_yet_implemented()

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
                self.remove()
            if self.session.backtrack():
                return
            self.session.is_backtracking_locally = True

    def interactively_view_score(self, pending_user_input=None):
        self.build_directory_manager.interactively_view_score(
            pending_user_input=pending_user_input,
            )

    def interactively_view_instrumentation_module(self):
        #return self.instrumentation_module_proxy.interactively_view()
        return self.instrumentation_module_proxy.interactively_edit()

    def make_asset_structure(self):
        self.fix_score_package_directory_structure(is_interactive=False)

    def make_setup_menu(self):
        setup_menu = self.session.io_manager.make_menu(where=self._where)
        attribute_section = setup_menu.make_attribute_section()
        attribute_section.menu_entries = self._make_setup_menu_entries()
        return setup_menu

    def make_svn_menu(self):
        svn_menu = self.session.io_manager.make_menu(where=self._where)
        command_section = svn_menu.make_command_section()
        command_section.append(('st', 'st'))
        command_section.append(('add', 'add'))
        command_section.append(('ci', 'ci'))
        return svn_menu

    def manage_build_directory(self):
        self.build_directory_manager._run()

    def manage_materials(self):
        self.material_package_wrangler._run(head=self.package_path)

    def manage_score_templates(self):
        self.score_template_directory_proxy._run()

    def manage_segments(self):
        self.segment_wrangler._run(head=self.package_path)

    def manage_setup(self, clear=True, cache=True):
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            breadcrumb = '{} - setup'.format(self.annotated_title)
            self.session.push_breadcrumb(breadcrumb)
            setup_menu = self.make_setup_menu()
            result = setup_menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self.handle_setup_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    def manage_stylesheets(self):
        self.stylesheet_wrangler._run(head=self.package_path)

    def manage_svn(self, clear=True, cache=False):
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb('repository commands')
            menu = self.make_svn_menu()
            result = menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self.handle_svn_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    def profile(self, prompt=True):
        if not os.path.exists(self.filesystem_path):
            message = 'directory {!r} does not exist.'
            message = message.format(self.filesystem_path)
            raise OSError(message)
        lines = []
        for subdirectory_path in self.top_level_directory_paths:
            lines.append('{} {}'.format(
                subdirectory_path.ljust(80), 
                os.path.exists(subdirectory_path)))
        for initializer in self.score_initializer_file_names:
            lines.append('{} {}'.format(
                initializer.ljust(80), 
                os.path.exists(initializer)))
        lines.append('')
        self.session.io_manager.display(lines)
        self.session.io_manager.proceed(is_interactive=prompt)

    def summarize_materials(self):
        wrangler = self.material_package_wrangler
        materials = wrangler.space_delimited_lowercase_names
        lines = []
        if not materials:
            lines.append('{}Materials (none yet)'.format(self._make_tab(1)))
        else:
            lines.append('{}Materials'.format(self._make_tab(1)))
        if materials:
            lines.append('')
        for i, material in enumerate(materials):
            lines.append('{}({}) {}'.format(
                self._make_tab(1), 
                i + 1, 
                material))
        self.session.io_manager.display(lines)

    def summarize_segments(self):
        segments = self.segment_wrangler.list_asset_names()
        lines = []
        if not segments:
            lines.append('{}Segments (none yet)'.format(self._make_tab(1)))
        else:
            lines.append('{}Segments'.format(self._make_tab(1)))
        for segment in segments:
            lines.append('{}{}'.format(self._make_tab(2), segment))
        lines.append('')
        self.session.io_manager.display(lines)

    ### UI MANIFEST ###

    user_input_to_action = PackageProxy.user_input_to_action.copy()
    user_input_to_action.update({
        'fix': fix,
        'g': manage_segments,
        'instrumentation': interactively_view_instrumentation_module,
        'm': manage_materials,
        'pdfv': interactively_view_score,
        'profile': profile,
        'removescore': interactively_remove,
        's': manage_setup,
        'svn': manage_svn,
        't': manage_score_templates,
        'u': manage_build_directory,
        'y': manage_stylesheets,
        })
