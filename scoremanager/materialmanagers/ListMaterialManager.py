# -*- encoding: utf-8 -*-
from scoremanager import iotools
from scoremanager.editors.ListEditor import ListEditor
from scoremanager.managers.MaterialManager import MaterialManager


class ListMaterialManager(MaterialManager):

    ### CLASS VARIABLES ###

    generic_output_name = 'list'
    output_material_checker = staticmethod(lambda x: isinstance(x, list))
    output_material_editor = ListEditor

    ### PUBLIC METHODS ###

    def _run_first_time(self):
        self._session._is_autoadding = True
        self._run(pending_user_input='omi')
        self._session._is_autoadding = False
