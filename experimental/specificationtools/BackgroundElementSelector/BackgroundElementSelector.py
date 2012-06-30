from abjad.tools.abctools.AbjadObject import AbjadObject


class BackgroundElementSelector(AbjadObject):
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
        self._klass = klass
        self._value = value

    ### SPECIAL METHODS ###

    def __repr__(self):
        module_parts = self.klass.__module__.split('.')
        qualified_class_name = '.'.join(module_parts[-3:-1])
        return '{}({}, {!r})'.format(self._class_name, qualified_class_name, self.value)

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
