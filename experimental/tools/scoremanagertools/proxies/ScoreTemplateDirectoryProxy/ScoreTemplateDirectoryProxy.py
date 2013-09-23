# -*- encoding: utf-8 -*-
import os
import subprocess
from abjad.tools import sequencetools
from experimental.tools.scoremanagertools.proxies.DirectoryProxy \
    import DirectoryProxy


class ScoreTemplateDirectoryProxy(DirectoryProxy):

    ### INITIALIZER ###

    def __init__(self, score_package_path=None, session=None):
        score_directory_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            score_package_path)
        filesystem_path = os.path.join(
            score_directory_path, 
            'templates',
            )
        DirectoryProxy.__init__(
            self,
            filesystem_path=filesystem_path,
            session=session,
            )
