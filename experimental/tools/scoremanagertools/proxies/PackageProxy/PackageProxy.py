import os
import sys
from abjad.tools import iotools
from experimental.tools import filesystemtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject import ScoreManagerObject
from experimental.tools.scoremanagertools.proxies.AssetProxy import AssetProxy
from experimental.tools.scoremanagertools.proxies.DirectoryProxy import DirectoryProxy
from experimental.tools.scoremanagertools.proxies.InitializerFileProxy import InitializerFileProxy
from experimental.tools.scoremanagertools.helpers import safe_import


#class PackageProxy(DirectoryProxy, AssetProxy):
class PackageProxy(DirectoryProxy, AssetProxy, ScoreManagerObject):

    ### INITIALIZER ###

    def __init__(self, package_path=None, session=None):
#        directory_path = filesystemtools.package_path_to_directory_path(package_path, self.configuration)
#        DirectoryProxy.__init__(self, directory_path=directory_path, session=session)
#        AssetProxy.__init__(self, asset_path=package_path, session=self.session)
        ScoreManagerObject.__init__(self, session=session)
        directory_path = filesystemtools.package_path_to_directory_path(package_path, self.configuration)
        DirectoryProxy.__init__(self, directory_path=directory_path, session=self.session)
        AssetProxy.__init__(self, asset_path=directory_path, session=self.session)
        self._package_path = package_path

    ### SPECIAL METHODS ###

    def __repr__(self):
        return AssetProxy.__repr__(self)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def directory_path(self):
        if self.package_path is not None:
            return filesystemtools.package_path_to_directory_path(self.package_path, self.configuration)

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
    def human_readable_name(self):
        return self.name.replace('_', ' ')

    @property
    def imported_package(self):
        return __import__(self.package_path, fromlist=['*'])

    @property
    def initializer_file_name(self):
        if self.directory_path is not None:
            return os.path.join(self.directory_path, '__init__.py')

    # TODO: write test
    @property
    def initializer_file_proxy(self):
        return InitializerFileProxy(self.initializer_file_name, session=self.session)

    @property
    def package_path(self):
        return self._package_path

    @property
    def package_root_name(self):
        return self.package_path.split('.')[0]

    @property
    def parent_initializer_file_name(self):
        if self.parent_package_path:
            parent_directory_path = filesystemtools.package_path_to_directory_path(
                self.parent_package_path, self.configuration)
            return os.path.join(parent_directory_path, '__init__.py')

    # TODO: write test
    @property
    def parent_initializer_file_proxy(self):
        if self.has_parent_initializer:
            return InitializerFileProxy(
                self.parent_initializer_file_name, session=self.session)

    @property
    def parent_package_path(self):
        if self.package_path is not None:
            result = '.'.join(self.package_path.split('.')[:-1])
            if result:
                return result

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
        return os.path.join(self.directory_path, 'tags.py')

    @property
    def tags_file_proxy(self):
        if not self.has_tags_file:
            tags_file = open(self.tags_file_name, 'w')
            tags_file.write('')
            tags_file.close()
        if True:
            return InitializerFileProxy(self.tags_file_name, session=self.session)

    ### PUBLIC METHODS ###

    def add_tag(self, tag_name, tag_value):
        tags = self.get_tags()
        tags[tag_name] = tag_value
        self.tags_file_proxy.write_tags_to_disk(tags)

    def add_tag_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('tag name')
        getter.append_expr('tag value')
        result = getter.run()
        if self.session.backtrack():
            return
        if result:
            tag_name, tag_value = result
            self.add_tag(tag_name, tag_value)

    def get_tag(self, tag_name):
        tags = self.get_tags()
        tag = tags.get(tag_name, None)
        return tag

    def get_tag_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('tag name')
        result = getter.run()
        if self.session.backtrack():
            return
        tag = self.get_tag(result)
        line = '{!r}'.format(tag)
        self.proceed(line)

    def get_tags(self):
        from collections import OrderedDict
        self.tags_file_proxy.conditionally_make_empty_asset()
        file_pointer = open(self.tags_file_name, 'r')
        file_contents_string = file_pointer.read()
        file_pointer.close()
        exec(file_contents_string)
        tags = locals().get('tags') or OrderedDict([])
        return tags

    def handle_tags_menu_result(self, result):
        if result == 'add':
            self.add_tag_interactively()
        elif result == 'rm':
            self.remove_tag_interactively()
        elif result == 'get':
            self.get_tag_interactively()
        return False

    def has_tag(self, tag_name):
        tags = self.get_tags()
        return bool(tag_name in tags)

    def make_tags_menu(self):
        menu, section = self.make_menu(where=self.where(), is_keyed=False)
        section.tokens = self.formatted_tags
        section = menu.make_section()
        section.append(('add', 'add tag'))
        section.append(('rm', 'delete tag'))
        section.append(('get', 'get tag'))
        return menu

    def manage_tags(self, clear=True, cache=False):
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb('tags')
            menu = self.make_tags_menu()
            result = menu.run(clear=clear)
            if self.session.backtrack():
                break
            self.handle_tags_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    def remove_initializer(self, is_interactive=True):
        if self.has_initializer:
            os.remove(self.initializer_file_name)
            line = 'initializer deleted.'
            self.proceed(line, is_interactive=is_interactive)

    def remove_tag(self, tag_name):
        tags = self.get_tags()
        del(tags[tag_name])
        self.tags_file_proxy.write_tags_to_disk(tags)

    def remove_tag_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('tag name')
        result = getter.run()
        if self.session.backtrack():
            return
        if result:
            tag_name = result
            self.remove_tag(tag_name)

    def set_package_path_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_underscore_delimited_lowercase_package_name('package name')
        result = getter.run()
        if self.session.backtrack():
            return
        self.package_path = result

    def unimport_package(self):
        self.remove_package_path_from_sys_modules(self.package_path)
