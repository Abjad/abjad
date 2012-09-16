from experimental import helpertools
from experimental.divisiontools.DivisionList import DivisionList


class VoiceDivisionList(DivisionList):
    r'''.. versionadded:: 1.0

    Voice division lists model all divisions that **start during** some voice.

    Composers do not create voice division lists because all
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
