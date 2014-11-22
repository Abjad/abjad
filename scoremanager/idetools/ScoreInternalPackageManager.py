# -*- encoding: utf-8 -*-
import itertools
import os
import shutil
from abjad.tools import systemtools
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
            'dc': self.check_definition_py,
            'de': self.edit_definition_py,
            'ds': self.write_stub_definition_py,
            #
            'vr': self.version_package,
            'vl': self.list_versions_directory,
            })
        return result

    @property
    def _versions_directory(self):
        return os.path.join(self._path, 'versions')

    ### PRIVATE METHODS ###

    def _audit_version_differences(self):
        last_version_number = self._get_last_version_number() or 0
        last_version_string = '%04d' % last_version_number
        next_version_number = last_version_number + 1
        next_version_string = '%04d' % next_version_number
        messages = []
        found_differing_artifacts = False
        versions_directory = self._versions_directory
        for source_path in self._source_paths:
            message = ' FROM: {}'.format(source_path)
            messages.append(message)
            base_name = os.path.basename(source_path)
            root, extension = os.path.splitext(base_name)
            file_name = '{}_{}{}'.format(root, last_version_string, extension)
            last_versioned_path = os.path.join(versions_directory, file_name)
            file_name = '{}_{}{}'.format(root, next_version_string, extension)
            next_versioned_path = os.path.join(versions_directory, file_name)
            message = '   TO: {}'.format(next_versioned_path)
            messages.append(message)
            comparison_method = systemtools.TestManager.compare_files
            if not comparison_method(source_path, last_versioned_path):
                found_differing_artifacts = True
        if found_differing_artifacts:
            messages.append('')
        else:
            messages = ['   IN: {}'.format(self._path)]
        return found_differing_artifacts, messages

    def _make_package_menu_section(self, menu, commands_only=False):
        superclass = super(ScoreInternalPackageManager,self)
        commands = superclass._make_package_menu_section(
            menu, commands_only=True)
        commands.append(('package - version', 'vr'))
        if commands_only:
            return commands
        if commands:
            menu.make_command_section(
                is_hidden=True,
                commands=commands,
                name='package',
                )

    def _make_version_package_messages(self):
        last_version_number = self._get_last_version_number() or 0
        next_version_number = last_version_number + 1
        next_version_string = '%04d' % next_version_number
        messages = []
        for source_path in self._source_paths:
            root, extension = os.path.splitext(source_path)
            message = ' FROM: {}'.format(source_path)
            messages.append(message)
            directory = self._versions_directory
            file_name = '{}_{}{}'.format(root, next_version_string, extension)
            target_path = os.path.join(directory, file_name)
            message = '   TO: {}'.format(target_path)
            messages.append(message)
        return messages

    def _make_versions_directory_menu_section(self, menu, commands_only=False):
        commands = []
        commands.append(('versions - list', 'vl'))
        commands.append(('versions - definition.py - edit', 'vde'))
        commands.append(('versions - illustration.ly - edit', 'vie'))
        commands.append(('versions - illustration.pdf - open', 'vio'))
        if commands_only:
            return commands
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='versions directory',
            )

    ### PUBLIC METHODS ###

    def check_definition_py(self, dry_run=False):
        r'''Checks ``definition.py``.

        Display errors generated during interpretation.
        '''
        inputs, outputs = [], []
        if dry_run:
            inputs.append(self._definition_py_path)
            return inputs, outputs
        stderr_lines = self._io_manager.check_file(self._definition_py_path)
        if stderr_lines:
            messages = [self._definition_py_path + ' FAILED:']
            messages.extend('    ' + _ for _ in stderr_lines)
            self._io_manager._display(messages)
        else:
            message = '{} OK.'.format(self._definition_py_path)
            self._io_manager._display(message)

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

    def interpret_illustration_ly(self, dry_run=False):
        r'''Interprets ``illustration.ly``.

        Makes ``illustration.pdf``.

        Returns pair. List of STDERR messages from LilyPond together
        with list of candidate messages.
        '''
        inputs, outputs = [], []
        if os.path.isfile(self._illustration_ly_path):
            inputs.append(self._illustration_ly_path)
            outputs.append((self._illustration_pdf_path,))
        if dry_run:
            return inputs, outputs
        if not os.path.isfile(self._illustration_ly_path):
            message = 'The file {} does not exist.'
            message = message.format(self._illustration_ly_path)
            self._io_manager._display(message)
            return [], []
        messages = self._format_messaging(inputs, outputs)
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking or not result:
            return [], []
        result = self._io_manager.run_lilypond(self._illustration_ly_path)
        subprocess_messages, candidate_messages = result
        return subprocess_messages, candidate_messages

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
        for directory_entry in sorted(os.listdir(versions_directory)):
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
        found_different_artifact, messages = self._audit_version_differences()
        if not found_different_artifact:
            messages.insert(0, 'nothing to version:')
            self._io_manager._display(messages)
            return
        messages.insert(0, 'will copy ...')
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