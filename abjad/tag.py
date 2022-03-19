import dataclasses
import typing

from . import _indent


class Tag:
    """
    Tag.

    ..  container:: example

        >>> abjad.Tag("YELLOW")
        Tag('YELLOW')

        >>> abjad.Tag("YELLOW:RED")
        Tag('YELLOW:RED')

        Removes duplicate words at initialization:

        >>> abjad.Tag("YELLOW:RED:RED")
        Tag('YELLOW:RED')

    ..  container:: example

        Raises exception on multiple only-edition tags:

        >>> abjad.Tag("+SEGMENT:+PARTS")
        Traceback (most recent call last):
            ...
        Exception: at most one only-edition tag: ['+SEGMENT', '+PARTS'].

    ..  container:: example

        Raises exception on mixed only-edition / not-edition tags:

        >>> abjad.Tag("+SEGMENT:-PARTS")
        Traceback (most recent call last):
        ...
        Exception: only-edition and not-edition forbidden in same tag:
        <BLANKLINE>
          ['+SEGMENT'] / ['-PARTS']

    """

    __slots__ = ("_string", "_words")

    def __init__(self, string: str = "") -> None:
        assert isinstance(string, str), repr(string)
        assert not string.startswith(":"), repr(string)
        words = string.split(":")
        assert isinstance(words, list), repr(words)
        words_: list[str] = []
        for word in words:
            if word not in words_:
                words_.append(word)
        only_edition_tags, not_edition_tags = [], []
        for word_ in words_:
            if word_.startswith("+"):
                only_edition_tags.append(word_)
            if word_.startswith("-"):
                not_edition_tags.append(word_)
        if 1 < len(only_edition_tags):
            raise Exception(f"at most one only-edition tag: {only_edition_tags!r}.")
        if only_edition_tags and not_edition_tags:
            message = "only-edition and not-edition forbidden in same tag:\n\n"
            message += f"  {only_edition_tags} / {not_edition_tags}"
            raise Exception(message)
        self._words = words_
        if bool(string):
            string = ":".join(words_)
            assert not string.startswith(":"), repr(string)
        else:
            string = ""
        self._string = string

    def __bool__(self):
        """
        Is true when tag has words.

        ..  container:: example

            >>> bool(abjad.Tag())
            False

            >>> bool(abjad.Tag("+PARTS"))
            True

        """
        return bool(self.string)

    def __contains__(self, argument) -> bool:
        """
        Is true when ``argument`` is word in tag.

        ..  container:: example

            >>> tag = abjad.Tag("-PARTS")
            >>> tag = tag.append(abjad.Tag("DEFAULT_CLEF"))

            >>> "PARTS" in tag
            False

            >>> "-PARTS" in tag
            True

            >>> abjad.Tag("DEFAULT_CLEF") in tag
            True

        """
        if isinstance(argument, str):
            return argument in self.words
        else:
            return argument.string in self.words

    def __eq__(self, argument):
        """
        Is true when ``argument`` is tag with same string representation.

        ..  container:: example

            >>> tag_1 = abjad.Tag()
            >>> tag_2 = abjad.Tag()
            >>> tag_3 = abjad.Tag("+PARTS")

            >>> tag_1 == tag_1
            True
            >>> tag_1 == tag_2
            True
            >>> tag_1 == tag_3
            False

            >>> tag_2 == tag_1
            True
            >>> tag_2 == tag_2
            True
            >>> tag_2 == tag_3
            False

            >>> tag_3 == tag_1
            False
            >>> tag_3 == tag_2
            False
            >>> tag_3 == tag_3
            True

        """
        if isinstance(argument, Tag):
            return self.string == argument.string
        return False

    def __hash__(self):
        """
        Hashes tag.

        ..  container:: example

            REGRESSION. Tags compare equal when strings compare equal:

            >>> tag_1 = abjad.Tag("MEASURE_1")
            >>> tag_2 = abjad.Tag("MEASURE_1")
            >>> hash(tag_1) == hash(tag_2)
            True

        """
        return hash(self.__class__.__name__ + self.string)

    def __iter__(self):
        """
        Iterates words in tag.

        ..  container:: example

            >>> tag = abjad.Tag("-PARTS:-SCORE:DEFAULT_CLEF")
            >>> for word  in tag:
            ...     word
            ...
            '-PARTS'
            '-SCORE'
            'DEFAULT_CLEF'

        """
        return iter(self.words)

    def __repr__(self):
        """
        Gets repr.
        """
        if self.string is None:
            return f"{type(self).__name__}()"
        else:
            return f"{type(self).__name__}({self.string!r})"

    @property
    def string(self) -> str:
        """
        Gets string.

        ..  container:: example

            >>> abjad.Tag().string
            ''

            >>> abjad.Tag("-PARTS:DEFAULT_CLEF").string
            '-PARTS:DEFAULT_CLEF'

        """
        return self._string

    @property
    def words(self) -> list[str]:
        """
        Gets words.

        ..  container:: example

            >>> abjad.Tag("-PARTS:DEFAULT_CLEF").words
            ['-PARTS', 'DEFAULT_CLEF']

        """
        return list(self._words)

    def append(self, word: typing.Optional["Tag"]) -> "Tag":
        """
        Appends ``word`` to tag.

        ..  container:: example

            >>> abjad.Tag("-PARTS").append(abjad.Tag("DEFAULT_CLEF"))
            Tag('-PARTS:DEFAULT_CLEF')

        """
        if not bool(word):
            return Tag(self.string)
        assert isinstance(word, Tag), repr(word)
        words = []
        if self.string:
            words.append(self.string)
        words.append(word.string)
        string = ":".join(words)
        return Tag(string)

    def editions(self) -> list["Tag"]:
        """
        Gets edition tags in tag.

        ..  container:: example

            >>> abjad.Tag("FOO").editions()
            []

            >>> abjad.Tag("+SEGMENT").only_edition()
            Tag('+SEGMENT')

            >>> abjad.Tag("+SEGMENT:FOO").only_edition()
            Tag('+SEGMENT')

            >>> abjad.Tag("-SEGMENT").editions()
            [Tag('-SEGMENT')]

            >>> abjad.Tag("-SEGMENT:FOO").editions()
            [Tag('-SEGMENT')]

            >>> abjad.Tag("-SEGMENT:-PARTS").editions()
            [Tag('-SEGMENT'), Tag('-PARTS')]

        """
        result = []
        for word in self:
            if word.startswith("+") or word.startswith("-"):
                result.append(Tag(word))
        return result

    def invert_edition_tags(self) -> "Tag":
        """
        Inverts edition tags in tag.

        ..  container:: example

            >>> abjad.Tag("FOO").invert_edition_tags()
            Tag('FOO')

            >>> abjad.Tag("FOO:-PARTS").invert_edition_tags()
            Tag('FOO:+PARTS')

            >>> abjad.Tag("FOO:+PARTS").invert_edition_tags()
            Tag('FOO:-PARTS')

        """
        words = []
        for word in self.words:
            if word.startswith("+"):
                word_ = "-" + word[1:]
            elif word.startswith("-"):
                word_ = "+" + word[1:]
            else:
                word_ = word
            words.append(word_)
        string = ":".join(words)
        tag = Tag(string)
        return tag

    def not_editions(self) -> list["Tag"]:
        """
        Gets not-edition tags in tag.

        ..  container:: example

            >>> abjad.Tag("FOO").not_editions()
            []

            >>> abjad.Tag("-SEGMENT").not_editions()
            [Tag('-SEGMENT')]

            >>> abjad.Tag("-SEGMENT:FOO").not_editions()
            [Tag('-SEGMENT')]

            >>> abjad.Tag("-SEGMENT:-PARTS").not_editions()
            [Tag('-SEGMENT'), Tag('-PARTS')]

        """
        result = []
        for word in self:
            if word.startswith("-"):
                result.append(Tag(word))
        return result

    def only_edition(self) -> typing.Optional["Tag"]:
        """
        Gets only-edition tag in tag.

        ..  container:: example

            >>> abjad.Tag("FOO").only_edition() is None
            True

            >>> abjad.Tag("+SEGMENT").only_edition()
            Tag('+SEGMENT')

            >>> abjad.Tag("+SEGMENT:FOO").only_edition()
            Tag('+SEGMENT')

        """
        for word in self:
            if word.startswith("+"):
                return Tag(word)
        else:
            return None


