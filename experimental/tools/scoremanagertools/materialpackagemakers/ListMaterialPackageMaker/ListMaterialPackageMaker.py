from experimental.tools.scoremanagertools import io
from experimental.tools.scoremanagertools.editors.ListEditor import ListEditor
from experimental.tools.scoremanagertools.materialpackagemakers.MaterialPackageMaker import MaterialPackageMaker


class ListMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS VARIABLES ###

    generic_output_name = 'list'
    output_material_checker = staticmethod(lambda x: isinstance(x, list))
    output_material_editor = ListEditor

    ### PUBLIC METHODS ###

    def run_first_time(self):
        self._session.is_autoadding = True
        self._run(user_input='omi')
        self._session.is_autoadding = False
