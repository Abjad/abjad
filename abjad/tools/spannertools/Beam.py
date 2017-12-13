from .Spanner import Spanner


class Beam(Spanner):
    r'''Beam.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
        >>> abjad.setting(staff).auto_beaming = False
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
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
            \new Staff \with {
                autoBeaming = ##f
            } {
                c'8 [
                d'8 ]
                e'8 [
                f'8 ]
                g'2
            }

    ..  container:: example

        Spanners can be tagged:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
        >>> abjad.setting(staff).auto_beaming = False
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
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
        \new Staff \with {
            autoBeaming = ##f
        } {
            c'8 [ %! BEAM
            d'8 ] %! BEAM
            e'8 [
            f'8 ]
            g'2
        }

    ..  container:: example

        Spanners can be site marked:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
        >>> abjad.setting(staff).auto_beaming = False
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
                c'8
                d'8
                e'8
                f'8
                g'2
            }

        >>> beam = abjad.Beam()
        >>> abjad.attach(beam, staff[:2], site='M1')
        >>> beam = abjad.Beam()
        >>> abjad.attach(beam, staff[2:4])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff \with {
            autoBeaming = ##f
        } {
            c'8 [ %! M1
            d'8 ] %! M1
            e'8 [
            f'8 ]
            g'2
        }

    ..  container:: example

        Spanners can be site marked and tagged at the same time:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
        >>> abjad.setting(staff).auto_beaming = False
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
                c'8
                d'8
                e'8
                f'8
                g'2
            }

        >>> beam = abjad.Beam()
        >>> abjad.attach(beam, staff[:2], site='M1', tag='BEAM')
        >>> beam = abjad.Beam()
        >>> abjad.attach(beam, staff[2:4])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff \with {
            autoBeaming = ##f
        } {
            c'8 [ %! BEAM:M1
            d'8 ] %! BEAM:M1
            e'8 [
            f'8 ]
            g'2
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_stemlet_length',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        direction=None,
        overrides=None,
        stemlet_length=None,
        ):
        import abjad
        Spanner.__init__(self, overrides=overrides)
        direction = abjad.String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction
        self._stemlet_length = stemlet_length

    ### PRIVATE METHODS ###

    def _add_stemlet_length(self, leaf, bundle):
        import abjad
        if self.stemlet_length is None:
            return
        if self._is_my_first_leaf(leaf):
            parentage = abjad.inspect(leaf).get_parentage()
            staff = parentage.get_first(abjad.Staff)
            headword = getattr(staff, 'headword', 'Staff')
            string = r'\override {}.Stem.stemlet-length = {}'
            string = string.format(headword, self.stemlet_length)
            bundle.before.commands.append(string)
        if self._is_my_last_leaf(leaf):
            parentage = abjad.inspect(leaf).get_parentage()
            staff = parentage.get_first(abjad.Staff)
            headword = getattr(staff, 'headword', 'Staff')
            string = r'\revert {}.Stem.stemlet-length'
            string = string.format(headword, self.stemlet_length)
            bundle.before.commands.append(string)

    def _copy_keyword_args(self, new):
        Spanner._copy_keyword_args(self, new)
        new._direction = self.direction
        new._stemlet_length = self.stemlet_length

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_first_leaf(leaf):
            if self.direction is not None:
                string = '{} ['.format(self.direction)
            else:
                string = '['
            bundle.right.spanner_starts.append(string)
        if self._is_my_last_leaf(leaf):
            string = ']'
            if self._is_my_first_leaf(leaf):
                bundle.right.spanner_starts.append(string)
            else:
                bundle.right.spanner_stops.append(string)
        self._add_stemlet_length(leaf, bundle)
        return bundle

    ### PUBLIC METHODS ###

    @staticmethod
    def _is_beamable(argument, beam_rests=False):
        '''Is true when `argument` is a beamable component. Otherwise false.

        ..  container:: example

            Without allowing for beamed rests:

            >>> staff = abjad.Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
            >>> staff.extend(r"r8 e''8 ( ef'2 )")
            >>> abjad.show(staff) # doctest: +SKIP

            >>> for leaf in staff:
            ...     result = abjad.Beam._is_beamable(leaf)
            ...     print('{:<8}\t{}'.format(leaf, result))
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
            ...     print('{:<8}\t{}'.format(leaf, result))
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

            Is true for skips of any duration when `beam_rests` is true:

            >>> skip = abjad.Skip((1, 32))
            >>> abjad.Beam._is_beamable(skip, beam_rests=True)
            True

            >>> skip = abjad.Skip((1))
            >>> abjad.Beam._is_beamable(skip, beam_rests=True)
            True

        ..  container:: example

            Is true for rests of any duration when `beam_rests` is true:

            >>> rest = abjad.Rest((1, 32))
            >>> abjad.Beam._is_beamable(rest, beam_rests=True)
            True

            >>> rest = abjad.Rest((1))
            >>> abjad.Beam._is_beamable(rest, beam_rests=True)
            True

        Returns true or false.
        '''
        import abjad
        prototype = (abjad.Note, abjad.Chord)
        if isinstance(argument, prototype):
            if 0 < argument.written_duration.flag_count:
                return True
        prototype = (
            abjad.MultimeasureRest,
            abjad.Rest,
            abjad.Skip,
            )
        if beam_rests and isinstance(argument, prototype):
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction.

        Defaults to none.

        Set to up, down or none.

        Returns up, down or none.
        '''
        return self._direction
        
    @property
    def stemlet_length(self):
        r'''Gets stemlet length.

        ..  container:: example

            >>> staff = abjad.Staff(
            ...     "r8 c' r c' g'2",
            ...     context_name='RhythmicStaff',
            ...     )
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.Beam(stemlet_length=2)
            >>> abjad.attach(beam, staff[:-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new RhythmicStaff \with {
                    autoBeaming = ##f
                } {
                    \override RhythmicStaff.Stem.stemlet-length = 2
                    r8 [
                    c'8
                    r8
                    \revert RhythmicStaff.Stem.stemlet-length
                    c'8 ]
                    g'2
                }

        Defaults to none.

        Set to nonnegative integer, float or none.

        Returns nonnegative integer, float or none.
        '''
        return self._stemlet_length
