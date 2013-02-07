from abjad.tools import timespantools
from abjad.tools.abctools.AbjadObject import AbjadObject


class VoiceProxy(AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        from experimental.tools import expressiontools
        from experimental.tools import specificationtools
        self._division_payload_expressions = \
            timespantools.TimespanInventory()
        self._rhythm_payload_expressions = \
            timespantools.TimespanInventory()
        self._voice_division_list = None

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def division_payload_expressions(self):
        '''Context proxy division payload expressions.

        Return inventory.
        '''
        return self._division_payload_expressions

    @property
    def rhythm_payload_expressions(self):
        '''Context proxy rhythm payload expressions.

        Return inventory.
        '''
        return self._rhythm_payload_expressions

    # TODO: rename to division_list
    @property
    def voice_division_list(self):
        '''Context proxy voice division list.

        Return voice division list.
        '''
        return self._voice_division_list
