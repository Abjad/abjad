# -*- encoding: utf-8 -*-
import itertools
import os
import shutil
from scoremanager.idetools.PackageManager import PackageManager


class ScoreInternalPackageManager(PackageManager):
    r'''Score-internal package manager.

    Abstract class from which ``MaterialPackageManager`` and
    ``SegmentPackageManager`` inherit.

    Implements versioning functionality.

    Implements sibling package navigation functionality.
    '''

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(ScoreInternalPackageManager, self)
        superclass.__init__(path=path, session=session)
        required_directories = list(self._required_directories)
        required_directories.append('versions')
        self._required_directories = tuple(required_directories)
        optional_files = list(self._optional_files)
        optional_files.append('definition.py')
        self._optional_files = tuple(optional_files)

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        superclass = super(ScoreInternalPackageManager, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            '<': self.go_to_previous_package,
            '>': self.go_to_next_package,
            #
            'vr': self.version_package,
            'vrls': self.list_versions_directory,
            })
        return result

    @property
    def _versions_directory(self):
        return os.path.join(self._path, 'versions')

    ### PRIVATE METHODS ###

    def _make_package_menu_section(self, menu, commands_only=False):
        superclass = super(ScoreInternalPackageManager,self)
        commands = superclass._make_package_menu_section(
            menu, commands_only=True)
        commands.append(('package - version', 'vr'))
        commands.append(('package - versions list', 'vrls'))
        if commands_only:
            return commands
        if commands:
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='package',
                )

    ### PUBLIC METHODS ###

    def go_to_next_package(self):
        r'''Goes to next package.

        Returns none.
        '''
        self._go_to_next_package()

    def go_to_previous_package(self):
        r'''Goes to previous package.

        Returns none.
        '''
        self._go_to_previous_package()

    def list_versions_directory(self, messages_only=False):
        r'''Lists versions directory.

        Returns none.
        '''
        versions_directory = self._versions_directory
        if not os.path.exists(versions_directory):
            message = 'no versions directory found {}.'
            message = message.format(self._versions_directory)
            self._io_manager._display(message)
            return
        file_names = []
        for directory_entry in os.listdir(versions_directory):
            if directory_entry[0].isalnum():
                file_names.append(directory_entry)
        file_names.sort(key=lambda _: self._file_name_to_version_number(_))
        messages = []
        def group_helper(file_name):
            root, extension = os.path.splitext(file_name)
            return root[-4:]
        for x in itertools.groupby(
            file_names,
            key=lambda _: self._file_name_to_version_number(_),
            ):
            key, file_names = x
            message = ' '.join(file_names)
            messages.append(message)
        if not messages:
            message = 'versions directory is empty.'
            messages.append(message)
        if messages_only:
            return messages
        else:
            self._io_manager._display(messages, capitalize=False)

    def version_package(self):
        r'''Versions package.
        
        Returns none.
        '''
        if not os.path.isdir(self._versions_directory):
            os.mkdir(self._versions_directory)
        messages = []
        messages.append('will copy ...')
        messages.extend(self._make_version_package_messages())
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return
        next_version_string = self._get_next_version_string()
        for source_path in self._source_paths:
            if not os.path.isfile(source_path):
                continue
            file_name = os.path.basename(source_path)
            root, extension = os.path.splitext(file_name)
            target_file_name = '{}_{}{}'.format(
                root,
                next_version_string,
                extension,
                )
            target_path = os.path.join(
                self._versions_directory,
                target_file_name,
                )
            shutil.copyfile(source_path, target_path)