# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate


class TupletSpellingSpecifier(AbjadValueObject):
    r'''Tuplet spelling specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_avoid_dots',
        '_rewrite_rest_filled_tuplets',
        '_flatten_trivial_tuplets',
        '_is_diminution',
        '_preferred_denominator',
        '_simplify_redundant_tuplets',
        '_use_note_duration_bracket',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        avoid_dots=False,
        flatten_trivial_tuplets=False,
        is_diminution=True,
        preferred_denominator=None,
        rewrite_rest_filled_tuplets=False,
        simplify_redundant_tuplets=False,
        use_note_duration_bracket=False,
        ):
        # TODO: Consider renaming is_diminution=True to is_augmentation=None.
        #       That would allow for all keywords to default to None,
        #       and therefore a single-line storage format.
        self._avoid_dots = bool(avoid_dots)
        self._flatten_trivial_tuplets = bool(flatten_trivial_tuplets)
        self._is_diminution = bool(is_diminution)
        self._preferred_denominator = preferred_denominator
        self._rewrite_rest_filled_tuplets = bool(rewrite_rest_filled_tuplets)
        self._simplify_redundant_tuplets = bool(simplify_redundant_tuplets)
        self._use_note_duration_bracket = bool(use_note_duration_bracket)

    ### PRIVATE METHODS ###

    def _apply_preferred_denominator(self, selections, divisions):
        from abjad.tools import scoretools
        if not self.preferred_denominator:
            return
        tuplets = iterate(selections).by_class(scoretools.Tuplet)
        tuplets = list(tuplets)
        if divisions is None:
            divisions = len(tuplets) * [None]
        assert len(selections) == len(divisions)
        assert len(tuplets) == len(divisions)
        for tuplet, division in zip(tuplets, divisions):
            if self.preferred_denominator == 'divisions':
                tuplet.preferred_denominator = division.numerator
            elif isinstance(
                self.preferred_denominator, durationtools.Duration):
                unit_duration = self.preferred_denominator
                assert unit_duration.numerator == 1
                duration = inspect_(tuplet).get_duration()
                denominator = unit_duration.denominator
                nonreduced_fraction = duration.with_denominator(denominator)
                tuplet.preferred_denominator = nonreduced_fraction.numerator
            elif mathtools.is_positive_integer(self.preferred_denominator):
                tuplet.preferred_denominator = self.preferred_denominator
            else:
                message = 'invalid value for preferred denominator: {!r}.'
                message = message.format(self.preferred_denominator)
                raise Exception(message)

    def _do_simplify_redundant_tuplets(self, selections):
        from abjad.tools import scoretools
        if not self.simplify_redundant_tuplets:
            return
        for tuplet in iterate(selections).by_class(scoretools.Tuplet):
            tuplet._simplify_redundant_tuplet()

    ### PUBLIC PROPERTIES ###

    @property
    def avoid_dots(self):
        r'''Is true when tuplet spelling should avoid dotted rhythmic values.
        Otherwise false.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._avoid_dots

    @property
    def flatten_trivial_tuplets(self):
        r'''Is true when tuplet spelling should flatten trivial tuplets.
        Otherwise false.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._flatten_trivial_tuplets

    @property
    def is_diminution(self):
        r'''Is true when tuplet should be spelled as diminution. Otherwise
        false.

        Defaults to true.

        Set to true or false.

        Returns true or false.
        '''
        return self._is_diminution

    @property
    def preferred_denominator(self):
        r'''Gets preferred denominator.

        Defaults to none.

        Set to ``'divisions'``, duration, integer or none.

        Returns ``'divisions'``, duration, integer or none.
        '''
        return self._preferred_denominator

    @property
    def rewrite_rest_filled_tuplets(self):
        r'''Is true when tuplet spelling should flatten rest-filled tuplets.
        Otherwise false.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._rewrite_rest_filled_tuplets

    @property
    def simplify_redundant_tuplets(self):
        r'''Is true when tuplets should be simplified. Otherwise false.

        Defaults to false.

        Set to true or false

        Returns true or false.
        '''
        return self._simplify_redundant_tuplets

    @property
    def use_note_duration_bracket(self):
        r'''Is true when tuplet should override tuplet number text with note
        duration bracket giving tuplet duration. Otherwise false.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._use_note_duration_bracket