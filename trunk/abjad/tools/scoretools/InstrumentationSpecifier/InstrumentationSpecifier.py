class InstrumentationSpecifier(object):
    r'''.. versionadded:: 2.5

    Abjad model of score instrumentation::

        abjad> flute = scoretools.Performer('Flute')
        abjad> flute.instruments.append(instrumenttools.Flute())
        abjad> flute.instruments.append(instrumenttools.AltoFlute())

    ::

        abjad> guitar = scoretools.Performer('Guitar')
        abjad> guitar.instruments.append(instrumenttools.Guitar())

    ::

        abjad> instrumentation_specifier = scoretools.InstrumentationSpecifier([flute, guitar])

    ::

        abjad> instrumentation_specifier
        InstrumentationSpecifier([Performer(name='Flute', instruments=[Flute(), AltoFlute()]), Performer(name='Guitar', instruments=[Guitar()])])

    Return instrumentation specifier.
    '''

    def __init__(self, performers=None):
        self.performers = performers

    ### OVERLOADS ###
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            # TODO: implement perform sort
            #if sorted(self.performers) == sorted(other.performers):
            if self.performers == other.performers:
                return True
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return self._repr_helper()

    ### PRIVATE ATTRIBUTES ###

    @property
    def _repr_with_tools_package(self):
        return self._repr_helper(include_tools_package=True)

    ### PRIVATE METHODS ###

    def _get_multiline_repr(self, include_tools_package=False):
        result = []
        if not self.performer_count:
            result.append(self._repr_helper(include_tools_package=include_tools_package))
        else:
            class_name = type(self).__name__
            if include_tools_package:
                tools_package = self.__module__.split('.')[-3]
                result.append('{}.{}(['.format(tools_package, class_name))
            else:
                result.append('{}(['.format(class_name))
            for performer in self.performers[:-1]:
                result.append('    {},'.format(
                    performer._repr_helper(include_tools_package=include_tools_package)))
            result.append('    {}])'.format(
                self.performers[-1]._repr_helper(include_tools_package=include_tools_package)))
            return result
        return result
            
    def _repr_helper(self, include_tools_package=False):
        class_name = type(self).__name__
        if include_tools_package:
            tools_package = self.__module__.split('.')[-3]
            performers = ', '.join([x._repr_with_tools_package for x in self.performers])
            return '{}.{}([{}])'.format(tools_package, class_name, performers)
        else:
            return '{}({!r})'.format(class_name, self.performers)

    ### PUBLIC ATTRIBUTES ###

    @property
    def instruments(self):
        r'''Read-only list of instruments derived from performers::

            abjad> instrumentation_specifier.instruments
            [Flute(), AltoFlute(), Guitar()]

        Return list.
        '''        
        instruments = []
        for performer in self.performers:
            instruments.extend(performer.instruments)
        return instruments

    @property
    def instrument_count(self):
        r'''Read-only number of instruments in score::
    
            abjad> instrumentation_specifier.instrument_count
            3

        Return nonnegative integer.
        '''
        return len(self.instruments)

    @property
    def performer_count(self):
        r'''Read-only number of performers in score::

            abjad> instrumentation_specifier.performer_count
            2

        Return nonnegative integer.
        '''
        return len(self.performers)

    @apply
    def performers():
        def fget(self):
            r'''Read / write list of performers in score::

                abjad> instrumentation_specifier.performers
                [Performer(name='Flute', instruments=[Flute(), AltoFlute()]), Performer(name='Guitar', instruments=[Guitar()])]

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
