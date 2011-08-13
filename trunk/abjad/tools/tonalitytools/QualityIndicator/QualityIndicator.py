from abjad.core import _Immutable


class QualityIndicator(_Immutable):
    '''.. versionadded:: 2.0

    Indicator of chord quality, such as major, minor, dominant,
    diminished, etc.

    Value object that can not be changed after instantiation.
    '''

    def __init__(self, quality_string):
        if quality_string not in self._acceptable_quality_strings:
            raise ValueError('can not initialize quality indicator.')
        #self._quality_string = quality_string
        object.__setattr__(self, '_quality_string', quality_string)

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.quality_string == arg.quality_string:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.quality_string)

    ### PRIVATE ATTRIBUTES ###

    _acceptable_quality_strings = (
        'major', 'minor', 'augmented', 'diminished',
        'dominant', 'half diminished',
    )

    _uppercase_quality_strings = ('major', 'augmented', 'dominant')

    ### PUBLIC ATTRIBUTES ###

    @property
    def is_uppercase(self):
        return self.quality_string in self._uppercase_quality_strings

    @property
    def quality_string(self):
        return self._quality_string
