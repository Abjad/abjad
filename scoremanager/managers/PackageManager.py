# -*- encoding: utf-8 -*-
import os
from scoremanager.managers.Manager import Manager


class PackageManager(Manager):
    r'''Package manager.
    '''
    
    ### PRIVATE METHODS ###

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