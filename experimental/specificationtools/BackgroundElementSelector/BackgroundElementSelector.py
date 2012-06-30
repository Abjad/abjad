from abjad.tools.abctools.AbjadObject import AbjadObject


class BackgroundElementSelector(AbjadObject):
    r'''.. versionadded:: 1.0

    Select one background object with mandatory `klass` and `value`.

    Select segment ``'red'``::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.BackgroundElementSelector(specificationtools.SegmentSpecification, 'red')
        BackgroundElementSelector(<class 'experimental.specificationtools.SegmentSpecification.SegmentSpecification.SegmentSpecification'>, 'red')

    .. note:: something will have to be done about repr class display.
    '''

    ### INITIALIZER ###
    
    def __init__(self, klass, value):
        from experimental import specificationtools
        assert specificationtools.is_background_element_klass(klass), repr(klass)
        assert isinstance(value, (int, str)), repr(value)
        self._klass = klass
        self._value = value

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
