from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.system.Tag import Tag


class Line(object):
    r"""
    Line in a LilyPond file.

    ..  container:: example

        >>> string = r'    %@%  \with-color %! MEASURE_NUMBER:SM31'
        >>> abjad.Line(string)
        Line(string='    %@%  \\with-color %! MEASURE_NUMBER:SM31')

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Segment-makers"

    __slots__ = ("_string",)

    ### INITIALIZER ###

    def __init__(self, string=""):
        assert isinstance(string, str), repr(string)
        self._string = string

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        r"""
        Gets string representation of line.

        ..  container:: example

            >>> string = r'    %@%  \with-color %! MEASURE_NUMBER:SM31'
            >>> str(abjad.Line(string))
            '    %@%  \\with-color %! MEASURE_NUMBER:SM31'

        Returns string.
        """
        return self.string

    ### PUBLIC PROPERTIES ###

    @property
    def string(self):
        r"""
        Gets string.

        ..  container:: example

            >>> string = r'    %@%  \with-color %! MEASURE_NUMBER:SM31'
            >>> abjad.Line(string).string
            '    %@%  \\with-color %! MEASURE_NUMBER:SM31'

        Returns string.
        """
        return self._string

    ### PUBLIC METHODS ###

    def get_tags(self):
        r"""
        Gets tags.

        ..  container:: example

            >>> string = r'    %@%  \with-color %! MEASURE_NUMBER:SM31'
            >>> abjad.Line(string).get_tags()
            [Tag('MEASURE_NUMBER'), Tag('SM31')]

        ..  container:: example

            REGRESSION. Works with multiple ``%!`` prefixes:

            >>> string = r'    %@%  \with-color %! SM31 %! SM32'
            >>> line = abjad.Line(string)
            >>> line.get_tags()
            [Tag('SM31'), Tag('SM32')]

        Returns list of zero or more strings.
        """
        tags = []
        if " %! " in self.string:
            for chunk in self.string.split(" %! ")[1:]:
                parts = chunk.split()
                parts = parts[0].split(":")
                tags_ = [Tag(_) for _ in parts]
                tags.extend(tags_)
        return tags

    def is_active(self):
        r"""
        Is true when line is active.

        ..  container:: example

            >>> string = '              \\clef "treble" %! EXPLICT_CLEF'
            >>> abjad.Line(string).is_active()
            True

            >>> string = '          %@% \\clef "treble" %! EXPLICT_CLEF'
            >>> abjad.Line(string).is_active()
            False

            >>> string = '          %%% \\clef "treble" %! EXPLICT_CLEF'
            >>> abjad.Line(string).is_active()
            False

        Returns true or false.
        """
        return not self.is_deactivated()

    def is_deactivated(self):
        r"""
        Is true when line is deactivated.

        ..  container:: example

            >>> string = '              \\clef "treble" %! EXPLICT_CLEF'
            >>> abjad.Line(string).is_deactivated()
            False

            >>> string = '          %@% \\clef "treble" %! EXPLICT_CLEF'
            >>> abjad.Line(string).is_deactivated()
            True

            >>> string = '          %%% \\clef "treble" %! EXPLICT_CLEF'
            >>> abjad.Line(string).is_deactivated()
            True

        Returns true or false.
        """
        string = self.string.strip()
        if string.startswith("%@%"):
            return True
        if string.startswith("%%%"):
            return True
        return False

    def match(self, predicate):
        r"""
        Is true when ``predicate`` matches tags.

        ..  container:: example

            >>> string = r'    %@%  \with-color %! MEASURE_NUMBER:SM31'
            >>> line = abjad.Line(string)

        ..  container:: example

            Tags:

            >>> line.match(abjad.Tag('MEASURE_NUMBER'))
            True

            >>> line.match(abjad.Tag('SM31'))
            True

            >>> line.match(abjad.Tag('%@%'))
            False

            >>> line.match(abjad.Tag('with-color'))
            False

            >>> line.match(abjad.Tag('%!'))
            False

        ..  container:: example

            Lambdas:

            >>> line.match(lambda x: any(_ for _ in x if str(_).startswith('M')))
            True

            >>> line.match(lambda x: any(_ for _ in x if str(_).startswith('S')))
            True

            >>> line.match(lambda x: any(_ for _ in x if str(_)[0] in 'SM'))
            True

        ..  container:: example

            Functions:

            >>> def predicate(tags):
            ...     if abjad.Tag('SM31') in tags and abjad.Tag('MEASURE_NUMBER') in tags:
            ...         return True
            ...     else:
            ...         return False

            >>> line.match(predicate)
            True

            >>> def predicate(tags):
            ...     if abjad.Tag('SM31') in tags and abjad.Tag('MEASURE_NUMBER') not in tags:
            ...         return True
            ...     else:
            ...         return False

            >>> line.match(predicate)
            False

        ..  container:: example

            REGRESSION. Works with multiple ``%!`` prefixes:

            >>> string = r'    %@%  \with-color %! SM31 %! SM32'
            >>> line = abjad.Line(string)

            >>> line.match(abjad.Tag('SM31'))
            True

            >>> line.match(abjad.Tag('SM32'))
            True

        Returns true or false.
        """
        if not callable(predicate) and not isinstance(predicate, Tag):
            message = f"must be callable or tag: {predicate!r}"
            raise Exception(message)
        tags = self.get_tags()
        if not tags:
            return False
        if predicate in tags:
            return True
        if not callable(predicate):
            return False
        return predicate(tags)