@dataclasses.dataclass(slots=True)
class Line:
    r"""
    Line in a LilyPond file.

    ..  container:: example

        >>> string = r"    %@%  \with-color %! MEASURE_NUMBER:SM31"
        >>> abjad.Line(string)
        Line(string='    %@%  \\with-color %! MEASURE_NUMBER:SM31')

    """

    string: str

    def get_tags(self):
        r"""
        Gets tags.

        ..  container:: example

            >>> string = r"    %@%  \with-color %! MEASURE_NUMBER:SM31"
            >>> abjad.Line(string).get_tags()
            [Tag('MEASURE_NUMBER'), Tag('SM31')]

        ..  container:: example

            REGRESSION. Works with multiple ``%!`` prefixes:

            >>> string = r"    %@%  \with-color %! SM31 %! SM32"
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

            >>> string = r"    %@%  \with-color %! MEASURE_NUMBER:SM31"
            >>> line = abjad.Line(string)

        ..  container:: example

            Tags:

            >>> line.match(abjad.Tag("MEASURE_NUMBER"))
            True

            >>> line.match(abjad.Tag("SM31"))
            True

            >>> line.match(abjad.Tag("%@%"))
            False

            >>> line.match(abjad.Tag("with-color"))
            False

            >>> line.match(abjad.Tag("%!"))
            False

        ..  container:: example

            Lambdas:

            >>> line.match(lambda x: any(_ for _ in x if _.string.startswith("M")))
            True

            >>> line.match(lambda x: any(_ for _ in x if _.string.startswith("S")))
            True

            >>> line.match(lambda x: any(_ for _ in x if _.string[0] in "SM"))
            True

        ..  container:: example

            Functions:

            >>> def predicate(tags):
            ...     if abjad.Tag("SM31") in tags and abjad.Tag("MEASURE_NUMBER") in tags:
            ...         return True
            ...     else:
            ...         return False

            >>> line.match(predicate)
            True

            >>> def predicate(tags):
            ...     if abjad.Tag("SM31") in tags and abjad.Tag("MEASURE_NUMBER") not in tags:
            ...         return True
            ...     else:
            ...         return False

            >>> line.match(predicate)
            False

        ..  container:: example

            REGRESSION. Works with multiple ``%!`` prefixes:

            >>> string = r"    %@%  \with-color %! SM31 %! SM32"
            >>> line = abjad.Line(string)

            >>> line.match(abjad.Tag("SM31"))
            True

            >>> line.match(abjad.Tag("SM32"))
            True

        Returns true or false.
        """
        if not callable(predicate) and not isinstance(predicate, Tag):
            raise Exception(f"must be callable or tag: {predicate!r}")
        tags = self.get_tags()
        if not tags:
            return False
        if predicate in tags:
            return True
        if not callable(predicate):
            return False
        return predicate(tags)


