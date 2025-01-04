import dataclasses
import typing

from . import tag as _tag


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Tweak:
    """
    Tweak.
    """

    string: str
    i: int | None = None
    tag: _tag.Tag | None = None

    def __post_init__(self):
        assert isinstance(self.string, str), repr(self.string)
        if self.i is not None:
            assert isinstance(self.i, int), repr(self.i)
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
    r"""
    Bundled indicator.

    ..  container:: example

        Raises exception on duplicate attributes:

        >>> abjad.Bundle(
        ...     indicator=abjad.Articulation("."),
        ...     tweaks=(
        ...         abjad.Tweak(r"- \tweak color #blue"),
        ...         abjad.Tweak(r"- \tweak color #red"),
        ...     ),
        ... )
        Traceback (most recent call last):
            ...
        Exception: duplicate 'color' attribute.

    """

    indicator: typing.Any
    tweaks: tuple[Tweak, ...] = ()
    comment: str | None = None

    def __post_init__(self):
        assert not isinstance(self.indicator, Bundle), repr(self.indicator)
        assert isinstance(self.tweaks, tuple), repr(self.tweaks)
        assert all(isinstance(_, Tweak) for _ in self.tweaks)
        attributes = [_.attribute() for _ in self.tweaks]
        for attribute in attributes:
            if 1 < attributes.count(attribute):
                raise Exception(f"duplicate {attribute!r} attribute.")
        assert isinstance(self.comment, str | None), repr(self.comment)

    def _get_contributions(self, *, component=None, wrapper=None):
        try:
            contributions = self.indicator._get_contributions(
                component=component, wrapper=wrapper
            )
        except TypeError:
            component = component or wrapper.component
            contributions = self.indicator._get_contributions(component=component)
        lists = contributions.get_contribution_lists()
        if len(lists) == 2 and ["<>"] in lists:
            lists.remove(["<>"])
        if len(lists) == 2 and [r"\pitchedTrill"] in lists:
            lists.remove([r"\pitchedTrill"])
        assert len(lists) == 1, repr(lists)
        list_ = lists[0]
        strings = []
        if self.comment is not None:
            strings.append(self.comment)
        for tweak in sorted(self.tweaks):
            strings.extend(tweak._list_contributions())
        if 2 <= len(list_) and list_[-2] in ("^", "_", "-"):
            list_[-2:-2] = strings
        else:
            list_[-1:-1] = strings
        return contributions

    def get_attribute(self, attribute: str) -> Tweak | None:
        r"""
        Gets tweak with ``attribute``.

        ..  container:: example

            >>> markup = abjad.Markup(r"\markup Allegro")
            >>> bundle = abjad.bundle(
            ...     markup,
            ...     r"- \tweak color #red",
            ...     r"- \tweak font-size 3",
            ... )
            >>> bundle.get_attribute("color")
            Tweak(string='- \\tweak color #red', i=None, tag=None)

            >>> bundle.get_attribute("style") is None
            True

        """
        tweaks = [_ for _ in self.tweaks if _.attribute() == attribute]
        assert len(tweaks) in (0, 1)
        if tweaks:
            tweak = tweaks[0]
            return tweak
        return None

    def remove(self, tweak: Tweak) -> "Bundle":
        r"""
        Removes ``tweak`` from bundle and returns new bundle.

        ..  container:: example

            >>> markup = abjad.Markup(r"\markup Allegro")
            >>> bundle_1 = abjad.bundle(markup, r"- \tweak color #red")
            >>> tweak = bundle_1.get_attribute("color")

            >>> bundle_2 = bundle_1.remove(tweak)
            >>> bundle_2
            Bundle(indicator=Markup(string='\\markup Allegro'), tweaks=(), comment=None)

            >>> bundle_3 = abjad.bundle(bundle_2, r"- \tweak color #blue")
            >>> bundle_3.tweaks
            (Tweak(string='- \\tweak color #blue', i=None, tag=None),)

        """
        assert tweak in self.tweaks, repr(tweak)
        tweaks = list(self.tweaks)
        tweaks.remove(tweak)
        new_bundle = dataclasses.replace(self, tweaks=tuple(tweaks))
        return new_bundle


