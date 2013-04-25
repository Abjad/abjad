from experimental.tools.scoremanagertools import menuing
from experimental.tools.scoremanagertools.editors.ListEditor import ListEditor
from experimental.tools.scoremanagertools.makers.MaterialPackageMaker import MaterialPackageMaker


class ListMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'list'
    output_material_checker = staticmethod(lambda x: isinstance(x, list))
    output_material_editor = ListEditor

    ### PUBLIC METHODS ###

    def run_first_time(self):
        self.session.is_autoadding = True
        self.run(user_input='omi')
        self.session.is_autoadding = False
