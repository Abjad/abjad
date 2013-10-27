# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class QualityIndicator(AbjadObject):
    '''An indicator of chord quality, such as major, minor, dominant,
    diminished, etc.

    Value object that can not be changed after instantiation.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_quality_string',
        )

    _default_positional_input_arguments = (
        repr('dominant'),
        )

    ### INITIALIZER ###

    def __init__(self, quality_string):
        if quality_string not in self._acceptable_quality_strings:
            raise ValueError('can not initialize quality indicator.')
        self._quality_string = quality_string

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.quality_string == arg.quality_string:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '{}({})'.format(self._class_name, self.quality_string)

    ### PRIVATE PROPERTIES ###

    _acceptable_quality_strings = (
        'major', 'minor', 'augmented', 'diminished',
        'dominant', 'half diminished',
    )

    _uppercase_quality_strings = (
        'major',
        'augmented',
        'dominant',
        )

    ### PUBLIC PROPERTIES ###

    @property
    def is_uppercase(self):
        return self.quality_string in self._uppercase_quality_strings

    @property
    def quality_string(self):
        return self._quality_string
