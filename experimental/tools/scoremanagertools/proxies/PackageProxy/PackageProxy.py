import os
from experimental.tools.scoremanagertools.proxies.DirectoryProxy import DirectoryProxy


class PackageProxy(DirectoryProxy):

    ### INITIALIZER ###

    def __init__(self, packagesystem_path=None, session=None):
        assert packagesystem_path is None or os.path.sep not in packagesystem_path, repr(packagesystem_path)
        filesystem_path = self.configuration.packagesystem_path_to_filesystem_path(
            packagesystem_path)
        DirectoryProxy.__init__(self, filesystem_path=filesystem_path, session=session)
        packagesystem_path = self.configuration.filesystem_path_to_packagesystem_path(
            filesystem_path)
        self._package_path = packagesystem_path

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _space_delimited_lowercase_name(self):
        return self.filesystem_basename.replace('_', ' ')

    ### PRIVATE METHODS ###

    def _run(self, cache=False, clear=True, user_input=None):
        self._io.assign_user_input(user_input=user_input)
        self._session.cache_breadcrumbs(cache=cache)
        while True:
            self._session.push_breadcrumb(self._breadcrumb)
            menu = self._make_main_menu()
            result = menu._run(clear=clear)
            if self._session.backtrack(source=self._backtracking_source):
                break
            elif not result:
                self._session.pop_breadcrumb()
                continue
            self._handle_main_menu_result(result)
            if self._session.backtrack(source=self._backtracking_source):
                break
            self._session.pop_breadcrumb()
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def formatted_tags(self):
        formatted_tags = []
        tags = self.get_tags()
        for key in sorted(tags):
            formatted_tag = '{!r}: {!r}'.format(key, tags[key])
            formatted_tags.append(formatted_tag)
        return formatted_tags

    @property
    def has_initializer(self):
        if self.initializer_file_name is not None:
            return os.path.isfile(self.initializer_file_name)

    @property
    def has_parent_initializer(self):
        if self.parent_initializer_file_name is not None:
            return os.path.isfile(self.parent_initializer_file_name)

    @property
    def has_tags_file(self):
        return os.path.isfile(self.tags_file_name)

    @property
    def imported_package(self):
        return __import__(self.package_path, fromlist=['*'])

    @property
    def initializer_file_name(self):
        if self.filesystem_path is not None:
            return os.path.join(self.filesystem_path, '__init__.py')

    # TODO: write test
    @property
    def initializer_file_proxy(self):
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.InitializerModuleProxy(
            self.initializer_file_name, session=self._session)

    @property
    def package_path(self):
        return self._package_path

    @property
    def package_root_name(self):
        return self.package_path.split('.')[0]

    @property
    def parent_directory_packagesystem_path(self):
        if self.package_path is not None:
            result = '.'.join(self.package_path.split('.')[:-1])
            if result:
                return result

    @property
    def parent_initializer_file_name(self):
        if self.parent_directory_packagesystem_path:
            return os.path.join(self.parent_directory_filesystem_path, '__init__.py')

    # TODO: write test
    @property
    def parent_initializer_file_proxy(self):
        from experimental.tools import scoremanagertools
        if self.has_parent_initializer:
            return scoremanagertools.proxies.InitializerModuleProxy(
                self.parent_initializer_file_name, session=self._session)

    @property
    def public_names(self):
        result = []
        imported_package_vars = vars(self.imported_package)
        for key in sorted(imported_package_vars.keys()):
            if not key.startswith('_'):
                result.append(imported_package_vars[key])
        return result

    @property
    def tags_file_name(self):
        return os.path.join(self.filesystem_path, 'tags.py')

    @property
    def tags_file_proxy(self):
        from experimental.tools import scoremanagertools
        if not self.has_tags_file:
            tags_file = open(self.tags_file_name, 'w')
            tags_file.write('')
            tags_file.close()
        return scoremanagertools.proxies.TagsModuleProxy(
            self.tags_file_name, session=self._session)

    ### PUBLIC METHODS ###

    def add_tag(self, tag_name, tag_value):
        tags = self.get_tags()
        tags[tag_name] = tag_value
        self.tags_file_proxy.write_tags_to_disk(tags)

    def get_tag(self, tag_name):
        tags = self.get_tags()
        tag = tags.get(tag_name, None)
        return tag

    def get_tags(self):
        from collections import OrderedDict
        self.tags_file_proxy.make_empty_asset()
        file_pointer = open(self.tags_file_name, 'r')
        file_contents_string = file_pointer.read()
        file_pointer.close()
        exec(file_contents_string)
        tags = locals().get('tags') or OrderedDict([])
        return tags

    def handle_tags_menu_result(self, result):
        if result == 'add':
            self.interactively_add_tag()
        elif result == 'rm':
            self.interactively_remove_tag()
        elif result == 'get':
            self.interactively_get_tag()
        return False

    def has_tag(self, tag_name):
        tags = self.get_tags()
        return bool(tag_name in tags)

    def interactively_add_tag(self):
        getter = self._io.make_getter(where=self._where)
        getter.append_string('tag name')
        getter.append_expr('tag value')
        result = getter._run()
        if self._session.backtrack():
            return
        if result:
            tag_name, tag_value = result
            self.add_tag(tag_name, tag_value)

    def interactively_get_tag(self):
        getter = self._io.make_getter(where=self._where)
        getter.append_string('tag name')
        result = getter._run()
        if self._session.backtrack():
            return
        tag = self.get_tag(result)
        line = '{!r}'.format(tag)
        self._io.proceed(line)

    def interactively_remove_tag(self):
        getter = self._io.make_getter(where=self._where)
        getter.append_string('tag name')
        result = getter._run()
        if self._session.backtrack():
            return
        if result:
            tag_name = result
            self.remove_tag(tag_name)

    def interactively_restore_initializer(self):
        self.initializer_file_proxy.interactively_restore(prompt=True)

    def interactively_set_package_path(self):
        getter = self._io.make_getter(where=self._where)
        getter.append_underscore_delimited_lowercase_package_name('package name')
        result = getter._run()
        if self._session.backtrack():
            return
        self.package_path = result

    def interactively_view_initializer(self):
        self.initializer_file_proxy.view()

    def interactively_write_initializer_boilerplate(self):
        self.initializer_file_proxy.interactively_write_boilerplate()

    def make_tags_menu(self):
        menu_tokens = self.formatted_tags
        menu, menu_section = self._io.make_menu(where=self._where, is_keyed=False, menu_tokens=menu_tokens)
        menu_tokens = [
            ('add', 'add tag'),
            ('rm', 'delete tag'),
            ('get', 'get tag'),
            ]
        menu_section = menu.make_section(
            menu_tokens=menu_tokens,
            return_value_attribute='key',
            is_keyed=True,
            )
        return menu

    def manage_tags(self, clear=True, cache=False):
        self._session.cache_breadcrumbs(cache=cache)
        while True:
            self._session.push_breadcrumb('tags')
            menu = self.make_tags_menu()
            result = menu._run(clear=clear)
            if self._session.backtrack():
                break
            self.handle_tags_menu_result(result)
            if self._session.backtrack():
                break
            self._session.pop_breadcrumb()
        self._session.pop_breadcrumb()
        self._session.restore_breadcrumbs(cache=cache)

    def remove_initializer(self, is_interactive=True):
        if self.has_initializer:
            os.remove(self.initializer_file_name)
            line = 'initializer deleted.'
            self._io.proceed(line, is_interactive=is_interactive)

    def remove_tag(self, tag_name):
        tags = self.get_tags()
        del(tags[tag_name])
        self.tags_file_proxy.write_tags_to_disk(tags)

    def run_first_time(self, **kwargs):
        self._run(**kwargs)

    def write_initializer_stub_file_to_disk(self):
        self.initializer_file_proxy.write_stub_file_to_disk(prompt=True)

    ### UI MANIFEST ###

    user_input_to_action = DirectoryProxy.user_input_to_action.copy()
    user_input_to_action.update({
        'incanned': interactively_write_initializer_boilerplate,
        'inr': interactively_restore_initializer,
        'instub': write_initializer_stub_file_to_disk,
        'inv': interactively_view_initializer,
        'tags': manage_tags,
        })
