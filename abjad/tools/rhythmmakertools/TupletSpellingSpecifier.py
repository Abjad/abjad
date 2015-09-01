# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class TupletSpellingSpecifier(AbjadValueObject):
    r'''Tuplet spelling specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_avoid_dots',
        '_flatten_trivial_tuplets',
        '_is_diminution',
        '_simplify_tuplets',
        '_use_note_duration_bracket',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        avoid_dots=False,
        flatten_trivial_tuplets=False,
        is_diminution=True,
        simplify_tuplets=False,
        use_note_duration_bracket=False,
        ):
        # TODO: Consider renaming is_diminution=True to is_augmentation=None.
        #       That would allow for all keywords to default to None,
        #       and therefore a single-line storage format.
        self._avoid_dots = bool(avoid_dots)
        self._flatten_trivial_tuplets = bool(flatten_trivial_tuplets)
        self._is_diminution = bool(is_diminution)
        self._simplify_tuplets = bool(simplify_tuplets)
        self._use_note_duration_bracket = bool(use_note_duration_bracket)

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
    def simplify_tuplets(self):
        r'''Is true when tuplets should be simplified. Otherwise false.

        Defaults to false.

        Set to true or false

        Returns true or false.
        '''
        return self._simplify_tuplets

    @property
    def use_note_duration_bracket(self):
        r'''Is true when tuplet should override tuplet number text with note
        duration bracket giving tuplet duration. Otherwise false.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._use_note_duration_bracket