# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import stringtools
from scoremanager.managers.Manager import Manager


class DirectoryManager(Manager):
    r'''Directory manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_asset_manager_class',
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        from scoremanager import managers
        superclass = super(DirectoryManager, self)
        superclass.__init__(
            path=path,
            session=session,
            )
        self._asset_manager_class = managers.FileManager

    ### PRIVATE PROPERTIES ###

    @property
    def _metadata_module_path(self):
        file_path = os.path.join(self._path, '__metadata__.py')
        return file_path

    @property
    def _space_delimited_lowercase_name(self):
        if self._path:
            base_name = os.path.basename(self._path)
            result = base_name.replace('_', ' ')
            return result

    @property
    def _user_input_to_action(self):
        superclass = super(DirectoryManager, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'mda': self.add_metadatum,
            'mdg': self.get_metadatum,
            'mdrm': self.remove_metadatum,
            'mdmro': self.view_metadata_module,
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

    def _get_file_manager(self, file_path):
        from scoremanager import managers
        file_manager = managers.FileManager(
            file_path,
            session=self._session,
            )
        return file_manager

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

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self._run_asset_manager(result)

    def _list_visible_asset_paths(self):
        file_names = self._list()
        file_names = [x for x in file_names if x[0].isalpha()]
        file_paths = []
        for file_name in file_names:
            file_path = os.path.join(self._path, file_name)
            file_paths.append(file_path)
        return file_paths

    def _make_asset_menu_section(self, menu):
        menu_entries = self._make_asset_menu_entries()
        if not menu_entries:
            return
        section = menu.make_asset_section(
            menu_entries=menu_entries,
            )
        menu._asset_section = section

    def _make_empty_asset(self, prompt=False):
        if not os.path.exists(self._path):
            os.makedirs(self._path)
            if self._is_in_git_repository(self._path):
                file_path = os.path.join(self._path, '.gitignore')
                with file(file_path, 'w') as file_pointer:
                    file_pointer.write('')
        self._io_manager.proceed(prompt=prompt)

    def _make_main_menu(self, name='directory manager'):
        menu = self._io_manager.make_menu(name=name)
        self._main_menu = menu
        self._make_asset_menu_section(menu)
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

    # TODO: remove prompt messaging
    def _remove_metadatum(self, metadatum_name):
        metadata = self._get_metadata()
        was_removed = False
        try:
            del(metadata[metadatum_name])
            was_removed = True
        except KeyError:
            pass
        if was_removed:
            self.rewrite_metadata_module(metadata, prompt=False)

    def _run_asset_manager(
        self,
        path,
        ):
        manager = self._asset_manager_class(
            path=path,
            session=self._session,
            )
        manager._run()

    def _write_metadata_module(self, metadata):
        lines = []
        lines.append(self._unicode_directive)
        lines.append('import collections')
        lines.append('')
        lines.append('')
        lines = '\n'.join(lines)
        metadata_lines = self._make_metadata_lines(metadata)
        lines = lines + '\n' + metadata_lines
        with file(self._metadata_module_path, 'w') as file_pointer:
            file_pointer.write(lines)

    ### PUBLIC METHODS ###

    def add_metadatum(self):
        r'''Adds metadatum to metadata module.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_snake_case_string('metadatum name', allow_empty=False)
        getter.append_expr('metadatum value')
        result = getter._run()
        if self._should_backtrack():
            return
        if result:
            metadatum_name, metadatum_value = result
            self._add_metadatum(metadatum_name, metadatum_value)

    def edit_metadata_module(self):
        r'''Edits metadata module.

        Returns none.
        '''
        file_path = self._metadata_module_path
        if os.path.isfile(file_path):
            self._io_manager.edit(file_path)

    def get_metadatum(self):
        r'''Gets metadatum from metadata module.

        Returns none.
        '''
        getter = self._io_manager.make_getter()
        getter.append_string('metadatum name')
        result = getter._run()
        if self._should_backtrack():
            return
        metadatum = self._get_metadatum(result)
        message = '{!r}'.format(metadatum)
        self._io_manager.proceed(message=message)

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
        getter = self._io_manager.make_getter()
        getter.append_string('metadatum name')
        result = getter._run()
        if self._should_backtrack():
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
        r'''Renames directory.

        Returns none.
        '''
        base_name = os.path.basename(self._path)
        line = 'current name: {}'.format(base_name)
        self._io_manager.display(line)
        getter = self._io_manager.make_getter()
        getter.append_snake_case_package_name('new name')
        new_package_name = getter._run()
        if self._should_backtrack():
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
        self._write_metadata_module(metadata)
        if prompt:
            message = 'rewrote metadata module.'
            self._io_manager.proceed(message)

    def view_metadata_module(self):
        r'''Views metadata module.

        Returns none.
        '''
        file_path = self._metadata_module_path
        if os.path.isfile(file_path):
            self._io_manager.view(file_path)