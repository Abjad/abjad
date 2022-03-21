import dataclasses
import typing

from . import tag as _tag


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Tweak:
    """
    Tweak.
    """

    string: str
    tag: _tag.Tag | None = None

    def __post_init__(self):
        assert isinstance(self.string, str), repr(self.string)
        if self.tag is not None:
            assert isinstance(self.tag, _tag.Tag), repr(self.tag)
        self._parse()

    def _list_contributions(self):
        result = []
        deactivate = False
        strings = [self.string]
        if self.tag is not None:
            strings = _tag.double_tag(strings, self.tag, deactivate=deactivate)
        result.extend(strings)
        return result

    def _parse(self):
        parts = self.string.split()
        post_event = False
        if parts[0] == "-":
            post_event = True
            parts.pop(0)
        assert parts[0] == r"\tweak", repr(self.string)
        parts.pop(0)
        attribute = parts[0]
        parts.pop(0)
        value = " ".join(parts)
        return post_event, attribute, value

    def attribute(self) -> str:
        post_event, attribute, value = self._parse()
        return attribute

    def post_event(self) -> bool:
        post_event, attribute, value = self._parse()
        return post_event

    def value(self) -> str:
        post_event, attribute, value = self._parse()
        return value


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Bundle:
    """
    Bundled indicator.
    """

    indicator: typing.Any
    tweaks: tuple[Tweak, ...] = dataclasses.field(default_factory=tuple)

    def __post_init__(self):
        assert isinstance(self.tweaks, tuple), repr(self.tweaks)
        assert all(isinstance(_, Tweak) for _ in self.tweaks)

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = self.indicator._get_contributions(
            component=component, wrapper=wrapper
        )
        lists = contributions.get_contribution_lists()
        assert len(lists) == 1, repr(lists)
        for list_ in lists:
            prefix = list_[0][0]
            if prefix in ("-", "_", "^"):
                strings = [prefix + " " + _.string for _ in self.tweaks]
            else:
                strings = [_.string for _ in self.tweaks]
            list_[0:0] = strings
        return contributions


def bundle(indicator: typing.Any, *tweaks: str) -> Bundle:
    r"""
    Bundles ``indicator`` with ``tweaks``.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> bundle = abjad.bundle(
        ...     abjad.Articulation("."),
        ...     r"\tweak color #red",
        ... )
        >>> abjad.attach(bundle, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                - \staccato
                d'4
                e'4
                f'4
            }

    """
    tweaks_ = tuple([Tweak(_) for _ in tweaks])
    return Bundle(indicator, tweaks=tweaks_)


def tweak(
    indicator: typing.Any,
    *tweaks: str | Tweak,
    overwrite: bool = False,
    tag: _tag.Tag = None,
) -> None:
    r"""
    Appends ``tweaks`` to ``indicator``.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> articulation = abjad.Articulation(".")
        >>> abjad.tweak(
        ...     articulation,
        ...     r"- \tweak color #red",
        ... )
        >>> abjad.attach(articulation, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                - \staccato
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Raises exception on conflicting tweaks:

        >>> articulation = abjad.Articulation(".")
        >>> abjad.tweak(
        ...     articulation,
        ...     r"- \tweak color #red",
        ...     r"- \tweak color #blue",
        ... )
        Traceback (most recent call last):
            ...
        Exception: conflicting tweaks:
            - \tweak color #red
            - \tweak color #blue

        Raises exception on conflicting tweaks:

        >>> articulation = abjad.Articulation(".")
        >>> abjad.tweak(
        ...     articulation,
        ...     r"- \tweak color #red",
        ... )
        >>> abjad.tweak(
        ...     articulation,
        ...     r"- \tweak color #blue",
        ... )
        Traceback (most recent call last):
            ...
        Exception: conflicting tweaks:
            - \tweak color #red
            - \tweak color #blue

    """
    try:
        tweaks_ = list(indicator.tweaks)
    except AttributeError:
        raise Exception(indicator)
    if tag is not None:
        assert isinstance(tag, _tag.Tag), repr(tag)
    for item in tweaks:
        duplicate = False
        if isinstance(item, Tweak):
            tweak = item
            if tag is not None:
                tweak = Tweak(tweak.string, tag=tag)
        else:
            assert isinstance(item, str), repr(item)
            if getattr(indicator, "post_event", False) and not item.startswith("-"):
                name = type(indicator).__name__
                message = (
                    f"Must prefix {name} (LilyPond 'post-event') tweak with hyphen."
                )
                raise Exception(message)
            if item.startswith("-") and not getattr(indicator, "post_event", False):
                name = type(indicator).__name__
                message = f"Must not prefix {name} tweak with hyphen."
                raise Exception(message)
            tweak = Tweak(item, tag=tag)
        for existing_tweak in tweaks_[:]:
            if existing_tweak == tweak:
                duplicate = True
                continue
            if existing_tweak.attribute() == tweak.attribute():
                if overwrite is True:
                    tweaks_.remove(existing_tweak)
                else:
                    message = "conflicting tweaks:\n"
                    message += f"    {existing_tweak.string}\n"
                    message += f"    {tweak.string}"
                    raise Exception(message)
        if not duplicate:
            tweaks_.append(tweak)
    tweaks_.sort()
    indicator.tweaks = tuple(tweaks_)
