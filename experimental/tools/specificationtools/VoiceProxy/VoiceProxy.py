from abjad.tools import timespantools
from abjad.tools.abctools.AbjadObject import AbjadObject


class VoiceProxy(AbjadObject):
    '''Voice proxy.
    '''

    ### INITIALIZER ###

    def __init__(self):
        from experimental.tools import specificationtools
        self._leaf_offset_list = []
        self._payload_expressions_by_attribute = specificationtools.AttributeDictionary()
        for attribute in self._payload_expressions_by_attribute:
            self._payload_expressions_by_attribute[attribute] = timespantools.TimespanInventory()
        self._voice_division_list = None

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def leaf_offset_list(self):
        '''Voice proxy leaf offset list.

        Return tuple.
        '''        
        return self._leaf_offset_list

    @property
    def payload_expressions_by_attribute(self):
        '''Voice proxy payload expressions by attribute.

        Return attribute dictionary.
        '''
        return self._payload_expressions_by_attribute

    @property
    def voice_division_list(self):
        '''Voice proxy voice division list.

        Return voice division list.
        '''
        return self._voice_division_list
