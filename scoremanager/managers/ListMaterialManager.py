# -*- encoding: utf-8 -*-
from scoremanager import iotools
from scoremanager.editors.ListEditor import ListEditor
from scoremanager.managers.MaterialManager import MaterialManager


class ListMaterialManager(MaterialManager):

    ### CLASS VARIABLES ###

    _output_material_checker = staticmethod(lambda x: isinstance(x, list))

    _output_material_editor = ListEditor

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        superclass = super(ListMaterialManager, self)
        superclass.__init__(filesystem_path=filesystem_path, session=session)
        self._generic_output_name = 'list'

    ### PUBLIC METHODS ###

    def _run_first_time(self):
        self._session._is_autoadding = True
        self._run(pending_user_input='omi')
        self._session._is_autoadding = False
