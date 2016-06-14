# -*- coding: utf-8 -*-
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import override


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
        beam_divisions_together=False,
        beam_rests=False,
        stemlet_length=None,
        use_feather_beams=False,
        ):
        assert isinstance(beam_each_division, bool)
        assert isinstance(beam_divisions_together, bool)
        assert isinstance(beam_rests, bool)
        assert isinstance(stemlet_length, (type(None), int, float))
        assert isinstance(use_feather_beams, bool)
        self._beam_each_division = beam_each_division
        self._beam_divisions_together = beam_divisions_together
        self._beam_rests = beam_rests
        self._stemlet_length = stemlet_length
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
            leaves = list(iterate(components).by_leaf())
            #attach(beam, components)
            attach(beam, leaves)
        elif self.beam_each_division:
            for selection in selections:
                beam = spannertools.MultipartBeam(beam_rests=self.beam_rests)
                if self.stemlet_length is not None:
                    grob_proxy = override(beam).staff.stem
                    grob_proxy.stemlet_length = self.stemlet_length
                leaves = list(iterate(selection).by_leaf())
                attach(beam, leaves)

    def __eq__(self, arg):
        r'''Is true when `arg` is a beam specifier with `beam_each_division`
        and `beam_divisions_together` equal to those of this beam specifier.
        Otherwise false.

        ..  container:: example

            ::

                >>> specifier_1 = rhythmmakertools.BeamSpecifier(
                ...     beam_each_division=True,
                ...     )
                >>> specifier_2 = rhythmmakertools.BeamSpecifier(
                ...     beam_each_division=False,
                ...     )

            ::

                >>> specifier_1 == specifier_1
                True
                >>> specifier_1 == specifier_2
                False
                >>> specifier_2 == specifier_1
                False
                >>> specifier_2 == specifier_2
                True

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            if self.beam_each_division == arg.beam_each_division and \
                self.beam_divisions_together == arg.beam_divisions_together:
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats beam specifier.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> print(format(specifier))
                rhythmmakertools.BeamSpecifier(
                    beam_each_division=True,
                    beam_divisions_together=False,
                    beam_rests=False,
                    use_feather_beams=False,
                    )

        Returns string.
        '''
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __hash__(self):
        r'''Hashes beam specifier.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(BeamSpecifier, self).__hash__()

    def __repr__(self):
        r'''Gets interpreter representation.

        ..  container:: example

            ::

                >>> rhythmmakertools.BeamSpecifier()
                BeamSpecifier(beam_each_division=True, beam_divisions_together=False, beam_rests=False, use_feather_beams=False)

        Returns string.
        '''
        return AbjadValueObject.__repr__(self)

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
                >>> specifier.beam_divisions_together
                False

        Defaults to false.

        Set to true or false.

        Returns true or false.
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
                >>> specifier.beam_rests
                False

        Defaults to false.

        Set to true or false.

        Returns true or false.
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
                >>> specifier.use_feather_beams
                False

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._use_feather_beams