# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class PackageWrangler(Wrangler):
    r'''Package wrangler.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        Wrangler.__init__(self, session=session)

    ### PRIVATE METHODS ###

    def _is_valid_directory_entry(self, expr):
        superclass = super(PackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _make_asset(self, path):
        assert os.path.sep in path
        package_name = os.path.basename(path)
        assert stringtools.is_snake_case_package_name(package_name)
        os.mkdir(path)
        package_manager = self._initialize_asset_manager(path)
        package_manager.fix(prompt=False)