def _match_line(line, tag, current_tags):
    if tag in current_tags:
        return True
    if callable(tag):
        return tag(current_tags)
    return False


def activate(text, tag, skipped=False):
    r"""
    Activates ``tag`` in ``text``.

    ..  container:: example

        Writes (deactivated) tag with ``"%@%"`` prefix into LilyPond
        input:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> string = r"\markup { \with-color #red Allegro }"
        >>> markup = abjad.Markup(string)
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.Tag("RED_MARKUP"),
        ... )

        >>> text = abjad.lilypond(staff, tags=True)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
            %@% - \markup { \with-color #red Allegro }
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

        Activates tag:

        >>> text, count = abjad.activate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
                - \markup { \with-color #red Allegro } %@%
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile([string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Deactivates tag again:

        >>> text, count = abjad.deactivate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
            %@% - \markup { \with-color #red Allegro }
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile([string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Activates tag again:

        >>> text, count = abjad.activate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
                - \markup { \with-color #red Allegro } %@%
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile([string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    Tags can toggle indefinitely.

    Returns text, count pair.

    Count gives number of activated tags.
    """
    assert isinstance(tag, Tag) or callable(tag), repr(tag)
    lines, count, skipped_count = [], 0, 0
    treated_last_line = False
    found_already_active_on_last_line = False
    text_lines = text.split("\n")
    text_lines = [_ + "\n" for _ in text_lines[:-1]] + text_lines[-1:]
    lines = []
    current_tags = []
    for line in text_lines:
        if line.lstrip().startswith("%! "):
            lines.append(line)
            current_tag = Tag(line.strip()[3:])
            current_tags.append(current_tag)
            continue
        if not _match_line(line, tag, current_tags):
            lines.append(line)
            treated_last_line = False
            found_already_active_on_last_line = False
            current_tags = []
            continue
        first_nonwhitespace_index = len(line) - len(line.lstrip())
        index = first_nonwhitespace_index
        if line[index : index + 4] in ("%%% ", "%@% "):
            if "%@% " in line:
                line = line.replace("%@%", "   ")
                suffix = " %@%"
            else:
                line = line.replace("%%%", "   ")
                suffix = None
            assert line.endswith("\n"), repr(line)
            if suffix:
                line = line.strip("\n") + suffix + "\n"
            if not treated_last_line:
                count += 1
            treated_last_line = True
            found_already_active_on_last_line = False
        else:
            if not found_already_active_on_last_line:
                skipped_count += 1
            found_already_active_on_last_line = True
            treated_last_line = False
        lines.append(line)
        current_tags = []
    text = "".join(lines)
    if skipped is True:
        return text, count, skipped_count
    else:
        return text, count


