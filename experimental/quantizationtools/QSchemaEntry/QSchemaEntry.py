from abjad.tools import abctools
from abjad.tools import contexttools
from abjad.tools import durationtools
from collections import OrderedDict
from experimental.quantizationtools.QGridSearchTree import QGridSearchTree
from experimental.quantizationtools.is_valid_beatspan import is_valid_beatspan


class QSchemaEntry(tuple, abctools.ImmutableAbjadObject):
    '''Represents one "point" in some quantization process where the rules for 
    quantization change.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()
    _fields = ('beatspan', 'search_tree', 'tempo', 'time_signature')

    ### INITIALIZER ###

    def __new__(cls, beatspan=None, search_tree=None, tempo=None, time_signature=None):

        if search_tree is not None:
            search_tree = QGridSearchTree(search_tree)

        if tempo is not None:
            tempo = contexttools.TempoMark(tempo)

        if time_signature is not None:
            time_signature = contexttools.TimeSignatureMark(time_signature)

        if beatspan is not None:
            beatspan = durationtools.Duration(beatspan)
            if time_signature is None:
                assert is_valid_beatspan(beatspan)
            else:
                assert time_signature.denominator == beatspan.denominator
                assert beatspan <= time_signature.duration
                assert time_signature.duration % beatspan == 0

        return tuple.__new__(cls, (beatspan, search_tree, tempo, time_signature))

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return tuple(self)

    def __repr__(self):
        return '\n'.join(self._get_tools_package_qualified_repr_pieces())

    ### SPECIAL METHODS ###

    @property
    def __dict__(self):
        return OrderedDict(zip(self._fields, self))

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def beatspan(self):
        '''The beatspan value optionally associated with this QSchemaEntry.'''
        return self[0]

    @property
    def search_tree(self):
        '''The QGridSearchTree optionally associated with this QSchemaEntry.'''
        return self[1]

    @property
    def tempo(self):
        '''The TempoMark optionally associated with this QSchemaEntry.'''
        return self[2]

    @property
    def time_signature(self):
        '''The TimeSignatureMark optionally associated with this QSchemaEntry.'''
        return self[3]

