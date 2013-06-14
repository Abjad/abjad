import os
from experimental.tools.scoremanagertools.proxies.PackageProxy \
    import PackageProxy


class ScorePackageProxy(PackageProxy):

    ### INITIALIZER ###

    def __init__(self, packagesystem_path=None, session=None):
        from experimental.tools import scoremanagertools
        PackageProxy.__init__(self, packagesystem_path, session=session)
        self._distribution_proxy = \
            scoremanagertools.proxies.DistributionDirectoryProxy(
            score_package_path=packagesystem_path, session=self._session)
        self._exergue_directory_proxy = \
            scoremanagertools.proxies.ExergueDirectoryProxy(
            score_package_path=packagesystem_path, session=self._session)
        self._music_proxy = scoremanagertools.proxies.MusicPackageProxy(
            score_package_path=packagesystem_path, session=self._session)
        self._segment_wrangler = \
            scoremanagertools.wranglers.SegmentPackageWrangler(
            session=self._session)
        self._material_package_wrangler = \
            scoremanagertools.wranglers.MaterialPackageWrangler(
            session=self._session)
        self._material_package_maker_wrangler = \
            scoremanagertools.wranglers.MaterialPackageMakerWrangler(
            session=self._session)

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            raise ValueError

    def _make_main_menu(self):
        menu, menu_section = self._io.make_menu(
            where=self._where,
            return_value_attribute='key',
            )
        menu_section.append(('segments', 'h'))
        menu_section.append(('materials', 'm'))
        menu_section.append(('specifiers', 'f'))
        menu_section.append(('setup', 's'))
        hidden_section = menu.make_section(
            return_value_attribute='key',
            is_hidden=True,
            )
        hidden_section.append(('fix package structure', 'fix'))
        hidden_section.append(('list directory contents', 'ls'))
        hidden_section.append(('profile package structure', 'profile'))
        hidden_section.append(('run py.test', 'py.test'))
        hidden_section.append(('remove score package', 'removescore'))
        hidden_section.append(('manage repository', 'svn'))
        hidden_section.append(('manage tags', 'tags'))
        return menu

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _backtracking_source(self):
        return 'score'

    @property
    def _breadcrumb(self):
        return self.annotated_title

    ### READ-ONLY PUBLIC PROPERTIES ###

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
    def exergue_directory_proxy(self):
        return self._exergue_directory_proxy

    @property
    def has_correct_directory_structure(self):
        return all([os.path.exists(name) 
            for name in self.top_level_directory_paths])

    @property
    def has_correct_initializers(self):
        return all([os.path.exists(initializer) 
            for initializer in self.score_initializer_file_names])

    @property
    def has_correct_package_structure(self):
        if self.has_correct_directory_structure:
            if self.has_correct_initializers:
                return True
        return False

    @property
    def instrumentation(self):
        return self.get_tag('instrumentation')

    @property
    def material_package_maker_wrangler(self):
        return self._material_package_maker_wrangler

    @property
    def material_package_wrangler(self):
        return self._material_package_wrangler

    @property
    def materials_directory_path(self):
        return os.path.join(self.filesystem_path, 'music', 'materials')

    @property
    def materials_package_initializer_file_name(self):
        return os.path.join(self.materials_directory_path, '__init__.py')

    @property
    def materials_package_path(self):
        return '.'.join([self.package_path, 'music', 'materials'])

    @property
    def music_proxy(self):
        return self._music_proxy

    @property
    def music_specifier_module_wrangler(self):
        return self._music_specifier_module_wrangler

    @property
    def score_initializer_file_names(self):
        return (
            self.initializer_file_name,
            self.music_proxy.initializer_file_name,
            )

    @property
    def score_package_wranglers(self):
        return (
            self.segment_wrangler,
            self.material_package_wrangler,
            )

    @property
    def segment_wrangler(self):
        return self._segment_wrangler

    @property
    def segments_directory_path(self):
        return os.path.join(self.filesystem_path, 'music', 'segments')

    @property
    def segments_package_initializer_file_name(self):
        return os.path.join(self.segments_directory_path, '__init__.py')

    @property
    def segments_package_path(self):
        return '.'.join([self.package_path, 'music', 'segments'])

    @property
    def stylesheets_directory_path(self):
        return os.path.join(self.filesystem_path, 'music', 'stylesheets')

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
            self.exergue_directory_proxy,
            self.music_proxy,
            )

    @property
    def untitled_indicator(self):
        return '(untitled score)'

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def forces_tagline():
        def fget(self):
            return self.get_tag('forces_tagline')
        def fset(self, forces_tagline):
            return self.add_tag('forces_tagline', forces_tagline)
        return property(**locals())

    # TODO: reverse the order of body string and key throughout method
    @property
    def setup_value_menu_tokens(self):
        result = []
        if self.title:
            result.append(('title', 'title: {!r}'.format(self.title)))
        else:
            result.append(('title', 'title:'))
        if self.year_of_completion:
            result.append(('year', 'year: {!r}'.format(
                self.year_of_completion)))
        else:
            result.append(('year', 'year:'))
        if self.get_tag('instrumentation'):
            result.append(('performers', 'performers: {}'.format(
                self.get_tag('instrumentation').performer_name_string)))
        else:
            result.append(('performers', 'performers:'))
        if self.forces_tagline:
            result.append(('tagline', 'tagline: {!r}'.format(
                self.forces_tagline)))
        else:
            result.append(('tagline', 'tagline:'))
        result = [(x[1], x[0]) for x in result]
        return result

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
                if not is_interactive or self._io.confirm(prompt):
                    os.mkdir(path)
        if not os.path.exists(self.initializer_file_name):
            result = False
            prompt = 'create {}? '.format(self.initializer_file_name)
            if not is_interactive or self._io.confirm(prompt):
                initializer = file(self.initializer_file_name, 'w')
                initializer.write('')
                initializer.close()
        if not os.path.exists(self.music_proxy.initializer_file_name):
            result = False
            prompt = 'create {}? '.format(
                self.music_proxy.initializer_file_name)
            if not is_interactive or self._io.confirm(prompt):
                initializer = file(self.music_proxy.initializer_file_name, 'w')
                initializer.write('')
                initializer.close()
        lines = []
        initializer = file(self.music_proxy.initializer_file_name, 'r')
        found_materials_import = False
        for line in initializer.readlines():
            lines.append(line)
            if line.startswith('import materials'):
                found_materials_import = True
        initializer.close()
        if not found_materials_import:
            result = False
            lines.insert(0, 'import materials\n')
            initializer = file(self.music_proxy.initializer_file_name, 'w')
            initializer.write(''.join(lines))
            initializer.close()
        if not os.path.exists(self.tags_file_name):
            result = False
            prompt = 'create {}? '.format(self.tags_file_name)
            if not is_interactive or self._io.confirm(prompt):
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
            if not is_interactive or self._io.confirm(prompt):
                os.mkdir(self.materials_directory_path)
        if not os.path.exists(self.materials_package_initializer_file_name):
            result = False
            file(self.materials_package_initializer_file_name, 'w').write('')
        if not os.path.exists(self.segments_directory_path):
            result = False
            prompt = 'create {}'.format(self.segments_directory_path)
            if not is_interactive or self._io.confirm(prompt):
                os.mkdir(self.segments_directory_path)
        if not os.path.exists(self.segments_package_initializer_file_name):
            result = False
            file(self.segments_package_initializer_file_name, 'w').write('')
        if not os.path.exists(self.stylesheets_directory_path):
            result = False
            prompt = 'create {}'.format(self.stylesheets_directory_path)
            if not is_interactive or self._io.confirm(prompt):
                os.mkdir(self.stylesheets_directory_path)
        self._io.proceed('packaged structure fixed.', 
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
        else:
            raise ValueError()

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
        getter = self._io.make_getter(where=self._where)
        getter.append_string('Forces tagline')
        result = getter._run()
        if self._session.backtrack():
            return
        self.add_tag('forces_tagline', result)

    def interactively_edit_instrumentation_specifier(self):
        from experimental.tools import scoremanagertools
        target = self.get_tag('instrumentation')
        editor = scoremanagertools.editors.InstrumentationEditor(
            session=self._session, target=target)
        editor._run() # maybe check for backtracking after this?
        self.add_tag('instrumentation', editor.target)

    def interactively_edit_title(self):
        getter = self._io.make_getter(where=self._where)
        getter.append_string('new title')
        result = getter._run()
        if self._session.backtrack():
            return
        self.add_tag('title', result)

    def interactively_edit_year_of_completion(self):
        getter = self._io.make_getter(where=self._where)
        getter.append_integer_in_range('year of completion', 
            start=1, allow_none=True)
        result = getter._run()
        if self._session.backtrack():
            return
        self.add_tag('year_of_completion', result)

    def interactively_make_score(self):
        self._io.print_not_yet_implemented()

    def interactively_remove(self):
        line = 'WARNING! Score package {!r} will be completely removed.'
        line = line.format(self.package_path)
        self._io.display([line, ''])
        getter = self._io.make_getter(where=self._where)
        getter.append_string("type 'clobberscore' to proceed")
        with self.backtracking:
            should_clobber = getter._run()
        if self._session.backtrack():
            return
        if should_clobber == 'clobberscore':
            with self.backtracking:
                self.remove()
            if self._session.backtrack():
                return
            self._session.is_backtracking_locally = True

    def make_asset_structure(self):
        self.fix_score_package_directory_structure(is_interactive=False)

    def make_setup_menu(self):
        setup_menu, menu_section = self._io.make_menu(
            where=self._where,
            return_value_attribute='key',
            is_numbered=True,
            )
        menu_section.menu_tokens = self.setup_value_menu_tokens
        return setup_menu

    def make_svn_menu(self):
        menu, menu_section = self._io.make_menu(
            where=self._where,
            return_value_attribute='key',
            )
        menu_section.append(('st', 'st'))
        menu_section.append(('add', 'add'))
        menu_section.append(('ci', 'ci'))
        return menu

    def manage_materials(self):
        self.material_package_wrangler._run(head=self.package_path)

    def manage_segments(self):
        self.segment_wrangler._run(head=self.package_path)

    def manage_setup(self, clear=True, cache=True):
        self._session.cache_breadcrumbs(cache=cache)
        while True:
            breadcrumb = '{} - setup'.format(self.annotated_title)
            self._session.push_breadcrumb(breadcrumb)
            setup_menu = self.make_setup_menu()
            result = setup_menu._run(clear=clear)
            if self._session.backtrack():
                break
            elif not result:
                self._session.pop_breadcrumb()
                continue
            self.handle_setup_menu_result(result)
            if self._session.backtrack():
                break
            self._session.pop_breadcrumb()
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)

    def manage_specifiers(self):
        self.music_speicifer_module_wrangler._run()

    def manage_svn(self, clear=True, cache=False):
        self._session.cache_breadcrumbs(cache=cache)
        while True:
            self._session.push_breadcrumb('repository commands')
            menu = self.make_svn_menu()
            result = menu._run(clear=clear)
            if self._session.backtrack():
                break
            elif not result:
                self._session.pop_breadcrumb()
                continue
            self.handle_svn_menu_result(result)
            if self._session.backtrack():
                break
            self._session.pop_breadcrumb()
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)

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
        self._io.display(lines)
        self._io.proceed(is_interactive=prompt)

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
        self._io.display(lines)

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
        self._io.display(lines)

    ### UI MANIFEST ###

    user_input_to_action = PackageProxy.user_input_to_action.copy()
    user_input_to_action.update({
        'h': manage_segments,
        'm': manage_materials,
        'f': manage_specifiers,
        's': manage_setup,
        'fix': fix,
        'profile': profile,
        'removescore': interactively_remove,
        'svn': manage_svn,
        })
