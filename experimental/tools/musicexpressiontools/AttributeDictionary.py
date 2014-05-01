# -*- encoding: utf-8 -*-
import collections
from abjad.tools import datastructuretools
from abjad.tools import timespantools
from experimental.tools.musicexpressiontools.AttributeNameEnumeration \
    import AttributeNameEnumeration


class AttributeDictionary(datastructuretools.TypedOrderedDict):
    r'''Attribute dictionary.
    '''

    ### CLASS VARIABLES ##

    attributes = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self):
        #collections.OrderedDict.__init__(self)
        datastructuretools.TypedOrderedDict.__init__(self)
        for attribute in self.attributes:
            self[attribute] = timespantools.TimespanInventory()
        assert 'time_signatures' in self

    ### SPECIAL METHODS ###

    def __repr__(self):
        return collections.OrderedDict.__repr__(self)

    def __setitem__(self, key, value):
        assert isinstance(key, str), repr(key)
        assert isinstance(value, (list, datastructuretools.TypedList)), \
            repr(value)
        datastructuretools.TypedOrderedDict.__setitem__(self, key, value)
