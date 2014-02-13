# -*- encoding: utf-8 -*-
from scoremanager import iotools
from scoremanager.editors.ListEditor import ListEditor
from scoremanager.managers.MaterialPackageManager import MaterialPackageManager


class ListMaterialPackageManager(MaterialPackageManager):

    ### CLASS VARIABLES ###

    generic_output_name = 'list'
    output_material_checker = staticmethod(lambda x: isinstance(x, list))
    output_material_editor = ListEditor

    ### PUBLIC METHODS ###

    def run_first_time(self):
        self.session.is_autoadding = True
        self._run(pending_user_input='omi')
        self.session.is_autoadding = False
