from abjad.tools import timespantools
from abjad.tools.abctools.AbjadObject import AbjadObject


class VoiceProxy(AbjadObject):
    '''Voice proxy.
    '''

    ### INITIALIZER ###

    def __init__(self):
        from experimental.tools import musicexpressiontools
        self._leaf_start_offsets = []
        self._leaf_stop_offsets = []
        self._leaves = []
        self._payload_expressions_by_attribute = musicexpressiontools.AttributeDictionary()
        for attribute in self._payload_expressions_by_attribute:
            self._payload_expressions_by_attribute[attribute] = timespantools.TimespanInventory()
        self._voice_division_list = None

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def leaf_start_offsets(self):
        '''Voice proxy leaf start offsets.

        Return list of offsets.
        '''        
        return self._leaf_start_offsets

    @property
    def leaf_stop_offsets(self):
        '''Voice proxy leaf stop offsets.

        Return list of offsets.
        '''        
        return self._leaf_stop_offsets

    @property
    def leaves(self):
        '''Voice proxy leaves.

        Return list of leaves.
        '''
        return self._leaves

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
