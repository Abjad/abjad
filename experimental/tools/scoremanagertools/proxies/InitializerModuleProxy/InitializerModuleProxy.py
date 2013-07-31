# -*- encoding: utf-8 -*-
import collections
import os
from experimental.tools.scoremanagertools.proxies.ModuleProxy \
    import ModuleProxy


class InitializerModuleProxy(ModuleProxy):

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        assert '__init__' in filesystem_path, repr(filesystem_path)
        packagesystem_path = \
            self.configuration.filesystem_path_to_packagesystem_path(
            filesystem_path)
        ModuleProxy.__init__(
            self,
            packagesystem_path=packagesystem_path,
            session=session)

    ### CLASS VARIABLES ###

    extension = '.py'

    ### PUBLIC METHODS ###

    def has_line(self, line):
        file_pointer = open(self.filesystem_path, 'r')
        for file_line in file_pointer.readlines():
            if file_line == line:
                file_pointer.close()
                return True
        file_pointer.close()
        return False

    def interactively_restore(self, prompt=False):
        self.write_stub_to_disk()
        self.session.io_manager.proceed(is_interactive=prompt)

    def write_stub_to_disk(self):
        file_pointer = open(self.filesystem_path, 'w')
        file_pointer.write('')
        file_pointer.close()
