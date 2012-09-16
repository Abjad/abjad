from experimental import helpertools
from experimental.divisiontools.DivisionList import DivisionList


class RhythmRegionDivisionList(DivisionList):
    r'''.. versionadded:: 1.0

    A region is an uninterrupted block of time to which a command applies.

    A rhythm region is an uninterrupted block of time to which a rhythm-maker applies.

    A rhythm region division list is the division list passed as
    input to a rhythm-maker.

    Composers do not create rhythm region division lists because all
    division lists arise as byproducts of interpretation.
    '''

    ### INITIALIZER ###

    def __init__(self, divisions, voice_name):
        voice_name = helpertools.expr_to_component_name(voice_name)
        DivisionList.__init__(self, divisions)
        self._voice_name = voice_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def voice_name(self):
        '''Division list voice name.

        Return string.
        '''
        return self._voice_name
