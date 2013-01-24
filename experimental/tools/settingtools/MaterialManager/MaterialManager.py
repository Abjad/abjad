from abjad.tools import iotools
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
        #return settingtools.PayloadExpression(material)
        if isinstance(material, (tuple, list)):
            return settingtools.PayloadExpression(material)
        elif isinstance(material, (str)):
            component = iotools.p(material)
            return settingtools.StartPositionedRhythmPayloadExpression([component], start_offset=0)
        else:
            raise TypeError(material)
