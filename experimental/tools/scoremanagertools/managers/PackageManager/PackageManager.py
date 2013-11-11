# -*- encoding: utf-8 -*-
import os
from abjad.tools import systemtools
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.managers.DirectoryManager \
    import DirectoryManager


class PackageManager(DirectoryManager):

    ### INITIALIZER ###

    def __init__(self, packagesystem_path=None, session=None):
        if packagesystem_path is None or \
            os.path.sep not in packagesystem_path:
            filesystem_path = \
                self.configuration.packagesystem_path_to_filesystem_path(
                    packagesystem_path)
        else:
            filesystem_path = packagesystem_path
        assert '.' not in filesystem_path, repr(filesystem_path)
        DirectoryManager.__init__(self,
            filesystem_path=filesystem_path,
            session=session,
            )
        packagesystem_path = \
            self.configuration.filesystem_path_to_packagesystem_path(
                filesystem_path)
        assert os.path.sep not in packagesystem_path, repr(packagesystem_path)
        self._package_path = packagesystem_path

    ### PRIVATE PROPERTIES ###

    @property
    def _space_delimited_lowercase_name(self):
        if self.filesystem_path:
            base_name = os.path.basename(self.filesystem_path)
            result = base_name.replace('_', ' ')
            return result

    ### PRIVATE METHODS ###

    def _make_tags_menu_entries(self):
        result = []
        tags = self._get_metadatas()
        for key in sorted(tags):
            display_string = key.replace('_', ' ')
            result.append((display_string, None, tags[key], key))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def has_initializer(self):
        if self.initializer_file_name is not None:
            return os.path.isfile(self.initializer_file_name)

    @property
    def has_metadata_module(self):
        return os.path.isfile(self.metadata_module_name)

    @property
    def imported_package(self):
        return __import__(self.package_path, fromlist=['*'])

    @property
    def initializer_file_name(self):
        if self.filesystem_path is not None:
            return os.path.join(self.filesystem_path, '__init__.py')

    @property
    def initializer_file_manager(self):
        from experimental.tools import scoremanagertools
        return scoremanagertools.managers.FileManager(
            self.initializer_file_name,
            session=self.session,
            )

    @property
    def metadata_module_name(self):
        file_path = os.path.join(self.filesystem_path, '__metadata__.py')
        return file_path

    @property
    def metadata_module_manager(self):
        from experimental.tools import scoremanagertools
        if not self.has_metadata_module:
            metadata_module = open(self.metadata_module_name, 'w')
            metadata_module.write('')
            metadata_module.close()
        return scoremanagertools.managers.MetadataModuleManager(
            self.metadata_module_name, session=self.session)

    @property
    def package_path(self):
        return self._package_path

    @property
    def package_root_name(self):
        return self.package_path.split('.')[0]

    @property
    def public_names(self):
        result = []
        imported_package_vars = vars(self.imported_package)
        for key in sorted(imported_package_vars.keys()):
            if not key.startswith('_'):
                result.append(imported_package_vars[key])
        return result

    ### PUBLIC METHODS ###

    def _add_metadata(self, tag_name, tag_value):
        assert stringtools.is_snake_case_string(tag_name)
        tags = self._get_metadatas()
        tags[tag_name] = tag_value
        self.metadata_module_manager.write_metadata_to_disk(tags)

    def _get_metadata(self, tag_name):
        tags = self._get_metadatas()
        tag = tags.get(tag_name, None)
        return tag

    def _get_metadatas(self):
        from collections import OrderedDict
        self.metadata_module_manager._make_empty_asset()
        file_pointer = open(self.metadata_module_name, 'r')
        file_contents_string = file_pointer.read()
        file_pointer.close()
        exec(file_contents_string)
        tags = locals().get('tags') or OrderedDict([])
        return tags

    def handle_tags_menu_result(self, result):
        if result == 'add':
            self.interactively_add_metadata()
        elif result == 'rm':
            self.interactively_remove_metadata()
        elif result == 'get':
            self.interactively_get_metadata()
        return False

    def has_tag(self, tag_name):
        tags = self._get_metadatas()
        return bool(tag_name in tags)

    def interactively_add_metadata(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('tag name')
        getter.append_expr('tag value')
        result = getter._run()
        if self.session.backtrack():
            return
        if result:
            tag_name, tag_value = result
            self._add_metadata(tag_name, tag_value)

    def interactively_get_metadata(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('tag name')
        result = getter._run()
        if self.session.backtrack():
            return
        tag = self._get_metadata(result)
        line = '{!r}'.format(tag)
        self.session.io_manager.proceed(line)

    def interactively_remove_metadata(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('tag name')
        result = getter._run()
        if self.session.backtrack():
            return
        if result:
            tag_name = result
            self._remove_metadata(tag_name)

    def interactively_rename_package(self):
        r'''Interactively renames package.

        Returns none.
        '''
        base_name = os.path.basename(self.filesystem_path)
        line = 'current name: {}'.format(base_name)
        self.session.io_manager.display(line)
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_snake_case_package_name('new name')
        new_package_name = getter._run()
        if self.session.backtrack():
            return
        lines = []
        line = 'current name: {}'.format(base_name)
        lines.append(line)
        line = 'new name:     {}'.format(new_package_name)
        lines.append(line)
        lines.append('')
        self.session.io_manager.display(lines)
        if not self.session.io_manager.confirm():
            return
        new_directory_path = self.filesystem_path.replace(
            base_name,
            new_package_name,
            )
        if self._is_versioned():
            # rename package directory
            command = 'svn mv {} {}'
            command = command.format(self.filesystem_path, new_directory_path)
            systemtools.IOManager.spawn_subprocess(command)
            # commit
            commit_message = 'renamed {} to {}.'
            commit_message = commit_message.format(
                base_name,
                new_package_name,
                )
            commit_message = commit_message.replace('_', ' ')
            parent_directory_path = os.path.dirname(self.filesystem_path)
            command = 'svn commit -m {!r} {}'
            command = command.format(
                commit_message,
                parent_directory_path,
                )
            systemtools.IOManager.spawn_subprocess(command)
        else:
            command = 'mv {} {}'
            command = command.format(self.filesystem_path, new_directory_path)
            systemtools.IOManager.spawn_subprocess(command)
        # update path name to reflect change
        self._path = new_directory_path
        self.session.is_backtracking_locally = True

    def interactively_restore_initializer(self):
        self.initializer_file_manager._write_stub_to_disk()
        self.session.io_manager.proceed(is_interactive=True)

    def interactively_set_package_path(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_snake_case_package_name('package name')
        result = getter._run()
        if self.session.backtrack():
            return
        self.package_path = result

    def interactively_view_initializer(self):
        self.initializer_file_manager.interactively_view()

    def interactively_view_metadata_module(self):
        #self.metadata_module_manager.interactively_view()
        self.metadata_module_manager.interactively_edit()

    def interactively_write_initializer_boilerplate(self):
        self.initializer_file_manager.interactively_write_boilerplate()

    def make_tags_menu(self):
        tags_menu = self.session.io_manager.make_menu(where=self._where)
        attribute_section = tags_menu.make_attribute_section()
        menu_entries = self._make_tags_menu_entries()
        attribute_section.menu_entries = menu_entries
        command_section = tags_menu.make_command_section()
        command_section.append(('add tag', 'add'))
        command_section.append(('delete tag', 'rm'))
        command_section.append(('get tag', 'get'))
        return tags_menu

    def manage_metadata(self, clear=True, cache=False):
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb('tags')
            menu = self.make_tags_menu()
            result = menu._run(clear=clear)
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
            self.session.io_manager.proceed(
                line, is_interactive=is_interactive)

    def remove_package(self):
        r'''Removes package.

        Returns none.
        '''
        self._remove()
        self.session.is_backtracking_locally = True

    def _remove_metadata(self, tag_name):
        tags = self._get_metadatas()
        del(tags[tag_name])
        self.metadata_module_manager.write_metadata_to_disk(tags)

    def run_first_time(self, **kwargs):
        self._run(**kwargs)

    def write_initializer_stub_file_to_disk(self):
        self.initializer_file_manager.write_stub_file_to_disk(prompt=True)

    ### UI MANIFEST ###

    user_input_to_action = DirectoryManager.user_input_to_action.copy()
    user_input_to_action.update({
        'incanned': interactively_write_initializer_boilerplate,
        'inr': interactively_restore_initializer,
        'instub': write_initializer_stub_file_to_disk,
        'inv': interactively_view_initializer,
        'metadata': interactively_view_metadata_module,
        'ren': interactively_rename_package,
        'rm': remove_package,
        'tags': manage_metadata,
        })
