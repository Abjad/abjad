from abjad.core._MutableAbjadObject import _MutableAbjadObject
from abjad.tools.pitchtools.OctaveTranspositionMapping import OctaveTranspositionMapping


class OctaveTranspositionMappingInventory(list, _MutableAbjadObject):
    '''.. versionadded:: 2.8

    Model of an ordered list of octave transposition mappings::

        abjad> mapping_1 = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
        abjad> mapping_2 = pitchtools.OctaveTranspositionMapping([('[A0, C8]', -18)])
        abjad> inventory = pitchtools.OctaveTranspositionMappingInventory([mapping_1, mapping_2])

    ::

        abjad> inventory
        OctaveTranspositionMappingInventory([OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)]), OctaveTranspositionMapping([('[A0, C8]', -18)])])

    Octave transposition mapping inventories inherit from list and are mutable.
    '''

    def __init__(self, octave_transposition_mapping_tokens=None):
        list.__init__(self)
        octave_transposition_mapping_tokens = octave_transposition_mapping_tokens or []
        self.extend(octave_transposition_mapping_tokens)

    ### OVERLOADS ###

    def __contains__(self, expr):
        try:
            mapping = OctaveTranspositionMapping(expr)
            return list.__contains__(self, mapping)
        except ValueError:
            return False
        
    def __repr__(self):
        return '{}({})'.format(self.class_name, list.__repr__(self))

    ### PUBLIC METHODS ###

    def append(self, expr):
        '''Change `expr` to octave transposition mapping and append::

            abjad> inventory = pitchtools.OctaveTranspositionMappingInventory([])
            abjad> inventory.append(pitchtools.OctaveTranspositionMapping([('[A0, C8]', -18)]))

        ::

            abjad> inventory
            OctaveTranspositionMappingInventory([OctaveTranspositionMapping([('[A0, C8]', -18)])])

        Return none.
        '''
        mapping = OctaveTranspositionMapping(expr)
        list.append(self, mapping)

    def extend(self, expr):
        '''Change elements in `expr` to octave transposition mapping and extend::

            abjad> inventory = pitchtools.OctaveTranspositionMappingInventory([])
            abjad> inventory.extend([([('[A0, C8]', -18)]), ([('[C4, C6]', 39)])])

        ::

            abjad> inventory
            OctaveTranspositionMappingInventory([OctaveTranspositionMapping([('[A0, C8]', -18)]), OctaveTranspositionMapping([('[C4, C6]', 39)])])

        Return none.
        '''
        for x in expr:
            self.append(x)
