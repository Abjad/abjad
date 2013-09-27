# -*- encoding: utf-8 -*-
import os
import sys
from abjad.tools import iotools
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.proxies.FileManager import FileManager
from experimental.tools.scoremanagertools.proxies.ParseableModuleMixin \
    import ParseableModuleMixin


class ModuleManager(FileManager, ParseableModuleMixin):

    ### INITIALIZER ###

    def __init__(self, packagesystem_path=None, session=None):
        if packagesystem_path is None or \
            os.path.sep not in packagesystem_path:
            filesystem_path = \
                self.configuration.packagesystem_path_to_filesystem_path(
                packagesystem_path, 
                is_module=True,
                )
        else:
            filesystem_path = packagesystem_path
            packagesystem_path = \
                self.configuration.filesystem_path_to_packagesystem_path(
                filesystem_path,
                )
        self._packagesystem_path = packagesystem_path
        FileManager.__init__(
            self,
            filesystem_path=filesystem_path,
            session=session,
            )

    ### CLASS VARIABLES ###

    extension = '.py'

    _generic_class_name = 'module'

    _temporary_asset_name = 'temporary_module.py'

    ### PRIVATE PROPERTIES ###

    @property
    def _space_delimited_lowercase_name(self):
        if self.filesystem_basename:
            name_without_extension = \
                self.filesystem_basename.strip(self.extension)
            return stringtools.string_to_space_delimited_lowercase(
                name_without_extension)

    ### PRIVATE METHODS ###

    def _space_delimited_lowercase_name_to_asset_name(
        self, space_delimited_lowercase_name):
        asset_name = FileManager._space_delimited_lowercase_name_to_asset_name(
            self, space_delimited_lowercase_name)
        asset_name += '.py'
        return asset_name

    ### PUBLIC PROPERTIES ###

    @property
    def packagesystem_basename(self):
        if self.packagesystem_path:
            return self.packagesystem_path.split('.')[-1]

    @property
    def packagesystem_path(self):
        return self._packagesystem_path

    @property
    def parent_directory_filesystem_path(self):
        if self.packagesystem_path:
            return self.configuration.packagesystem_path_to_filesystem_path(
                self.parent_directory_packagesystem_path)

    @property
    def parent_directory_packagesystem_path(self):
        if self.packagesystem_path:
            return '.'.join(self.packagesystem_path.split('.')[:-1])

    ### PUBLIC METHODS ###

    def execute_file_lines(self, return_attribute_name=None):
        if os.path.isfile(self.filesystem_path):
            file_pointer = open(self.filesystem_path, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            exec(file_contents_string)
            if return_attribute_name is not None:
                if return_attribute_name in locals():
                    return locals()[return_attribute_name]

    def interpret_in_external_process(self):
        command = 'python {}'.format(self.filesystem_path)
        result = iotools.spawn_subprocess(command)
        if result != 0:
            self.session.io_manager.display('')
            self.session.io_manager.proceed()

    def read_file(self):
        if self.parse():
            try:
                self.execute_file_lines()
                return True
            except:
                pass
        return False

    def run_abjad(self, prompt=True):
        command = 'abjad {}'.format(self.filesystem_path)
        iotools.spawn_subprocess(command)
        self.session.io_manager.proceed(
            'file executed', 
            is_interactive=prompt,
            )

    def run_python(self, prompt=True):
        command = 'python {}'.format(self.filesystem_path)
        iotools.spawn_subprocess(command)
        self.session.io_manager.proceed(
            'file executed.', 
            is_interactive=prompt,
            )
