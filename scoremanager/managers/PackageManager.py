# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import systemtools
from abjad.tools import stringtools
from scoremanager.managers.DirectoryManager import DirectoryManager


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

    def _add_metadatum(self, metadatum_name, metadatum_value):
        assert stringtools.is_snake_case_string(metadatum_name)
        metadata = self._get_metadata()
        metadata[metadatum_name] = metadatum_value
        self.interactively_rewrite_metadata_module(metadata)

    def _get_metadata(self):
        metadata = None
        if os.path.isfile(self.metadata_module_path):
            file_pointer = open(self.metadata_module_path, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            exec(file_contents_string)
            metadata = locals().get('metadata')
        metadata = metadata or collections.OrderedDict()
        return metadata

    def _get_metadatum(self, metadatum_name):
        metadata = self._get_metadata()
        metadatum = metadata.get(metadatum_name, None)
        return metadatum

    def _make_main_menu(self, where=None):
        where = where or self._where
        main_menu = self.session.io_manager.make_menu(where=where)
        hidden_section = main_menu.make_command_section(is_secondary=True)
        return main_menu, hidden_section

    @staticmethod
    def _make_metadata_lines(metadata):
        if metadata:
            lines = []
            for key, value in sorted(metadata.iteritems()):
                key = repr(key)
                if hasattr(value, '_get_multiline_repr'):
                    repr_lines = \
                        value._get_multiline_repr(include_tools_package=True)
                    value = '\n    '.join(repr_lines)
                    lines.append('({}, {})'.format(key, value))
                else:
                    if hasattr(value, '_storage_format_specification'):
                        string = format(value)
                    else:
                        string = repr(value)
                    lines.append('({}, {})'.format(key, string))
            lines = ',\n    '.join(lines)
            result = 'metadata = collections.OrderedDict([\n    {},\n    ])'
            result = result.format(lines)
        else:
            result = 'metadata = collections.OrderedDict([])'
        return result

    def _make_metadata_menu_entries(self):
        result = []
        metadata = self._get_metadata()
        for key in sorted(metadata):
            display_string = key.replace('_', ' ')
            result.append((display_string, None, metadata[key], key))
        return result

    def _remove_metadatum(self, metadatum_name):
        metadata = self._get_metadata()
        was_removed = False
        try:
            del(metadata[metadatum_name])
            was_removed = True
        except KeyError:
            message = 'metadatum not found: {!r}.'
            message = message.format(metadatum_name)
            self.session.io_manager.proceed(message)
        if was_removed:
            self.interactively_rewrite_metadata_module(metadata)
            message = 'metadatum removed: {!r}.'
            message = message.format(metadatum_name)
            self.session.io_manager.proceed(message)

    def _write_metadata(self, metadata):
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('import collections\n')
        lines.append('\n\n')
        metadata_lines = self._make_metadata_lines(metadata) 
        lines.extend(metadata_lines)
        lines = ''.join(lines)
        file_pointer = file(self.metadata_module_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()

    ### PUBLIC PROPERTIES ###

    @property
    def imported_package(self):
        return __import__(self.package_path, fromlist=['*'])

    @property
    def initializer_file_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self.initializer_file_path,
            session=self.session,
            )

    @property
    def initializer_file_path(self):
        if self.filesystem_path is not None:
            return os.path.join(self.filesystem_path, '__init__.py')

    @property
    def metadata_module_path(self):
        file_path = os.path.join(self.filesystem_path, '__metadata__.py')
        return file_path

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

    @property
    def views_module_path(self):
        file_path = os.path.join(self.filesystem_path, '__views__.py')
        return file_path
        
    ### PUBLIC METHODS ###

    def handle_metadata_menu_result(self, result):
        if result == 'add':
            self.interactively_add_metadatum()
        elif result == 'rm':
            self.interactively_remove_metadatum()
        elif result == 'get':
            self.interactively_get_metadatum()
        return False

    def has_metadatum(self, metadatum_name):
        metadata = self._get_metadata()
        return bool(metadatum_name in metadata)

    def interactively_add_metadatum(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('metadatum name')
        getter.append_expr('metadatum value')
        result = getter._run()
        if self.session._backtrack():
            return
        if result:
            metadatum_name, metadatum_value = result
            self._add_metadatum(metadatum_name, metadatum_value)

    def interactively_get_metadatum(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('metadatum name')
        result = getter._run()
        if self.session._backtrack():
            return
        metadatum = self._get_metadatum(result)
        message = '{!r}'.format(metadatum)
        self.session.io_manager.proceed(message=message)

    def interactively_remove_initializer_module(self, prompt=True):
        if os.path.isfile(self.initializer_file_path):
            os.remove(self.initializer_file_path)
            line = 'initializer deleted.'
            self.session.io_manager.proceed(
                line, 
                prompt=prompt,
                )

    def interactively_remove_views_module(self, prompt=True):
        if os.path.isfile(self.views_module_path):
            if prompt:
                message = 'remove views module?'
                if not self.session.io_manager.confirm(message):
                    return
            os.remove(self.views_module_path)
            line = 'views module removed.'
            self.session.io_manager.proceed(
                line, 
                prompt=prompt,
                )

    def interactively_remove_metadata_module(self, prompt=True):
        if os.path.isfile(self.metadata_module_path):
            if prompt:
                message = 'remove metadata module?'
                if not self.session.io_manager.confirm(message):
                    return
            os.remove(self.metadata_module_path)
            line = 'metadata module removed.'
            self.session.io_manager.proceed(
                line, 
                prompt=prompt,
                )

    def interactively_remove_metadatum(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('metadatum name')
        result = getter._run()
        if self.session._backtrack():
            return
        if result:
            metadatum_name = result
            self._remove_metadatum(metadatum_name)

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
        if self.session._backtrack():
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
            self.session.io_manager.spawn_subprocess(command)
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
            self.session.io_manager.spawn_subprocess(command)
        else:
            command = 'mv {} {}'
            command = command.format(self.filesystem_path, new_directory_path)
            self.session.io_manager.spawn_subprocess(command)
        # update path name to reflect change
        self._path = new_directory_path
        self.session.is_backtracking_locally = True

    def interactively_set_package_path(self):
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_snake_case_package_name('package name')
        result = getter._run()
        if self.session._backtrack():
            return
        self.package_path = result

    def interactively_view_initializer_module(self):
        self.initializer_file_manager.interactively_view()

    def interactively_view_metadata_module(self):
        file_path = self.metadata_module_path
        if os.path.isfile(file_path):
            command = 'vim -R {}'.format(file_path)
            self.session.io_manager.spawn_subprocess(command)

    def interactively_write_boilerplate_initializer_module(self):
        self.initializer_file_manager.interactively_write_boilerplate()

    def interactively_rewrite_metadata_module(
        self, 
        metadata=None, 
        prompt=True,
        ):
        if metadata is None:
            metadata = self._get_metadata()
        self._write_metadata(metadata)

    def interactively_write_stub_initializer_module(self):
        self.initializer_file_manager._write_stub()
        line = 'stub initializer written.'
        self.session.io_manager.display([line, ''])
        self.session.io_manager.proceed()

    def remove_package(self):
        r'''Removes package.

        Returns none.
        '''
        self._remove()
        self.session.is_backtracking_locally = True

    def run_first_time(self, **kwargs):
        self._run(**kwargs)

    ### UI MANIFEST ###

    user_input_to_action = DirectoryManager.user_input_to_action.copy()
    user_input_to_action.update({
        'inbp': interactively_write_boilerplate_initializer_module,
        'inrm': interactively_remove_initializer_module,
        'ins': interactively_write_stub_initializer_module,
        'inv': interactively_view_initializer_module,
        'mda': interactively_add_metadatum,
        'mdg': interactively_get_metadatum,
        'mdrm': interactively_remove_metadatum,
        'mdmv': interactively_view_metadata_module,
        'mdmrm': interactively_remove_metadata_module,
        'mdmrw': interactively_rewrite_metadata_module,
        'ren': interactively_rename_package,
        'rm': remove_package,
        })
