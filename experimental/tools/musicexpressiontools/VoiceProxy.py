# -*- encoding: utf-8 -*-
from abjad.tools import timerelationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class VoiceProxy(AbjadObject):
    r'''Voice proxy.
    '''

    ### INITIALIZER ###

    def __init__(self):
        from experimental.tools import musicexpressiontools
        self._leaf_start_offsets = []
        self._leaf_stop_offsets = []
        self._leaves = []
        self._payload_expressions_by_attribute = \
            musicexpressiontools.AttributeDictionary()
        for attribute in self._payload_expressions_by_attribute:
            self._payload_expressions_by_attribute[attribute] = \
                timerelationtools.TimespanInventory()
        self._voice_division_list = None

    ### PUBLIC PROPERTIES ###

    @property
    def leaf_start_offsets(self):
        r'''Voice proxy leaf start offsets.

        Returns list of offsets.
        '''
        return self._leaf_start_offsets

    @property
    def leaf_stop_offsets(self):
        r'''Voice proxy leaf stop offsets.

        Returns list of offsets.
        '''
        return self._leaf_stop_offsets

    @property
    def leaves(self):
        r'''Voice proxy leaves.

        Returns list of leaves.
        '''
        return self._leaves

    @property
    def payload_expressions_by_attribute(self):
        r'''Voice proxy payload expressions by attribute.

        Returns attribute dictionary.
        '''
        return self._payload_expressions_by_attribute

    @property
    def voice_division_list(self):
        r'''Voice proxy voice division list.

        Returns voice division list.
        '''
        return self._voice_division_list
