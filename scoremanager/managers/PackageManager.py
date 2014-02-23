# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import systemtools
from abjad.tools import stringtools
from scoremanager.managers.DirectoryManager import DirectoryManager


class PackageManager(DirectoryManager):

    ### INITIALIZER ###

    def __init__(self, package_path=None, session=None):
        if package_path is None or \
            os.path.sep not in package_path:
            filesystem_path = \
                self.configuration.package_path_to_filesystem_path(
                    package_path)
        else:
            filesystem_path = package_path
        assert '.' not in filesystem_path, repr(filesystem_path)
        DirectoryManager.__init__(
            self,
            filesystem_path=filesystem_path,
            session=session,
            )
        package_path = \
            self.configuration.filesystem_path_to_package_path(
                filesystem_path)
        assert os.path.sep not in package_path, repr(package_path)
        self._package_path = package_path

    ### PRIVATE PROPERTIES ###

    @property
    def _initializer_file_manager(self):
        from scoremanager import managers
        return managers.FileManager(
            self._initializer_file_path,
            session=self._session,
            )

    @property
    def _initializer_file_path(self):
        if self._filesystem_path is not None:
            return os.path.join(self._filesystem_path, '__init__.py')

    @property
    def _metadata_module_path(self):
        file_path = os.path.join(self._filesystem_path, '__metadata__.py')
        return file_path

    @property
    def _package_root_name(self):
        return self._package_path.split('.')[0]

    @property
    def _space_delimited_lowercase_name(self):
        if self._filesystem_path:
            base_name = os.path.basename(self._filesystem_path)
            result = base_name.replace('_', ' ')
            return result

    @property
    def _views_module_path(self):
        file_path = os.path.join(self._filesystem_path, '__views__.py')
        return file_path

    ### PRIVATE METHODS ###

    def _add_metadatum(self, metadatum_name, metadatum_value):
        assert stringtools.is_snake_case_string(metadatum_name)
        metadata = self._get_metadata()
        metadata[metadatum_name] = metadatum_value
        self.rewrite_metadata_module(metadata)

    def _get_metadata(self):
        metadata = None
        if os.path.isfile(self._metadata_module_path):
            file_pointer = open(self._metadata_module_path, 'r')
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
        main_menu = self._session.io_manager.make_menu(where=where)
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
            self._session.io_manager.proceed(message)
        if was_removed:
            self.rewrite_metadata_module(metadata)
            message = 'metadatum removed: {!r}.'
            message = message.format(metadatum_name)
            self._session.io_manager.proceed(message)

    def _run_first_time(self, **kwargs):
        self._run(**kwargs)

    def _write_metadata(self, metadata):
        lines = []
        lines.append('# -*- encoding: utf-8 -*-\n')
        lines.append('import collections\n')
        lines.append('\n\n')
        metadata_lines = self._make_metadata_lines(metadata) 
        lines.extend(metadata_lines)
        lines = ''.join(lines)
        file_pointer = file(self._metadata_module_path, 'w')
        file_pointer.write(lines)
        file_pointer.close()

    ### PUBLIC METHODS ###

    def add_metadatum(self):
        r'''Adds metadatum to metadata module.

        Returns none.
        '''
        getter = self._session.io_manager.make_getter(where=self._where)
        getter.append_string('metadatum name')
        getter.append_expr('metadatum value')
        result = getter._run()
        if self._session._backtrack():
            return
        if result:
            metadatum_name, metadatum_value = result
            self._add_metadatum(metadatum_name, metadatum_value)

    def get_metadatum(self):
        r'''Gets metadatum from metadata module.

        Returns none.
        '''
        getter = self._session.io_manager.make_getter(where=self._where)
        getter.append_string('metadatum name')
        result = getter._run()
        if self._session._backtrack():
            return
        metadatum = self._get_metadatum(result)
        message = '{!r}'.format(metadatum)
        self._session.io_manager.proceed(message=message)

    def remove_initializer_module(self, prompt=True):
        r'''Removes initializer module.

        Returns none.
        '''
        if os.path.isfile(self._initializer_file_path):
            os.remove(self._initializer_file_path)
            line = 'initializer deleted.'
            self._session.io_manager.proceed(
                line, 
                prompt=prompt,
                )

    def remove_metadata_module(self, prompt=True):
        r'''Removes metadata module.

        Returns none.
        '''
        if os.path.isfile(self._metadata_module_path):
            if prompt:
                message = 'remove metadata module?'
                if not self._session.io_manager.confirm(message):
                    return
            os.remove(self._metadata_module_path)
            line = 'metadata module removed.'
            self._session.io_manager.proceed(
                line, 
                prompt=prompt,
                )

    def remove_metadatum(self):
        r'''Removes metadatum from meatdata module.

        Returns none.
        '''
        getter = self._session.io_manager.make_getter(where=self._where)
        getter.append_string('metadatum name')
        result = getter._run()
        if self._session._backtrack():
            return
        if result:
            metadatum_name = result
            self._remove_metadatum(metadatum_name)

    def remove_package(self):
        r'''Removes package.

        Returns none.
        '''
        self._remove()
        self._session._is_backtracking_locally = True

    def remove_views_module(self, prompt=True):
        r'''Removes views module.

        Returns none.
        '''
        if os.path.isfile(self._views_module_path):
            if prompt:
                message = 'remove views module?'
                if not self._session.io_manager.confirm(message):
                    return
            os.remove(self._views_module_path)
            line = 'views module removed.'
            self._session.io_manager.proceed(
                line, 
                prompt=prompt,
                )

    def rename_package(self):
        r'''Renames package.

        Returns none.
        '''
        base_name = os.path.basename(self._filesystem_path)
        line = 'current name: {}'.format(base_name)
        self._session.io_manager.display(line)
        getter = self._session.io_manager.make_getter(where=self._where)
        getter.append_snake_case_package_name('new name')
        new_package_name = getter._run()
        if self._session._backtrack():
            return
        lines = []
        line = 'current name: {}'.format(base_name)
        lines.append(line)
        line = 'new name:     {}'.format(new_package_name)
        lines.append(line)
        lines.append('')
        self._session.io_manager.display(lines)
        if not self._session.io_manager.confirm():
            return
        new_directory_path = self._filesystem_path.replace(
            base_name,
            new_package_name,
            )
        if self._is_versioned():
            # rename package directory
            command = 'svn mv {} {}'
            command = command.format(self._filesystem_path, new_directory_path)
            self._session.io_manager.spawn_subprocess(command)
            # commit
            commit_message = 'renamed {} to {}.'
            commit_message = commit_message.format(
                base_name,
                new_package_name,
                )
            commit_message = commit_message.replace('_', ' ')
            parent_directory_path = os.path.dirname(self._filesystem_path)
            command = 'svn commit -m {!r} {}'
            command = command.format(
                commit_message,
                parent_directory_path,
                )
            self._session.io_manager.spawn_subprocess(command)
        else:
            command = 'mv {} {}'
            command = command.format(self._filesystem_path, new_directory_path)
            self._session.io_manager.spawn_subprocess(command)
        # update path name to reflect change
        self._path = new_directory_path
        self._session._is_backtracking_locally = True

    def rewrite_metadata_module(
        self, 
        metadata=None, 
        prompt=True,
        ):
        r'''Rewrites metadata module.

        Returns none.
        '''
        if metadata is None:
            metadata = self._get_metadata()
        self._write_metadata(metadata)

    def set_package_path(self):
        r'''Sets package path.

        Returns none.
        '''
        getter = self._session.io_manager.make_getter(where=self._where)
        getter.append_snake_case_package_name('package name')
        result = getter._run()
        if self._session._backtrack():
            return
        self._package_path = result

    def view_initializer_module(self):
        r'''Views initializer module.

        Returns none.
        '''
        self.initializer_file_manager.view()

    def view_metadata_module(self):
        r'''Views metadata module.

        Returns none.
        '''
        file_path = self._metadata_module_path
        if os.path.isfile(file_path):
            command = 'vim -R {}'.format(file_path)
            self._session.io_manager.spawn_subprocess(command)

    def write_boilerplate_initializer_module(self):
        r'''Writes boilerplate initializer module.

        Returns none.
        '''
        self.initializer_file_manager.write_boilerplate()

    def write_stub_initializer_module(self):
        r'''Wrties stub initializer module.

        Returns none.
        '''
        self.initializer_file_manager._write_stub()
        line = 'stub initializer written.'
        self._session.io_manager.display([line, ''])
        self._session.io_manager.proceed()

    ### UI MANIFEST ###

    _user_input_to_action = DirectoryManager._user_input_to_action.copy()
    _user_input_to_action.update({
        'inbp': write_boilerplate_initializer_module,
        'inrm': remove_initializer_module,
        'ins': write_stub_initializer_module,
        'inv': view_initializer_module,
        'mda': add_metadatum,
        'mdg': get_metadatum,
        'mdrm': remove_metadatum,
        'mdmv': view_metadata_module,
        'mdmrm': remove_metadata_module,
        'mdmrw': rewrite_metadata_module,
        'ren': rename_package,
        'rm': remove_package,
        })
