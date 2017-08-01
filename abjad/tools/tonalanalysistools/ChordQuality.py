# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class ChordQuality(AbjadValueObject):
    '''Chord quality.

    ::

        >>> from abjad.tools import tonalanalysistools

    ..  container:: example

        Initializes from string:

        ::

            >>> tonalanalysistools.ChordQuality('major')
            ChordQuality('major')

    ..  container:: example

        Initializes from other chord quality:

        ::

            >>> quality = tonalanalysistools.ChordQuality('major')
            >>> tonalanalysistools.ChordQuality(quality)
            ChordQuality('major')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_quality_string',
        )

    _acceptable_quality_strings = (
        'augmented',
        'diminished',
        'dominant',
        'half diminished',
        'major',
        'minor',
        )

    _uppercase_quality_strings = (
        'augmented',
        'dominant',
        'major',
        )

    ### INITIALIZER ###

    def __init__(self, quality_string='major'):
        quality_string = str(quality_string)
        if quality_string not in self._acceptable_quality_strings:
            message = 'can not initialize chord quality: {!r}.'
            message = message.format(quality_string)
            raise ValueError(message)
        self._quality_string = quality_string

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a chord quality with quality string
        equal to that of this chord quality. Otherwise false.

        ..  container:: example
    
            ::

                >>> quality_1 = tonalanalysistools.ChordQuality('major')
                >>> quality_2 = tonalanalysistools.ChordQuality('major')
                >>> quality_3 = tonalanalysistools.ChordQuality('dominant')

            ::

                >>> quality_1 == quality_1
                True
                >>> quality_1 == quality_2
                True
                >>> quality_1 == quality_3
                False

            ::

                >>> quality_2 == quality_1
                True
                >>> quality_2 == quality_2
                True
                >>> quality_2 == quality_3
                False

            ::

                >>> quality_3 == quality_1
                False
                >>> quality_3 == quality_2
                False
                >>> quality_3 == quality_3
                True

        Returns true or false.
        '''
        return super(ChordQuality, self).__eq__(argument)

    def __hash__(self):
        r'''Hashes chord quality.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(ChordQuality, self).__hash__()

    def __str__(self):
        r'''Gets string representation of chord quality.

        ..  container:: example

            ::

                >>> quality = tonalanalysistools.ChordQuality('major')
                >>> str(quality)
                'major'

        Returns string.
        '''
        return self.quality_string

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        values = [self.quality_string]
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def is_uppercase(self):
        r'''Is true when chord quality is uppercase. Otherwise false.

        ..  container:: example

            ::

                >>> tonalanalysistools.ChordQuality('major').is_uppercase
                True

            ::

                >>> tonalanalysistools.ChordQuality('minor').is_uppercase
                False

        Returns true or false.
        '''
        return self.quality_string in self._uppercase_quality_strings

    @property
    def quality_string(self):
        r'''Gets quality string.

        ..  container:: example

            ::

                >>> tonalanalysistools.ChordQuality('major').quality_string
                'major'

            ::

                >>> tonalanalysistools.ChordQuality('minor').quality_string
                'minor'

        Returns string.
        '''
        return self._quality_string
