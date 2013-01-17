from abjad.tools.abctools import AbjadObject


class MaterialManager(AbjadObject):
    '''Material manager.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### PUBLIC METHODS ###

    def register_material(self, material):
        from experimental.tools import settingtools
        return settingtools.AbsoluteExpression(material)
