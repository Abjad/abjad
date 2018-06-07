import typing
from abjad.enumerations import VerticalAlignment
from abjad.top.inspect import inspect
from abjad.top.new import new
from abjad.typings import Number
from abjad.utilities.String import String
from .Spanner import Spanner


class Beam(Spanner):
    r"""
    Beam.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
        >>> abjad.setting(staff).auto_beaming = False
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                d'8
                e'8
                f'8
                g'2
            }

        >>> beam = abjad.Beam()
        >>> abjad.attach(beam, staff[:2])
        >>> beam = abjad.Beam()
        >>> abjad.attach(beam, staff[2:4])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                [
                d'8
                ]
                e'8
                [
                f'8
                ]
                g'2
            }

    ..  container:: example

        Tweaks beam positions:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
        >>> abjad.setting(staff).auto_beaming = False
        >>> beam = abjad.Beam()
        >>> abjad.tweak(beam).positions = (3, 3)
        >>> abjad.attach(beam, staff[:2])
        >>> beam = abjad.Beam()
        >>> abjad.tweak(beam).positions = (3, 3)
        >>> abjad.attach(beam, staff[2:4])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                - \tweak positions #'(3 . 3)
                [
                d'8
                ]
                e'8
                - \tweak positions #'(3 . 3)
                [
                f'8
                ]
                g'2
            }

    ..  container:: example

        Spanners can be tagged:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
        >>> abjad.setting(staff).auto_beaming = False
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                c'8
                d'8
                e'8
                f'8
                g'2
            }

        >>> beam = abjad.Beam()
        >>> abjad.attach(beam, staff[:2], tag='BEAM')
        >>> beam = abjad.Beam()
        >>> abjad.attach(beam, staff[2:4])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff
        \with
        {
            autoBeaming = ##f
        }
        {
            c'8
            [ %! BEAM
            d'8
            ] %! BEAM
            e'8
            [
            f'8
            ]
            g'2
        }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_stemlet_length',
        )

    _start_command = '['

    _stop_command = ']'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: typing.Union[str, VerticalAlignment] = None,
        leak: bool = None,
        stemlet_length: Number = None,
        ) -> None:
        Spanner.__init__(self, leak=leak)
        direction = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction
        self._stemlet_length = stemlet_length

    ### PRIVATE METHODS ###

    def _add_stemlet_length(self, leaf, bundle):
        from abjad.core.Staff import Staff
        if self.stemlet_length is None:
            return
        if leaf is self[0]:
            parentage = inspect(leaf).get_parentage()
            staff = parentage.get_first(Staff)
            lilypond_type = staff.lilypond_type
            string = r'\override {}.Stem.stemlet-length = {}'
            string = string.format(lilypond_type, self.stemlet_length)
            bundle.before.commands.append(string)
        if leaf is self[-1]:
            parentage = inspect(leaf).get_parentage()
            staff = parentage.get_first(Staff)
            lilypond_type = staff.lilypond_type
            string = r'\revert {}.Stem.stemlet-length'
            string = string.format(lilypond_type, self.stemlet_length)
            bundle.before.commands.append(string)

    def _copy_keywords(self, new):
        Spanner._copy_keywords(self, new)
        new._direction = self.direction
        new._stemlet_length = self.stemlet_length

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if leaf is self[0]:
            strings = self.start_command()
            bundle.right.spanner_starts.extend(strings)
        if leaf is self[-1]:
            string = self.stop_command()
            if leaf is self[0]:
                bundle.right.spanner_starts.append(string)
            else:
                bundle.right.spanner_stops.append(string)
        self._add_stemlet_length(leaf, bundle)
        return bundle

    @staticmethod
    def _is_beamable(argument, beam_rests=False) -> bool:
        """
        Is true when ``argument`` is a beamable component.

        ..  container:: example

            Without allowing for beamed rests:

            >>> staff = abjad.Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
            >>> staff.extend(r"r8 e''8 ( ef'2 )")
            >>> abjad.show(staff) # doctest: +SKIP

            >>> for leaf in staff:
            ...     result = abjad.Beam._is_beamable(leaf)
            ...     print(f'{str(leaf):<8}\t{result}')
            ...
            r32     False
            a'32    True
            gs'32   True
            fs''32  True
            f''8    True
            r8      False
            e''8    True
            ef'2    False

        ..  container:: example

            Allowing for beamed rests:

            >>> staff = abjad.Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
            >>> staff.extend(r"r8 e''8 ( ef'2 )")
            >>> abjad.show(staff) # doctest: +SKIP

            >>> for leaf in staff:
            ...     result = abjad.Beam._is_beamable(
            ...         leaf,
            ...         beam_rests=True,
            ...         )
            ...     print(f'{str(leaf):<8}\t{result}')
            ...
            r32	True
            a'32	True
            gs'32	True
            fs''32	True
            f''8	True
            r8	True
            e''8	True
            ef'2	False

        ..  container:: example

            Is true for skips of any duration when ``beam_rests`` is true:

            >>> skip = abjad.Skip((1, 32))
            >>> abjad.Beam._is_beamable(skip, beam_rests=True)
            True

            >>> skip = abjad.Skip((1))
            >>> abjad.Beam._is_beamable(skip, beam_rests=True)
            True

        ..  container:: example

            Is true for rests of any duration when ``beam_rests`` is true:

            >>> rest = abjad.Rest((1, 32))
            >>> abjad.Beam._is_beamable(rest, beam_rests=True)
            True

            >>> rest = abjad.Rest((1))
            >>> abjad.Beam._is_beamable(rest, beam_rests=True)
            True

        """
        from abjad.core.Chord import Chord
        from abjad.core.MultimeasureRest import MultimeasureRest
        from abjad.core.Note import Note
        from abjad.core.Rest import Rest
        from abjad.core.Skip import Skip
        if isinstance(argument, (Chord, Note)):
            if 0 < argument.written_duration.flag_count:
                return True
        prototype = (
            MultimeasureRest,
            Rest,
            Skip,
            )
        if beam_rests and isinstance(argument, prototype):
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> typing.Optional[String]:
        """
        Gets direction.
        """
        return self._direction
        
    @property
    def leak(self):
        r"""
        Is true when beam leaks one leaf to the right with LilyPond empty chord
        ``<>`` construct.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam()
            >>> abjad.attach(beam, staff[:3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    [
                    d'8
                    e'8
                    ]
                    f'8
                    g'2
                }

            With leak:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam(leak=True)
            >>> abjad.attach(beam, staff[:3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    [
                    d'8
                    e'8
                    <> ]
                    f'8
                    g'2
                }

        """
        return super(Beam, self).leak

    @property
    def stemlet_length(self) -> typing.Optional[Number]:
        r"""
        Gets stemlet length.

        ..  container:: example

            >>> staff = abjad.Staff(
            ...     "r8 c' r c' g'2",
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam(stemlet_length=2)
            >>> abjad.attach(beam, staff[:-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new RhythmicStaff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \override RhythmicStaff.Stem.stemlet-length = 2
                    r8
                    [
                    c'8
                    r8
                    \revert RhythmicStaff.Stem.stemlet-length
                    c'8
                    ]
                    g'2
                }

        """
        return self._stemlet_length

    ### PUBLIC METHODS ###

    def start_command(self) -> typing.List[str]:
        """
        Gets start command.

        ..  container:: example

            >>> abjad.Beam().start_command()
            ['[']

            With direction:

            >>> abjad.Beam(direction=abjad.Up).start_command()
            ['^ [']

        """
        return super(Beam, self).start_command()

    def stop_command(self) -> typing.Optional[str]:
        """
        Gets stop command.

        ..  container:: example

            >>> abjad.Beam().stop_command()
            ']'

            Leaked to the right:

            >>> abjad.Beam(leak=True).stop_command()
            '<> ]'

        """
        string = super(Beam, self).stop_command()
        string = self._add_leak(string)
        return string
