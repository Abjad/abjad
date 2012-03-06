from abjad.core._MutableAbjadObject import _MutableAbjadObject
from abjad.tools.pitchtools.OctaveTranspositionMappingComponent import OctaveTranspositionMappingComponent


class OctaveTranspositionMapping(list, _MutableAbjadObject):
    '''.. versionadded:: 2.8

    Octave transposition mapping::

        abjad> pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
        OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])

    Model ``pitchtools.transpose_chromatic_pitch_number_by_octave_transposition_mapping`` input.
    (See the docs to that function.)

    Octave transposition mappings inherit from list and are mutable.
    '''

    def __init__(self, arg_list=None):
        list.__init__(self)
        arg_list = arg_list or []
        self.extend(arg_list)

    ### OVERLOADS ###
    
    def __contains__(self, expr):
        try:
            mapping_component = OctaveTranspositionMappingComponent(expr)
            return list.__contains__(self, mapping_component)
        except ValueError:
            return False

    def __repr__(self):
        return '{}([{}])'.format(self.class_name, self._repr_contents_string)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _repr_contents_string(self):
        result = []
        for mapping_component in self:
            result.append(mapping_component._input_argument_token)
        return ', '.join(result)
    
    ### PUBLIC METHODS ###

    def append(self, expr):
        '''Change `expr` to octave transpositon mapping component and append::

            abjad> mapping = pitchtools.OctaveTranspositionMapping([])
            abjad> mapping.append(('[A0, C4)', 15))

        ::

            abjad> mapping
            OctaveTranspositionMapping([('[A0, C4)', 15)])

        Return none.
        '''
        list.append(self, OctaveTranspositionMappingComponent(expr))
    
    def extend(self, expr):
        '''Change elements in `expr` to octave transposition mappings and then extend::

            abjad> mapping = pitchtools.OctaveTranspositionMapping([])
            abjad> mapping.extend([('[A0, C4)', 15), ('[C4, C8)', 27)])

        ::

            abjad> mapping
            OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])

        Return none.
        '''
        for x in expr:
            self.append(x)
