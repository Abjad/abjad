class _Flageolet(object):
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
