# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class ChordExtent(AbjadValueObject):
    '''Chord extent.

    ::

        >>> from abjad.tools import tonalanalysistools

    ..  container:: example

        Initializes from number:

        ::

            >>> tonalanalysistools.ChordExtent(7)
            ChordExtent(7)

    ..  container:: example

        Initializes from other chord extent:

        ::

            >>> extent = tonalanalysistools.ChordExtent(7)
            >>> tonalanalysistools.ChordExtent(extent)
            ChordExtent(7)

    Defined equal to outer interval of any root-position chord.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    _acceptable_number = (
        5,
        7,
        9,
        )

    _extent_number_to_extent_name = {
        5: 'triad',
        7: 'seventh',
        9: 'ninth',
        }

    ### INITIALIZER ###

    def __init__(self, number=5):
        if isinstance(number, int):
            if number not in self._acceptable_number:
                message = 'can not initialize extent: {}.'
                raise ValueError(message.format(number))
            number = number
        elif isinstance(number, type(self)):
            number = number.number
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a chord extent with number equal to that of
        this chord extent. Otherwise false.

        ..  container:: example

            ::

                >>> extent_1 = tonalanalysistools.ChordExtent(5)
                >>> extent_2 = tonalanalysistools.ChordExtent(5)
                >>> extent_3 = tonalanalysistools.ChordExtent(7)

            ::

                >>> extent_1 == extent_1
                True
                >>> extent_1 == extent_2
                True
                >>> extent_1 == extent_3
                False

            ::

                >>> extent_2 == extent_1
                True
                >>> extent_2 == extent_2
                True
                >>> extent_2 == extent_3
                False

            ::

                >>> extent_3 == extent_1
                False
                >>> extent_3 == extent_2
                False
                >>> extent_3 == extent_3
                True

        Returns true or false.
        '''
        return super(ChordExtent, self).__eq__(argument)

    def __hash__(self):
        r'''Hashes chord extent.

        Returns integer.
        '''
        return super(ChordExtent, self).__hash__()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        values = [self.number]
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        r'''Gets name.

        ..  container:: example

            ::

                >>> tonalanalysistools.ChordExtent(5).name
                'triad'

            ::

                >>> tonalanalysistools.ChordExtent(7).name
                'seventh'

        Returns string.
        '''
        return self._extent_number_to_extent_name[self.number]

    @property
    def number(self):
        r'''Gets number.

        ..  container:: example

            ::

                >>> tonalanalysistools.ChordExtent(7).number
                7

        Returns nonnegative integer.
        '''
        return self._number
