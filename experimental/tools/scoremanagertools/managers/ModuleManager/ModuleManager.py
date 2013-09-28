# -*- encoding: utf-8 -*-
import os
from abjad.tools import iotools
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.managers.FileManager \
    import FileManager


class ModuleManager(FileManager):

    ### PRIVATE METHODS ###

    def _space_delimited_lowercase_name_to_asset_name(
        self, space_delimited_lowercase_name):
        space_delimited_lowercase_name = space_delimited_lowercase_name.lower()
        asset_name = space_delimited_lowercase_name.replace(' ', '_')
        asset_name += '.py'
        return asset_name
