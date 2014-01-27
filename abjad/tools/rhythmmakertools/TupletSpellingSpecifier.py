# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class TupletSpellingSpecifier(AbjadObject):
    r'''Tuplet spelling specifier.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_avoid_dots',
        '_is_diminution',
        '_is_fixed_duration',
        '_rewrite_improper_ratios',
        )

    _attribute_manifest = (
        'is_diminution',
        'is_fixed_duration',
        'avoid_dots',
        'rewrite_improper_ratios',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        avoid_dots=False,
        is_diminution=True,
        is_fixed_duration=False,
        rewrite_improper_ratio=True,
        ):
        assert isinstance(avoid_dots, bool), avoid_dots
        assert isinstance(is_diminution, bool), is_diminution
        assert isinstance(is_fixed_duration, bool), is_fixed_duration
        assert isinstance(rewrite_improper_ratios, bool)
        self._avoid_dots = avoid_dots
        self._is_diminution = is_diminution
        self._is_fixed_duration = is_fixed_duration
        self._rewrite_improper_ratio = rewrite_improper_ratio

    ### SPECIAL METHODS ###

    def __makenew__(self, *args, **kwargs):
        r'''Makes new tuplet spelling specifier with optional `kwargs`.

        Returns new tuplet spelling specifier.
        '''
        assert not args
        arguments = {}
        for attribute_name in self._attribute_manifest:
            arguments[attribute_name] = getattr(self, attribute_name)
        arguments.update(kwargs)
        return type(self)(**arguments)

    ### PUBLIC PROPERTIES ###

    @property
    def avoid_dots(self):
        r'''Is true when tuplet spelling should avoid dotted rhythmic values.
        Otherwise false.

        Defaults to false.

        Returns boolean.
        '''
        return self._avoid_dots

    @property
    def is_diminution(self):
        r'''Is true when tuplet should be spelled as diminution. Otherwise
        false.

        Defaults to true.

        Returns boolean.
        '''
        return self._is_diminution

    @property
    def is_fixed_duration(self):
        r'''Is true when tuplet should be spelled as fixed-duration. Otherwise
        false.

        Defaults to false.

        Returns boolean.
        '''
        return self._is_fixed_duration

    @property
    def rewrite_improper_ratio(self):
        r'''Is true when tuplet should spell ratio strictly greater than 
        ``1/2`` and strictly less than ``2``.
       
        Defaults to true.

        Returns boolean.
        '''
        return self._rewrite_improper_ratio
