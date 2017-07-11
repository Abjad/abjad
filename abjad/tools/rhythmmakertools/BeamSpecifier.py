# -*- coding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import select


class BeamSpecifier(AbjadValueObject):
    r'''Beam specifier.

    ::

        >>> import abjad
        >>> from abjad.tools import rhythmmakertools

    ..  container:: example

        Beams each division by default:

        ::

            >>> staff = abjad.Staff(name='RhythmicStaff')
            >>> staff.extend("c'8 c' c'16 c' c' c' c'8 c' c' c'")
            >>> abjad.setting(staff).auto_beaming = False
            >>> selections = [staff[:4], staff[4:]]
            >>> specifier = rhythmmakertools.BeamSpecifier()
            >>> specifier(selections)
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \context Staff = "RhythmicStaff" \with {
                autoBeaming = ##f
            } {
                c'8 [
                c'8
                c'16
                c'16 ]
                c'16 [
                c'16
                c'8
                c'8
                c'8
                c'8 ]
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_beam_divisions_together',
        '_beam_each_division',
        '_beam_rests',
        '_hide_nibs',
        '_stemlet_length',
        '_use_feather_beams',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        beam_each_division=True,
        beam_divisions_together=None,
        beam_rests=None,
        hide_nibs=None,
        stemlet_length=None,
        use_feather_beams=None,
        ):
        if beam_each_division is None:
            beam_each_division = bool(beam_each_division)
        self._beam_each_division = beam_each_division
        if beam_divisions_together is not None:
            beam_divisions_together = bool(beam_divisions_together)
        self._beam_divisions_together = beam_divisions_together
        if beam_rests is not None:
            beam_rests = bool(beam_rests)
        self._beam_rests = beam_rests
        if hide_nibs is not None:
            hide_nibs = bool(hide_nibs)
        self._hide_nibs = hide_nibs
        if stemlet_length is not None:
            assert isinstance(stemlet_length, (int, float))
        self._stemlet_length = stemlet_length
        if use_feather_beams is not None:
            use_feather_beams = bool(use_feather_beams)
        self._use_feather_beams = use_feather_beams

    ### SPECIAL METHODS ###

    def __call__(self, selections):
        r'''Calls beam specifier on `selections`.

        Returns none.
        '''
        if self.beam_divisions_together:
            if self.hide_nibs:
                beam = spannertools.MultipartBeam(beam_rests=self.beam_rests)
            else:
                durations = []
                for selection in selections:
                    if isinstance(selection, selectiontools.Selection):
                        duration = selection.get_duration()
                    else:
                        duration = selection._get_duration()
                    durations.append(duration)
                beam = spannertools.DuratedComplexBeam(
                    beam_rests=self.beam_rests,
                    durations=durations,
                    span_beam_count=1,
                    )
            components = []
            for selection in selections:
                if isinstance(selection, selectiontools.Selection):
                    components.extend(selection)
                elif isinstance(selection, scoretools.Tuplet):
                    components.append(selection)
                else:
                    raise TypeError(selection)
            if self.stemlet_length is not None:
                grob_proxy = override(beam).staff.stem
                grob_proxy.stemlet_length = self.stemlet_length
            leaves = select(components).by_leaf()
            attach(beam, leaves)
        elif self.beam_each_division:
            for selection in selections:
                beam = spannertools.MultipartBeam(beam_rests=self.beam_rests)
                if self.stemlet_length is not None:
                    grob_proxy = override(beam).staff.stem
                    grob_proxy.stemlet_length = self.stemlet_length
                leaves = select(selection).by_leaf()
                attach(beam, leaves)

    def __format__(self, format_specification=''):
        r'''Formats beam specifier.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> f(specifier)
                rhythmmakertools.BeamSpecifier(
                    beam_each_division=True,
                    )

        Returns string.
        '''
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __repr__(self):
        r'''Gets interpreter representation of beam specifier.

        ..  container:: example

            ::

                >>> rhythmmakertools.BeamSpecifier()
                BeamSpecifier(beam_each_division=True)

        Returns string.
        '''
        return super(BeamSpecifier, self).__repr__()

    ### PRIVATE METHODS ###

    def _detach_all_beams(self, divisions):
        for component in iterate(divisions).by_class():
            detach(spannertools.Beam, component)

    ### PUBLIC PROPERTIES ###

    @property
    def beam_divisions_together(self):
        r'''Is true when divisions should beam together. Otherwise false.

        ..  container:: example

            Does not beam divisions together:

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 c' c'16 c' c' c' c'8 c' c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    c'8 [
                    c'8
                    c'16
                    c'16 ]
                    c'16 [
                    c'16
                    c'8
                    c'8
                    c'8
                    c'8 ]
                }

        ..  container:: example

            Beams divisions together (but excludes rests):

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 c' c'16 c' c' c' c'8 r c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier(
                ...     beam_divisions_together=True,
                ...     beam_rests=False,
                ...     )
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #1
                    c'8 [
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    c'8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #2
                    c'16
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #1
                    c'16
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #2
                    c'16
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #1
                    c'16
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    c'8 ]
                    r8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    c'8 [
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #0
                    c'8 ]
                }

        ..  container:: example

            Beams divisions together (and includes rests):

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 c' c'16 c' c' c' c'8 r c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier(
                ...     beam_divisions_together=True,
                ...     beam_rests=True,
                ...     )
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #1
                    c'8 [
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    c'8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #2
                    c'16
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #1
                    c'16
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #2
                    c'16
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #1
                    c'16
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    c'8
                    r8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    c'8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #0
                    c'8 ]
                }

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.beam_divisions_together is None
                True

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._beam_divisions_together

    @property
    def beam_each_division(self):
        r'''Is true when specifier beams each division. Otherwise false.

        ..  container:: example

            Beams nothing:

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 c' c'16 c' c' c' c'8 c' c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier(
                ...     beam_each_division=False,
                ...     )
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    c'8
                    c'8
                    c'16
                    c'16
                    c'16
                    c'16
                    c'8
                    c'8
                    c'8
                    c'8
                }

        ..  container:: example

            Beams each division (but excludes rests):

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 c' c'16 c' c' c' c'8 r c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier(
                ...     beam_each_division=True,
                ...     beam_rests=False,
                ...     )
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    c'8 [
                    c'8
                    c'16
                    c'16 ]
                    c'16 [
                    c'16
                    c'8 ]
                    r8
                    c'8 [
                    c'8 ]
                }

        ..  container:: example

            Beams each division (and includes rests):

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 c' c'16 c' c' c' c'8 r c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier(
                ...     beam_each_division=True,
                ...     beam_rests=True,
                ...     )
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    c'8 [
                    c'8
                    c'16
                    c'16 ]
                    c'16 [
                    c'16
                    c'8
                    r8
                    c'8
                    c'8 ]
                }

        ..  container:: example

            Defaults to true:

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.beam_each_division
                True

        Set to true or false.

        Returns true or false.
        '''
        return self._beam_each_division

    @property
    def beam_rests(self):
        r'''Is true when beams should include rests. Otherwise false.

        ..  container:: example

            Does not beam rests:

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 c' c'16 c' c' c' c'8 r c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    c'8 [
                    c'8
                    c'16
                    c'16 ]
                    c'16 [
                    c'16
                    c'8 ]
                    r8
                    c'8 [
                    c'8 ]
                }

        ..  container:: example

            Beams rests:

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 c' c'16 c' c' c' c'8 r c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier(
                ...     beam_rests=True,
                ...     )
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    c'8 [
                    c'8
                    c'16
                    c'16 ]
                    c'16 [
                    c'16
                    c'8
                    r8
                    c'8
                    c'8 ]
                }

        ..  container:: example

            Beams skips:

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 c' c'16 c' c' c' c'8 s c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier(
                ...     beam_rests=True,
                ...     )
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    c'8 [
                    c'8
                    c'16
                    c'16 ]
                    c'16 [
                    c'16
                    c'8
                    s8
                    c'8
                    c'8 ]
                }

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.beam_rests is None
                True

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._beam_rests

    @property
    def hide_nibs(self):
        r'''Is true when specifier hides nibs.

        ..  container:: example

            Does not hide nibs:

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 r c'16 c' c' c' c'8 r c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier(
                ...     beam_divisions_together=True,
                ...     beam_rests=False,
                ...     )
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    \set stemLeftBeamCount = #0
                    \set stemRightBeamCount = #1
                    c'8 [ ]
                    r8
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #2
                    c'16 [
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #1
                    c'16
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #2
                    c'16
                    \set stemLeftBeamCount = #2
                    \set stemRightBeamCount = #1
                    c'16
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    c'8 ]
                    r8
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #1
                    c'8 [
                    \set stemLeftBeamCount = #1
                    \set stemRightBeamCount = #0
                    c'8 ]
                }

        ..  container:: example

            Hides nibs:

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 r c'16 c' c' c' c'8 r c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier(
                ...     beam_divisions_together=True,
                ...     beam_rests=False,
                ...     hide_nibs=True,
                ...     )
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    c'8
                    r8
                    c'16 [
                    c'16
                    c'16
                    c'16
                    c'8 ]
                    r8
                    c'8 [
                    c'8 ]
                }

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._hide_nibs

    @property
    def stemlet_length(self):
        r'''Gets stemlet length.

        ..  container:: example

            Beams rests without stemlets:

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 c' c'16 c' c' c' c'8 r c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier(
                ...     beam_rests=True,
                ...     )
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    c'8 [
                    c'8
                    c'16
                    c'16 ]
                    c'16 [
                    c'16
                    c'8
                    r8
                    c'8
                    c'8 ]
                }

        ..  container:: example

            Beams rests with stemlets:

            ::

                >>> staff = abjad.Staff(name='RhythmicStaff')
                >>> staff.extend("c'8 c' c'16 c' c' c' c'8 r c' c'")
                >>> abjad.setting(staff).auto_beaming = False
                >>> selections = [staff[:4], staff[4:]]
                >>> specifier = rhythmmakertools.BeamSpecifier(
                ...     beam_rests=True,
                ...     stemlet_length=2,
                ...     )
                >>> specifier(selections)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \context Staff = "RhythmicStaff" \with {
                    autoBeaming = ##f
                } {
                    \override Staff.Stem.stemlet-length = #2
                    c'8 [
                    c'8
                    c'16
                    \revert Staff.Stem.stemlet-length
                    c'16 ]
                    \override Staff.Stem.stemlet-length = #2
                    c'16 [
                    c'16
                    c'8
                    r8
                    c'8
                    \revert Staff.Stem.stemlet-length
                    c'8 ]
                }

        Stemlets appear only when `beam_rests` is set to true.

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.stemlet_length is None
                True

        Set to integer, float or none.

        Returns integer, float or none.
        '''
        return self._stemlet_length

    @property
    def use_feather_beams(self):
        r'''Is true when multiple beams should feather. Otherwise false.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.use_feather_beams is None
                True

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._use_feather_beams
