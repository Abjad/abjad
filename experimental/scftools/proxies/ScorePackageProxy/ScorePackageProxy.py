from scftools.proxies.PackageProxy import PackageProxy
import os


class ScorePackageProxy(PackageProxy):

    def __init__(self, score_package_short_name=None, session=None):
        import scftools
        PackageProxy.__init__(self, score_package_short_name, session=session)
        self._dist_proxy = scftools.proxies.DistDirectoryProxy(
            score_package_short_name=score_package_short_name, session=self.session)
        self._etc_proxy = scftools.proxies.EtcDirectoryProxy(
            score_package_short_name=score_package_short_name, session=self.session)
        self._exg_proxy = scftools.proxies.ExgDirectoryProxy(
            score_package_short_name=score_package_short_name, session=self.session)
        self._mus_proxy = scftools.proxies.MusPackageProxy(
            score_package_short_name=score_package_short_name, session=self.session)
        self._chunk_wrangler = scftools.wranglers.ChunkPackageWrangler(
            session=self.session)
        self._material_package_wrangler = scftools.wranglers.MaterialPackageWrangler(
            session=self.session)
        self._material_package_maker_wrangler = scftools.wranglers.MaterialPackageMakerWrangler(
            session=self.session)
        self._music_specifier_module_wrangler = scftools.wranglers.MusicSpecifierModuleWrangler(
            session=self.session)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def annotated_title(self):
        if isinstance(self.year_of_completion, int):
            return self.title_with_year
        else:
            return self.title

    @property
    def backtracking_source(self):
        return 'score'

    @property
    def breadcrumb(self):
        return self.annotated_title

    @property
    def chunk_wrangler(self):
        return self._chunk_wrangler

    @property
    def chunks_package_directory_name(self):
        return os.path.join(self.path_name, 'mus', 'chunks')

    @property
    def chunks_package_importable_name(self):
        return self.dot_join([self.importable_name, 'mus', 'chunks'])

    @property
    def chunks_package_initializer_file_name(self):
        return os.path.join(self.chunks_package_directory_name, '__init__.py')

    @property
    def composer(self):
        return self.get_tag('composer')

    @property
    def dist_pdf_directory_name(self):
        return os.path.join(self.dist_proxy.path_name, 'pdf')

    @property
    def dist_proxy(self):
        return self._dist_proxy

    @property
    def etc_proxy(self):
        return self._etc_proxy

    @property
    def exg_proxy(self):
        return self._exg_proxy

    @property
    def has_correct_directory_structure(self):
        return all([os.path.exists(name) for name in self.top_level_directory_names])

    @property
    def has_correct_initializers(self):
        return all([os.path.exists(initializer) for initializer in self.score_initializer_file_names])

    @property
    def has_correct_package_structure(self):
        return self.has_correct_directory_structure and self.has_correct_initializers

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
    def materials_package_directory_name(self):
        return os.path.join(self.path_name, 'mus', 'materials')

    @property
    def materials_package_importable_name(self):
        return self.dot_join([self.importable_name, 'mus', 'materials'])

    @property
    def materials_package_initializer_file_name(self):
        return os.path.join(self.materials_package_directory_name, '__init__.py')

    @property
    def mus_proxy(self):
        return self._mus_proxy

    @property
    def music_specifier_module_wrangler(self):
        return self._music_specifier_module_wrangler

    @property
    def score_initializer_file_names(self):
        return (
            self.initializer_file_name,
            self.mus_proxy.initializer_file_name,
            )

    @property
    def score_package_wranglers(self):
        return (
            self.chunk_wrangler,
            self.material_package_wrangler,
            )

    @property
    def tempo_inventory(self):
        from abjad.tools import contexttools
        for material_package_proxy in self.material_package_wrangler.list_asset_proxies(head=self.short_name):
            if material_package_proxy.get_tag('material_package_maker_class_name') == \
                'TempoMarkInventoryMaterialPackageMaker':
                return material_package_proxy.output_material

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
    def top_level_directory_names(self):
        return tuple([x.path_name for x in self.top_level_directory_proxies])

    @property
    def top_level_directory_proxies(self):
        return (
            self.dist_proxy,
            self.etc_proxy,
            self.exg_proxy,
            self.mus_proxy,
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

    @property
    def setup_value_menu_tokens(self):
        result = []
        if self.title:
            result.append(('title', 'title: {!r}'.format(self.title)))
        else:
            result.append(('title', 'title:'))
        if self.year_of_completion:
            result.append(('year', 'year: {!r}'.format(self.year_of_completion)))
        else:
            result.append(('year', 'year:'))
        if self.get_tag('instrumentation'):
            result.append(('performers', 'performers: {}'.format(
                self.get_tag('instrumentation').performer_name_string)))
        else:
            result.append(('performers', 'performers:'))
        if self.forces_tagline:
            result.append(('tagline', 'tagline: {!r}'.format(self.forces_tagline)))
        else:
            result.append(('tagline', 'tagline:'))
        return result

    @apply
    def year_of_completion():
        def fget(self):
            return self.get_tag('year_of_completion')
        def fset(self, year_of_completion):
            return self.add_tag('year_of_completion', year_of_completion)
        return property(**locals())

    ### PUBLIC METHODS ###

    def edit_forces_tagline_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('Forces tagline')
        result = getter.run()
        if self.backtrack():
            return
        self.add_tag('forces_tagline', result)

    def edit_instrumentation_specifier_interactively(self):
        import scftools
        target = self.get_tag('instrumentation')
        editor = scftools.editors.InstrumentationEditor(session=self.session, target=target)
        editor.run() # maybe check for backtracking after this?
        self.add_tag('instrumentation', editor.target)

    def edit_title_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('new title')
        result = getter.run()
        if self.backtrack():
            return
        self.add_tag('title', result)

    def edit_year_of_completion_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_integer_in_range('year of completion', start=1, allow_none=True)
        result = getter.run()
        if self.backtrack():
            return
        self.add_tag('year_of_completion', result)

    def fix(self, is_interactive=True):
        result = True
        if self.short_name == 'recursif':
            return True
        for path_name in self.top_level_directory_names:
            if not os.path.exists(path_name):
                result = False
                prompt = 'create {!r}? '.format(path_name)
                if not is_interactive or self.confirm(prompt):
                    os.mkdir(path_name)
        if not os.path.exists(self.initializer_file_name):
            result = False
            prompt = 'create {}? '.format(self.initializer_file_name)
            if not is_interactive or self.confirm(prompt):
                initializer = file(self.initializer_file_name, 'w')
                initializer.write('')
                initializer.close()
        if not os.path.exists(self.mus_proxy.initializer_file_name):
            result = False
            prompt = 'create {}? '.format(self.mus_proxy.initializer_file_name)
            if not is_interactive or self.confirm(prompt):
                initializer = file(self.mus_proxy.initializer_file_name, 'w')
                initializer.write('')
                initializer.close()
        lines = []
        initializer = file(self.mus_proxy.initializer_file_name, 'r')
        found_materials_import = False
        for line in initializer.readlines():
            lines.append(line)
            if line.startswith('import materials'):
                found_materials_import = True
        initializer.close()
        if not found_materials_import:
            result = False
            lines.insert(0, 'import materials\n')
            initializer = file(self.mus_proxy.initializer_file_name, 'w')
            initializer.write(''.join(lines))
            initializer.close()
        if not os.path.exists(self.tags_file_name):
            result = False
            prompt = 'create {}? '.format(self.tags_file_name)
            if not is_interactive or self.confirm(prompt):
                tags_file = file(self.tags_file_name, 'w')
                tags_file.write('# -*- encoding: utf-8 -*-\n')
                tags_file.write('from abjad import *\n')
                tags_file.write('from collections import OrderedDict\n')
                tags_file.write('\n')
                tags_file.write('\n')
                tags_file.write('tags = OrderedDict([])\n')
                tags_file.close()
        if not os.path.exists(self.materials_package_directory_name):
            result = False
            prompt = 'create {}'.format(self.materials_package_directory_name)
            if not is_interactive or self.confirm(prompt):
                os.mkdir(self.materials_package_directory_name)
        if not os.path.exists(self.materials_package_initializer_file_name):
            result = False
            file(self.materials_package_initializer_file_name, 'w').write('')
        if not os.path.exists(self.chunks_package_directory_name):
            result = False
            prompt = 'create {}'.format(self.chunks_package_directory_name)
            if not is_interactive or self.confirm(prompt):
                os.mkdir(self.chunks_package_directory_name)
        if not os.path.exists(self.chunks_package_initializer_file_name):
            result = False
            file(self.chunks_package_initializer_file_name, 'w').write('')
        self.proceed('packaged structure fixed.', is_interactive=is_interactive)
        return result

    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'h':
            self.chunk_wrangler.run(head=self.short_name)
        elif  result == 'm':
            self.material_package_wrangler.run(head=self.short_name)
        elif result == 'f':
            self.music_specifier_module_wrangler.run()
        elif result == 's':
            self.manage_setup(cache=True)
        elif result == 'fix':
            self.fix()
        elif result == 'ls':
            self.print_directory_contents()
        elif result == 'profile':
            self.profile()
        elif result == 'removescore':
            self.remove_interactively()
        elif result == 'svn':
            self.manage_svn()
        elif result == 'tags':
            self.manage_tags()
        else:
            raise ValueError

    def handle_setup_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'title':
            self.edit_title_interactively()
        elif result == 'year':
            self.edit_year_of_completion_interactively()
        elif result == 'tagline':
            self.edit_forces_tagline_interactively()
        elif result == 'performers':
            self.edit_instrumentation_specifier_interactively()
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

    def make_asset_structure(self):
        self.fix_score_package_directory_structure(is_interactive=False)

    def make_main_menu(self):
        menu, section = self.make_menu(where=self.where(), is_numbered=True)
        section = menu.make_section()
        section.append(('h', 'chunks'))
        section.append(('m', 'materials'))
        section.append(('f', 'specifiers'))
        section.append(('s', 'setup'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('fix', 'fix package structure'))
        hidden_section.append(('ls', 'list directory contents'))
        hidden_section.append(('profile', 'profile package structure'))
        hidden_section.append(('removescore', 'remove score package'))
        hidden_section.append(('svn', 'manage repository'))
        hidden_section.append(('tags', 'manage tags'))
        return menu

    def make_score_interactively(self):
        self.print_not_yet_implemented()

    def make_setup_menu(self):
        setup_menu, section = self.make_menu(where=self.where(),
            is_parenthetically_numbered=True, is_keyed=False)
        section.tokens = self.setup_value_menu_tokens
        section.return_value_attribute = 'key'
        return setup_menu

    def make_svn_menu(self):
        menu, section = self.make_menu(where=self.where(), is_keyed=False)
        section.return_value_attribute = 'key'
        section.append(('st', 'st'))
        section.append(('add', 'add'))
        section.append(('ci', 'ci'))
        return menu

    def manage_setup(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb('{} - setup'.format(self.annotated_title))
            setup_menu = self.make_setup_menu()
            result = setup_menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_setup_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    def manage_svn(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb('repository commands')
            menu = self.make_svn_menu()
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_svn_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    def profile(self, prompt=True):
        if not os.path.exists(self.path_name):
            raise OSError('directory {!r} does not exist.'.format(self.path_name))
        if self.short_name == 'recursif':
            return
        lines = []
        for subdirectory_name in self.top_level_directory_names:
            lines.append('{} {}'.format(subdirectory_name.ljust(80), os.path.exists(subdirectory_name)))
        for initializer in self.score_initializer_file_names:
            lines.append('{} {}'.format(initializer.ljust(80), os.path.exists(initializer)))
        lines.append('')
        self.display(lines)
        self.proceed(is_interactive=prompt)

    def remove_interactively(self):
        line = 'WARNING! Score package {!r} will be completely removed.'.format(self.importable_name)
        self.display([line, ''])
        getter = self.make_getter(where=self.where())
        getter.append_string("type 'clobberscore' to proceed")
        self.push_backtrack()
        should_clobber = getter.run()
        self.pop_backtrack()
        if self.backtrack():
            return
        if should_clobber == 'clobberscore':
            self.push_backtrack()
            self.remove()
            self.pop_backtrack()
            if self.backtrack():
                return
            self.session.is_backtracking_locally = True

    def summarize_chunks(self):
        chunks = self.chunk_wrangler.package_underscored_names
        lines = []
        if not chunks:
            lines.append('{}Chunks (none yet)'.format(self.make_tab(1)))
        else:
            lines.append('{}Chunks'.format(self.make_tab(1)))
        for chunk in chunks:
            lines.append('{}{}'.format(self.make_tab(2), chunk))
        lines.append('')
        self.display(lines)

    def summarize_materials(self):
        materials = self.material_package_wrangler.human_readable_names
        lines = []
        if not materials:
            lines.append('{}Materials (none yet)'.format(self.make_tab(1)))
        else:
            lines.append('{}Materials'.format(self.make_tab(1)))
        if materials:
            lines.append('')
        for i, material in enumerate(materials):
            lines.append('{}({}) {}'.format(self.make_tab(1), i + 1, material))
        self.display(lines)
