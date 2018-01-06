from abjad.tools.abctools.AbjadObject import AbjadObject


class Line(AbjadObject):
    r'''Line in a LilyPond file.

    ..  container:: example

        >>> string = '    %@%  \with-color %! MEASURE_NUMBER_MARKUP:SM31'
        >>> abjad.Line(string)
        Line(string='    %@%  \\with-color %! MEASURE_NUMBER_MARKUP:SM31')

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segment-makers'

    __slots__ = (
        '_string',
        )

    ### INITIALIZER ###

    def __init__(self, string=''):
        assert isinstance(string, str), repr(string)
        self._string = string

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of line.

        ..  container:: example

            >>> string = '    %@%  \with-color %! MEASURE_NUMBER_MARKUP:SM31'
            >>> str(abjad.Line(string))
            '    %@%  \\with-color %! MEASURE_NUMBER_MARKUP:SM31'

        Returns string.
        '''
        return self.string

    ### PUBLIC PROPERTIES ###

    @property
    def string(self):
        r'''Gets string.

        ..  container:: example

            >>> string = '    %@%  \with-color %! MEASURE_NUMBER_MARKUP:SM31'
            >>> abjad.Line(string).string
            '    %@%  \\with-color %! MEASURE_NUMBER_MARKUP:SM31'

        Returns string.
        '''
        return self._string

    ### PUBLIC METHODS ###

    def get_tags(self):
        r'''Gets tags.

        ..  container:: example

            >>> string = '    %@%  \with-color %! MEASURE_NUMBER_MARKUP:SM31'
            >>> abjad.Line(string).get_tags()
            ['MEASURE_NUMBER_MARKUP', 'SM31']

        Returns list of zero or more strings.
        '''
        tags = []
        if ' %! ' in self.string:
            index = self.string.find('%! ')
            string = self.string[index+2:].strip()
            parts = string.split()
            tags.extend(parts[0].split(':'))
        return tags

    def match(self, predicate):
        r'''Is true when `predicate` matches tags.

        ..  container:: example

            >>> string = '    %@%  \with-color %! MEASURE_NUMBER_MARKUP:SM31'
            >>> line = abjad.Line(string)

        ..  container:: example

            Strings:

            >>> line.match('MEASURE_NUMBER_MARKUP')
            True

            >>> line.match('SM31')
            True

            >>> line.match(['MEASURE_NUMBER_MARKUP', 'SM31'])
            False

            >>> line.match('%@%')
            False

            >>> line.match('with-color')
            False

            >>> line.match('%!')
            False

        ..  container:: example

            Lambdas:

            >>> line.match(lambda x: any(_ for _ in x if _.startswith('M')))
            True

            >>> line.match(lambda x: any(_ for _ in x if _.startswith('S')))
            True

            >>> line.match(lambda x: any(_ for _ in x if _[0] in 'SM'))
            True

        ..  container:: example

            Functions:

            >>> def predicate(tags):
            ...     if 'SM31' in tags and 'MEASURE_NUMBER_MARKUP' in tags:
            ...         return True
            ...     else:
            ...         return False

            >>> line.match(predicate)
            True

            >>> def predicate(tags):
            ...     if 'SM31' in tags and 'MEASURE_NUMBER_MARKUP' not in tags:
            ...         return True
            ...     else:
            ...         return False

            >>> line.match(predicate)
            False

        Returns true or false.
        '''
        tags = self.get_tags()
        if not tags:
            return False
        if predicate in tags:
            return True
        if not callable(predicate):
            return False
        return predicate(tags)
