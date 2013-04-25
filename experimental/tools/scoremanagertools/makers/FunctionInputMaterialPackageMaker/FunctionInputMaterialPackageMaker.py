from experimental.tools.scoremanagertools.makers.MaterialPackageMaker import MaterialPackageMaker


class FunctionInputMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    should_have_user_input_module = True
    user_input_demo_values = []
    user_input_module_import_statements = []
    user_input_tests = []
