from abjad.core._ImmutableAbjadObject import _ImmutableAbjadObject


class _Flageolet(_ImmutableAbjadObject):
    '''Abjad model of both natural and artificial harmonics.
    Abstract base class.
    '''

    __slots__ = ()

    ### PUBLIC ATTRIBUTES ###

    @property
    def suono_reale(self):
        '''Actual sound of the harmonic when played.
        '''
        raise Exception('Not Implemented')
