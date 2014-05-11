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
        '_package_name',
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(DirectoryManager, self)
        superclass.__init__(path=path, session=session)
        assert path is not None
        self._package_name = os.path.basename(path)

    ### PRIVATE PROPERTIES ###

    @property
    def _initializer_file_path(self):
        return os.path.join(self._path, '__init__.py')

    @property
    def _input_to_action(self):
        superclass = super(DirectoryManager, self)
        result = superclass._input_to_action
        result = result.copy()
        result.update({
            'ino': self.open_initializer,
            'inws': self.write_stub_initializer,
            'mda': self.add_metadatum,
            'mdg': self.get_metadatum,
            'mdrm': self.remove_metadatum,
            'mdmo': self.open_metadata_module,
            'mdmrw': self.rewrite_metadata_module,
            })
        return result

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
    def _views_module_path(self):
        file_path = os.path.join(self._path, '__views__.py')
        return file_path

    ### PRIVATE METHODS ###

    def _add_metadatum(self, metadatum_name, metadatum_value):
        assert ' ' not in metadatum_name, repr(metadatum_name)
        metadata = self._get_metadata()
        metadata[metadatum_name] = metadatum_value
        self.rewrite_metadata_module(
            metadata=metadata, 
            confirm=False, 
            notify=False,
            )

    def _enter_run(self):
        self._session._is_navigating_to_next_asset = False
        self._session._is_navigating_to_previous_asset = False
        self._session._last_asset_path = self._path

    def _get_metadata(self):
        metadata = None
        if os.path.isfile(self._metadata_module_path):
            file_pointer = open(self._metadata_module_path, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            try:
                exec(file_contents_string)
            except:
                message = 'can not interpret metadata module: {!r}.'
                message = message.format(self)
                print(message)
            metadata = locals().get('metadata')
        metadata = metadata or collections.OrderedDict()
        return metadata

    def _get_metadatum(self, metadatum_name):
        metadata = self._get_metadata()
        metadatum = metadata.get(metadatum_name, None)
        return metadatum

    def _handle_main_menu_result(self, result):
        if result in self._input_to_action:
            self._input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self._run_asset_manager(result)

#    def _make_asset_menu_section(self, menu):
#        menu_entries = self._make_asset_menu_entries()
#        if not menu_entries:
#            return
#        section = menu.make_asset_section(
#            menu_entries=menu_entries,
#            )

    def _make_main_menu(self, name='directory manager'):
        menu = self._io_manager.make_menu(name=name)
        return menu

    @staticmethod
    def _make_metadata_lines(metadata):
        if metadata:
            lines = []
            for key, value in sorted(metadata.items()):
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
            self.rewrite_metadata_module(
                metadata=metadata, 
                confirm=False, 
                notify=False,
                )

    def _rename_interactively(
        self,
        extension=None,
        file_name_callback=None,
        force_lowercase=True,
        ):
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
        result = self._io_manager.confirm()
        if self._should_backtrack():
            return
        if not result:
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

    def _run_asset_manager(
        self,
        path,
        ):
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        manager._run()

    def _run_first_time(self, **kwargs):
        self._run(**kwargs)

    def _write_metadata_module(self, metadata):
        lines = []
        lines.append(self._unicode_directive)
        lines.append('import collections')
        lines.append('')
        lines.append('')
        contents = '\n'.join(lines)
        metadata_lines = self._make_metadata_lines(metadata)
        contents = contents + '\n' + metadata_lines
        with file(self._metadata_module_path, 'w') as file_pointer:
            file_pointer.write(contents)

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

    def open_initializer(self):
        r'''Opens initializer.

        Returns none.
        '''
        self._io_manager.open_file(self._initializer_file_path)

    def open_metadata_module(self):
        r'''Edits metadata module.

        Returns none.
        '''
        path = self._metadata_module_path
        if os.path.isfile(path):
            self._io_manager.edit(path)
        else:
            message = 'can not find {}.'.format(path)
            self._io_manager.display([message, ''])

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

    def rewrite_metadata_module(
        self, 
        confirm=True, 
        metadata=None, 
        notify=True,
        ):
        r'''Rewrites metadata module.

        Returns none.
        '''
        if metadata is None:
            metadata = self._get_metadata()
        self._write_metadata_module(metadata)
        if notify:
            message = 'rewrote metadata module.'
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True

    def write_stub_initializer(self, confirm=True, notify=True):
        r'''Writes initializer stub.

        Returns none.
        '''
        path = self._initializer_file_path
        if notify:
            message = 'will write stub to {}.'
            message = message.format(path)
            self._io_manager.display(message)
        if confirm:
            result = self._io_manager.confirm()
            if self._should_backtrack():
                return
            if not result:
                return
        self._io_manager.write_stub(self._initializer_file_path)
        if notify:
            message = 'wrote stub to {}.'
            message = message.format(path)
            self._io_manager.display([message, ''])
            self._session._hide_next_redraw = True