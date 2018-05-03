from .Beam import Beam


class MultipartBeam(Beam):
    r'''Multipart beam.

    Beams together everything that can be beamed and ignores everything else.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'4 f'8 g'8 r4")
        >>> beam = abjad.MultipartBeam()
        >>> abjad.attach(beam, staff[:])
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
                [
                d'8
                ]
                e'4
                f'8
                [
                g'8
                ]
                r4
            }

    ..  container:: example

        >>> staff = abjad.Staff("c'8 r8 d'8 r8 f'8 g'8 r4")
        >>> beam = abjad.MultipartBeam()
        >>> abjad.attach(beam, staff[:])
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
                r8
                d'8
                r8
                f'8
                [
                g'8
                ]
                r4
            }

    Avoids rests.

    Avoids large-duration notes.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beam_rests',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beam_rests=False,
        direction=None,
        overrides=None,
        stemlet_length=None,
        ):
        Beam.__init__(
            self,
            direction=direction,
            overrides=overrides,
            stemlet_length=stemlet_length,
            )
        self._beam_rests = bool(beam_rests)

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        self._beam_rests = self.beam_rests

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if not self._is_beamable(leaf, beam_rests=self.beam_rests):
            return bundle
        direction_string = ''
        if self.direction is not None:
            direction_string = '{} '.format(self.direction)
        beamable_leaf_count = 0
        for leaf_ in self.leaves:
            if self._is_beamable(leaf_, beam_rests=self.beam_rests):
                beamable_leaf_count += 1
        if 2 <= beamable_leaf_count:
            previous_leaf = leaf._get_leaf(-1)
            if previous_leaf not in self.leaves:
                previous_leaf = None
            next_leaf = leaf._get_leaf(1)
            if next_leaf not in self.leaves:
                next_leaf = None
            start_piece = None
            stop_piece = None
            if leaf is self[0]:
                if next_leaf is not None:
                    if self._is_beamable(
                        next_leaf,
                        beam_rests=self.beam_rests,
                        ):
                        start_piece = '{}['.format(direction_string)
            else:
                if previous_leaf is not None:
                    if not self._is_beamable(
                        previous_leaf,
                        beam_rests=self.beam_rests,
                        ):
                        if self._is_beamable(
                            next_leaf,
                            beam_rests=self.beam_rests,
                            ):
                            start_piece = '{}['.format(direction_string)
            if leaf is self[-1]:
                if previous_leaf is not None:
                    if self._is_beamable(
                        previous_leaf,
                        beam_rests=self.beam_rests,
                        ):
                        stop_piece = ']'
            else:
                if self._is_beamable(
                    previous_leaf,
                    beam_rests=self.beam_rests,
                    ):
                    next_leaf = leaf._get_leaf(1)
                    if next_leaf is not None:
                        if not self._is_beamable(
                            next_leaf,
                            beam_rests=self.beam_rests,
                            ):
                            stop_piece = ']'
            if start_piece and stop_piece:
                bundle.right.spanner_starts.extend([
                    start_piece, stop_piece])
            elif start_piece:
                bundle.right.spanner_starts.append(start_piece)
            elif stop_piece:
                bundle.right.spanner_stops.append(stop_piece)
        self._add_stemlet_length(leaf, bundle)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def beam_rests(self):
        r'''Is true when beam should include rests. Otherwise false.

        ..  container:: example

            Without beamed rests:

            >>> staff = abjad.Staff("c'8 d'8 r8 f'8 g'8 r4.")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.MultipartBeam()
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

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
                r8
                f'8
                [
                g'8
                ]
                r4.
            }

            Abjad beams no rests.

            LilyPond beams no rests.

        ..  container:: example

            With beamed rests:

            >>> staff = abjad.Staff("c'8 d'8 r8 f'8 g'8 r4.")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.MultipartBeam(beam_rests=True)
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

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
                r8
                f'8
                g'8
                r4.
                ]
            }

            Abjad beams all rests.

            LilyPond beams only small-duration rests.

        ..  container:: example

            With beamed rests:

            >>> staff = abjad.Staff("c'8 d'8 r4. f'8 g'8 r8")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.MultipartBeam(beam_rests=True)
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

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
                r4.
                f'8
                g'8
                r8
                ]
            }

            Abjad beams all rests.

            LilyPond beams only small-duration rests.

        ..  container:: example

            With beamed skips:

            >>> staff = abjad.Staff("c'8 d'8 s4. f'8 g'8 s8")
            >>> abjad.setting(staff).auto_beaming = False
            >>> beam = abjad.MultipartBeam(beam_rests=True)
            >>> abjad.attach(beam, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

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
                s4.
                f'8
                g'8
                s8
                ]
            }

            Abjad beams all skips.

            LilyPond beams all (internal) skips.

        Defaults to false.

        Set to true or false.

        Returns true of false.
        '''
        return self._beam_rests

    @property
    def stemlet_length(self):
        r'''Gets stemlet length.

        ..  container:: example

            >>> staff = abjad.Staff(
            ...     "c'16 r c' c' r c'",
            ...     lilypond_type='RhythmicStaff',
            ...     )
            >>> durations = [(3, 16), (3, 16)]
            >>> beam = abjad.MultipartBeam(
            ...     beam_rests=True,
            ...     stemlet_length=1.5,
            ...     )
            >>> abjad.attach(beam, staff[:])
            >>> abjad.override(staff).beam.positions = (4.5, 4.5)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new RhythmicStaff
                \with
                {
                    \override Beam.positions = #'(4.5 . 4.5)
                }
                {
                    \override RhythmicStaff.Stem.stemlet-length = 1.5
                    c'16
                    [
                    r16
                    c'16
                    c'16
                    r16
                    \revert RhythmicStaff.Stem.stemlet-length
                    c'16
                    ]
                }

        Defaults to none.

        Set to nonnegative integer, float or none.

        Returns nonnegative integer, float or none.
        '''
        return self._stemlet_length
