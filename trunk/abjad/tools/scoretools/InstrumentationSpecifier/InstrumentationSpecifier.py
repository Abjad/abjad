class InstrumentationSpecifier(object):
    r'''.. versionadded:: 2.5

    Abjad model of score instrumentation.
    '''

    def __init__(self, performers=None):
        self.performers = performers

    ### OVERLOADS ###
    
    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.performers)

    ### PUBLIC ATTRIBUTES ###

    @property
    def instruments(self):
        r'''Read-only list of instruments derived from performers.

        Return list.
        '''        
        instruments = []
        for performer in self.performers:
            instruments.extend(performer.instruments)
        return instruments

    @property
    def instrument_count(self):
        r'''Read-only number of instruments in score.
    
        Return nonnegative integer.
        '''
        return len(self.instruments)

    @property
    def performer_count(self):
        r'''Read-only number of performers in score.

        Return nonnegative integer.
        '''
        return len(self.performers)

    @apply
    def performers():
        def fget(self):
            r'''Read / write list of performers in score.

            Return list.
            '''
            return self._performers
        def fset(self, performers):
            from abjad.tools import scoretools
            assert isinstance(performers, (list, type(None)))
            if performers is None:
                self._performers = []
            else:
                assert all([isinstance(x, scoretools.Performer) for x in performers])
                self._performers = list(performers[:])
        return property(**locals())
