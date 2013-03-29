from make_illustration_from_output_material import make_illustration_from_output_material
from scf.editors.ConstellationCircuitSelectionEditor import ConstellationCircuitSelectionEditor
from scf.makers.MaterialPackageMaker import MaterialPackageMaker


class ConstellationCircuitSelectionMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'constellation circuit selection'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, list))
    output_material_editor = ConstellationCircuitSelectionEditor

    ### PUBLIC METHODS ###

    def run_first_time(self):
        self.session.is_autoadding = True
        self.run(user_input='omi')
        self.session.is_autoadding = False