def bundle(
    indicator: typing.Any,
    *tweaks: str | Tweak,
    comment: str | None = None,
    overwrite: bool = False,
    tag: _tag.Tag | None = None,
) -> Bundle:
    r"""
    Bundles ``indicator`` with ``tweaks``.

    ..  container:: example

        Bundles indicator:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> bundle = abjad.bundle(
        ...     abjad.Articulation("."),
        ...     r"- \tweak color #red",
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

    ..  container:: example

        Bundles existing bundle:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> bundle = abjad.bundle(abjad.Articulation("."), r"- \tweak color #red")
        >>> bundle = abjad.bundle(bundle, r"- \tweak font-size 3")
        >>> abjad.attach(bundle, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #red
                - \tweak font-size 3
                - \staccato
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Raises exception on duplicate attribute:

        >>> bundle = abjad.bundle(
        ...     abjad.Articulation("."),
        ...     r"- \tweak color #blue",
        ...     r"- \tweak color #red",
        ... )
        Traceback (most recent call last):
            ...
        Exception: duplicate 'color' attribute:
        Tweak(string='- \\tweak color #blue', i=None, tag=None)
        Tweak(string='- \\tweak color #red', i=None, tag=None)

        Unless ``overwrite=True``:

        >>> bundle = abjad.bundle(
        ...     abjad.Articulation("."),
        ...     r"- \tweak color #blue",
        ...     r"- \tweak color #red",
        ...     overwrite=True,
        ... )
        >>> for _ in bundle.tweaks: _
        Tweak(string='- \\tweak color #red', i=None, tag=None)

    ..  container:: example

        Also raises exception on duplicate attribute:

        >>> bundle = abjad.bundle(
        ...     abjad.Articulation("."),
        ...     r"- \tweak color #blue",
        ... )
        >>> bundle = abjad.bundle(
        ...     bundle,
        ...     r"- \tweak color #red",
        ... )
        Traceback (most recent call last):
            ...
        Exception: duplicate 'color' attribute:
        OLD: Tweak(string='- \\tweak color #blue', i=None, tag=None)
        NEW: Tweak(string='- \\tweak color #red', i=None, tag=None)

        Unless ``overwrite=True``:

        >>> bundle = abjad.bundle(
        ...     abjad.Articulation("."),
        ...     r"- \tweak color #blue",
        ... )
        >>> bundle = abjad.bundle(
        ...     bundle,
        ...     r"- \tweak color #red",
        ...     overwrite=True,
        ... )
        >>> for _ in bundle.tweaks: _
        Tweak(string='- \\tweak color #red', i=None, tag=None)

    """
    input_tweaks: list[Tweak] = []
    for item in tweaks:
        if isinstance(item, Tweak):
            tweak = item
        else:
            assert isinstance(item, str)
            tweak = Tweak(item, tag=tag)
        tweak_attribute = tweak.attribute()
        for input_tweak in input_tweaks[:]:
            if input_tweak.attribute() == tweak_attribute:
                if overwrite is True:
                    input_tweaks.remove(input_tweak)
                else:
                    message = f"duplicate {tweak_attribute!r} attribute:\n"
                    message += repr(input_tweak) + "\n"
                    message += repr(tweak)
                    raise Exception(message)
        input_tweaks.append(tweak)
    if isinstance(indicator, Bundle):
        bundle_tweaks = list(indicator.tweaks)
        for input_tweak in input_tweaks:
            input_tweak_attribute = input_tweak.attribute()
            for bundle_tweak in bundle_tweaks[:]:
                if bundle_tweak.attribute() == input_tweak_attribute:
                    if overwrite is True:
                        bundle_tweaks.remove(bundle_tweak)
                    else:
                        message = f"duplicate {input_tweak.attribute()!r} attribute:\n"
                        message += f"OLD: {bundle_tweak!r}\n"
                        message += f"NEW: {input_tweak!r}"
                        raise Exception(message)
            bundle_tweaks.append(input_tweak)
        indicator = indicator.indicator
        input_tweaks = bundle_tweaks
    input_tweaks.sort()
    return Bundle(indicator, tweaks=tuple(input_tweaks), comment=comment)


def tweak(
    indicator: typing.Any,
    *tweaks: str | Tweak,
    overwrite: bool = False,
    tag: _tag.Tag | None = None,
) -> None:
    """
    Appends ``tweaks`` to ``indicator``.
    """
    from . import score as _score

    prototype = (
        _score.NoteHead,
        _score.Tuplet,
    )
    assert isinstance(indicator, prototype), repr(indicator)
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
    try:
        indicator.tweaks = tuple(tweaks_)
    except dataclasses.FrozenInstanceError:
        raise Exception(indicator, tweaks_)
