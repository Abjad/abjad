from abjad.tools import introspectiontools
from experimental.specificationtools.Selector import Selector


class BackgroundElementSelector(Selector):
    r'''.. versionadded:: 1.0

    Select one background object with mandatory `klass` and `value`.

    Select segment ``'red'``::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.BackgroundElementSelector(specificationtools.Segment, 'red')
        BackgroundElementSelector(specificationtools.Segment, 'red')

    Select segment ``0``::

        >>> specificationtools.BackgroundElementSelector(specificationtools.Segment, 0)
        BackgroundElementSelector(specificationtools.Segment, 0)

    Select measure ``0``::

        >>> specificationtools.BackgroundElementSelector(measuretools.Measure, 0)
        BackgroundElementSelector(measuretools.Measure, 0)

    Select division ``0``::

        >>> specificationtools.BackgroundElementSelector(specificationtools.Division, 0)
        BackgroundElementSelector(specificationtools.Division, 0)

    More examples to follow.
    '''

    ### INITIALIZER ###
    
    def __init__(self, klass, value):
        from experimental import specificationtools
        assert specificationtools.is_background_element_klass(klass), repr(klass)
        assert isinstance(value, (int, str)), repr(value)
        Selector.__init__(self)
        self._klass = klass
        self._value = value

    ### SPECIAL METHODS ###

    def __repr__(self):
        klass = introspectiontools.klass_to_tools_package_qualified_klass_name(self.klass)
        return '{}({}, {!r})'.format(self._class_name, klass, self.value)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def klass(self):
        '''Background element selector class initialized by user.

        Return segment, measure or division class.
        '''
        return self._klass

    @property
    def value(self):
        '''Background element selector value initialized by user.

        Return integer or string.
        '''
        return self._value
