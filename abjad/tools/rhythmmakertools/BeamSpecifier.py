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

    ..  container:: example

        **Example 1.** Beams notes in each division together but does not beam
        between divisions:

        ::

            >>> specifier = rhythmmakertools.BeamSpecifier(
            ...     beam_each_division=True,
            ...     beam_divisions_together=False
            ...     )

    ..  container:: example

        **Example 2.** Beams everything:

        ::

            >>> specifier = rhythmmakertools.BeamSpecifier(
            ...     beam_each_division=True,
            ...     beam_divisions_together=True
            ...     )

    ..  container:: example

        **Example 3.** Beams nothing:

        ::

            >>> specifier = rhythmmakertools.BeamSpecifier(
            ...     beam_each_division=False,
            ...     beam_divisions_together=False
            ...     )

    Beam specifiers are immutable.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_beam_divisions_together',
        '_beam_each_division',
        '_beam_rests',
        '_stemlet_length',
        '_use_feather_beams',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beam_each_division=True,
        beam_divisions_together=None,
        beam_rests=None,
        stemlet_length=None,
        use_feather_beams=None,
        ):
        # assert isinstance(beam_each_division, bool)
        # assert isinstance(beam_divisions_together, bool)
        # assert isinstance(beam_rests, bool)
        # assert isinstance(use_feather_beams, bool)
        if beam_each_division is None:
            beam_each_division = bool(beam_each_division)
        self._beam_each_division = beam_each_division
        if beam_divisions_together is not None:
            beam_divisions_together = bool(beam_divisions_together)
        self._beam_divisions_together = beam_divisions_together
        if beam_rests is not None:
            beam_rests = bool(beam_rests)
        self._beam_rests = beam_rests
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
            durations = []
            for selection in selections:
                if isinstance(selection, selectiontools.Selection):
                    duration = selection.get_duration()
                else:
                    duration = selection._get_duration()
                durations.append(duration)
            beam = spannertools.DuratedComplexBeam(
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
            #attach(beam, components)
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
                >>> print(format(specifier))
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
        r'''Gets interpreter representation.

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

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.beam_divisions_together is None
                True

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._beam_divisions_together

    @property
    def beam_each_division(self):
        r'''Is true when each division should be beamed. Otherwise false.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.beam_each_division
                True

        Defaults to true.

        Set to true or false.

        Returns true or false.
        '''
        return self._beam_each_division

    @property
    def beam_rests(self):
        r'''Is true when beams should include rests. Otherwise false.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.beam_rests is None
                True

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._beam_rests

    @property
    def stemlet_length(self):
        r'''Gets stemlet length.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.stemlet_length is None
                True

        Defaults to none.

        Set to none, integer or float.

        Note that stemlets appear only when `beam_rests` is set to true.

        Returns none, integer or float.
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
