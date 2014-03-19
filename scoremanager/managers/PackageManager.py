# -*- encoding: utf-8 -*-
import collections
import os
import traceback
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.managers.DirectoryManager import DirectoryManager


class PackageManager(DirectoryManager):
    r'''Package manager.
    '''

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        if path is not None:
            assert os.path.sep in path
        DirectoryManager.__init__(
            self,
            path=path,
            session=session,
            )
        package_path = self._configuration.path_to_package_path(path)
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
        if self._path is not None:
            return os.path.join(self._path, '__init__.py')

    @property
    def _metadata_module_path(self):
        file_path = os.path.join(self._path, '__metadata__.py')
        return file_path

    @property
    def _package_root_name(self):
        return self._package_path.split('.')[0]

    @property
    def _space_delimited_lowercase_name(self):
        if self._path:
            base_name = os.path.basename(self._path)
            result = base_name.replace('_', ' ')
            return result

    @property
    def _user_input_to_action(self):
        superclass = super(PackageManager, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'inbp': self.write_initializer_boilerplate,
            'inrm': self.remove_initializer,
            'ins': self.write_initializer_stub,
            'inv': self.view_initializer,
            'mda': self.add_metadatum,
            'mdg': self.get_metadatum,
            'mdrm': self.remove_metadatum,
            'mmmv': self.view_metadata_module,
            'mdmrm': self.remove_metadata_module,
            'mdmrw': self.rewrite_metadata_module,
            'ren': self.rename,
            'rm': self.remove,
            })
        return result

    @property
    def _views_module_path(self):
        file_path = os.path.join(self._path, '__views__.py')
        return file_path

    ### PRIVATE METHODS ###

    def _add_metadatum(self, metadatum_name, metadatum_value):
        assert stringtools.is_snake_case_string(metadatum_name)
        metadata = self._get_metadata()
        metadata[metadatum_name] = metadatum_value
        self.rewrite_metadata_module(metadata, prompt=False)

    def _get_metadata(self):
        metadata = None
        if os.path.isfile(self._metadata_module_path):
            file_pointer = open(self._metadata_module_path, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            try:
                exec(file_contents_string)
            except:
                message = 'Can not interpret metadata module: {!r}.'
                message = message.format(self)
                print message
            metadata = locals().get('metadata')
        metadata = metadata or collections.OrderedDict()
        return metadata

    def _get_metadatum(self, metadatum_name):
        metadata = self._get_metadata()
        metadatum = metadata.get(metadatum_name, None)
        return metadatum

    def _make_main_menu(self, where=None):
        where = where or self._where
        menu = self._io_manager.make_menu(where=where)
        return menu

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
            self._io_manager.proceed(message)
        if was_removed:
            self.rewrite_metadata_module(metadata, prompt=False)
            message = 'metadatum removed: {!r}.'
            message = message.format(metadatum_name)
            self._io_manager.proceed(message)

    def _run_first_time(self, **kwargs):
        self._run(**kwargs)

    def _write_metadata(self, metadata):
        lines = []
        lines.append(self._unicode_directive + '\n')
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
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_snake_case_string('metadatum name', allow_empty=False)
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
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('metadatum name')
        result = getter._run()
        if self._session._backtrack():
            return
        metadatum = self._get_metadatum(result)
        message = '{!r}'.format(metadatum)
        self._io_manager.proceed(message=message)

    def remove_initializer(self, prompt=True):
        r'''Removes initializer module.

        Returns none.
        '''
        if os.path.isfile(self._initializer_file_path):
            os.remove(self._initializer_file_path)
            line = 'initializer deleted.'
            self._io_manager.proceed(
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
                if not self._io_manager.confirm(message):
                    return
            os.remove(self._metadata_module_path)
            line = 'metadata module removed.'
            self._io_manager.proceed(
                line, 
                prompt=prompt,
                )

    def remove_metadatum(self):
        r'''Removes metadatum from meatdata module.

        Returns none.
        '''
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('metadatum name')
        result = getter._run()
        if self._session._backtrack():
            return
        if result:
            metadatum_name = result
            self._remove_metadatum(metadatum_name)

    def remove_views_module(self, prompt=True):
        r'''Removes views module.

        Returns none.
        '''
        if os.path.isfile(self._views_module_path):
            if prompt:
                message = 'remove views module?'
                if not self._io_manager.confirm(message):
                    return
            os.remove(self._views_module_path)
            line = 'views module removed.'
            self._io_manager.proceed(
                line, 
                prompt=prompt,
                )

    def rename(self):
        r'''Renames package.

        Returns none.
        '''
        base_name = os.path.basename(self._path)
        line = 'current name: {}'.format(base_name)
        self._io_manager.display(line)
        getter = self._io_manager.make_getter(where=self._where)
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
        self._io_manager.display(lines)
        if not self._io_manager.confirm():
            return
        new_directory_path = self._path.replace(
            base_name,
            new_package_name,
            )
        if self._is_svn_versioned():
            # rename package directory
            command = 'svn mv {} {}'
            command = command.format(self._path, new_directory_path)
            self._io_manager.spawn_subprocess(command)
            # commit
            commit_message = 'renamed {} to {}.'
            commit_message = commit_message.format(
                base_name,
                new_package_name,
                )
            commit_message = commit_message.replace('_', ' ')
            parent_directory_path = os.path.dirname(self._path)
            command = 'svn commit -m {!r} {}'
            command = command.format(
                commit_message,
                parent_directory_path,
                )
            self._io_manager.spawn_subprocess(command)
        else:
            command = 'mv {} {}'
            command = command.format(self._path, new_directory_path)
            self._io_manager.spawn_subprocess(command)
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
        if prompt:
            message = 'rewrote metadata module.'
            self._io_manager.proceed(message)

    def view_initializer(self):
        r'''Views initializer module.

        Returns none.
        '''
        from scoremanager import managers
        manager = managers.FileManager(
            self._initializer_file_path,
            session=self._session,
            )
        manager.view()

    def view_metadata_module(self):
        r'''Views metadata module.

        Returns none.
        '''
        file_path = self._metadata_module_path
        if os.path.isfile(file_path):
            self._io_manager.view(file_path)

    def write_initializer_boilerplate(self, prompt=True):
        r'''Writes boilerplate initializer module.

        Returns none.
        '''
        from scoremanager import managers
        manager = managers.FileManager(
            self._initializer_file_path,
            session=self._session,
            )
        manager.write_boilerplate(prompt=prompt)

    def write_initializer_stub(self, prompt=True):
        r'''Wrties stub initializer module.

        Returns none.
        '''
        from scoremanager import managers
        manager = managers.FileManager(
            self._initializer_file_path,
            session=self._session,
            )
        manager._write_stub()
        message = 'stub initializer written.'
        self._io_manager.proceed(message)