def deactivate(text, tag, prepend_empty_chord=False, skipped=False):
    r"""
    Deactivates ``tag`` in ``text``.

    ..  container:: example

        Writes (active) tag into LilyPond input:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> string = r"\markup { \with-color #red Allegro }"
        >>> markup = abjad.Markup(string)
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     tag=abjad.Tag("RED_MARKUP"),
        ... )

        >>> text = abjad.lilypond(staff, tags=True)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
            - \markup { \with-color #red Allegro }
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

        Deactivates tag:

        >>> text = abjad.lilypond(staff, tags=True)
        >>> text, count = abjad.deactivate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
        %%% - \markup { \with-color #red Allegro }
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile([string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Activates tag again:

        >>> text, count = abjad.activate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
            - \markup { \with-color #red Allegro }
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile([string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Deactivates tag again:

        >>> text, count = abjad.deactivate(text, abjad.Tag("RED_MARKUP"))
        >>> print(text)
        \new Staff
        {
            c'4
            %! RED_MARKUP
        %%% - \markup { \with-color #red Allegro }
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip("\n") for _ in text.split("\n")]
        >>> string = "\n".join(lines)
        >>> lilypond_file = abjad.LilyPondFile([string])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    Tags can toggle indefinitely.

    Returns text, count pair.

    Count gives number of deactivated tags.
    """
    assert isinstance(tag, Tag) or callable(tag), repr(tag)
    lines, count, skipped_count = [], 0, 0
    treated_last_line, last_index = False, None
    found_already_deactivated_on_last_line = False
    text_lines = text.split("\n")
    text_lines = [_ + "\n" for _ in text_lines[:-1]] + text_lines[-1:]
    lines = []
    previous_line_was_tweak = False
    current_tags = []
    for line in text_lines:
        if line.lstrip().startswith("%! "):
            lines.append(line)
            current_tag = Tag(line.strip()[3:])
            current_tags.append(current_tag)
            continue
        if not _match_line(line, tag, current_tags):
            lines.append(line)
            treated_last_line, last_index = False, None
            found_already_deactivated_on_last_line = False
            current_tags = []
            continue
        first_nonwhitespace_index = len(line) - len(line.lstrip())
        index = first_nonwhitespace_index
        if line[index] != "%":
            if last_index is None:
                last_index = index
            if " %@%" in line:
                prefix = "%@% "
                line = line.replace(" %@%", "")
            else:
                prefix = "%%% "
            if prepend_empty_chord and not previous_line_was_tweak:
                prefix += "<> "
            target = line[last_index - 4 : last_index]
            assert target == "    ", repr((line, target, index, tag))
            characters = list(line)
            characters[last_index - 4 : last_index] = list(prefix)
            line = "".join(characters)
            if not treated_last_line:
                count += 1
            treated_last_line = True
            found_already_deactivated_on_last_line = False
        else:
            if not found_already_deactivated_on_last_line:
                skipped_count += 1
            found_already_deactivated_on_last_line = True
            treated_last_line = False
        lines.append(line)
        previous_line_was_tweak = "tweak" in line
        current_tags = []
    text = "".join(lines)
    if skipped is True:
        return text, count, skipped_count
    else:
        return text, count


def double_tag(strings, tag_, deactivate=None):
    """
    Double tags ``strings``.
    """
    assert isinstance(tag_, Tag), repr(tag_)
    before_tags = []
    if tag_:
        line = tag_.string
        lines = line.split(":")
        lines = ["%! " + _ for _ in lines]
        before_tags.extend(lines)
    right_tagged_lines = strings
    if deactivate is True:
        right_tagged_lines = ["%@% " + _ for _ in right_tagged_lines]
    result = []
    for right_tagged_line in right_tagged_lines:
        if right_tagged_line.strip().startswith("%!"):
            result.append(right_tagged_line)
            continue
        result.extend(before_tags)
        result.append(right_tagged_line)
    return result


def left_shift_tags(text, realign=None) -> str:
    """
    Left shifts tags in ``strings`` and realigns to column ``realign``.
    """
    strings = text.split("\n")
    strings_ = []
    for string in strings:
        if "%@% " not in string or "%!" not in string:
            strings_.append(string)
            continue
        if not string.startswith(4 * " "):
            strings_.append(string)
            continue
        string_ = string[4:]
        tag_start = string_.find("%!")
        string_ = list(string_)
        string_[tag_start:tag_start] = _indent.INDENT
        string_ = "".join(string_)
        strings_.append(string_)
    text = "\n".join(strings_)
    return text


def remove_tags(string) -> str:
    """
    Removes all tags from ``string``.
    """
    lines = []
    for line in string.split("\n"):
        if "%!" not in line:
            lines.append(line)
            continue
        tag_start = line.find("%!")
        line = line[:tag_start]
        line = line.rstrip()
        if line:
            lines.append(line)
    string = "\n".join(lines)
    return string
