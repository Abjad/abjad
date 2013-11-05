# -*- encoding: utf-8 -*-

from abjad.tools.abctools import AbjadObject
from abjad.tools.functiontools import override


class LilyPondFormatManager(AbjadObject):

    ### PUBLIC METHODS ###

    @staticmethod
    def format_lilypond_attribute(attribute):
        r'''Formats LilyPond attribute according to Scheme formatting
        conventions.

        Returns string.
        '''
        attribute = attribute.replace('__', " #'")
        result = attribute.replace('_', '-')
        result = "#'%s" % result
        return result

    @staticmethod
    def format_lilypond_value(expr):
        r'''Formats LilyPond `expr` according to Scheme formatting conventions.

        Returns string.
        '''
        from abjad.tools import schemetools
        if '_lilypond_format' in dir(expr) and not isinstance(expr, str):
            pass
        elif expr in (True, False):
            expr = schemetools.Scheme(expr)
        elif expr in (Up, Down, Left, Right, Center):
            expr = schemetools.Scheme(repr(expr).lower())
        elif isinstance(expr, int) or isinstance(expr, float):
            expr = schemetools.Scheme(expr)
        elif expr in (
            'black',
            'blue',
            'center',
            'cyan',
            'darkblue',
            'darkcyan',
            'darkgreen',
            'darkmagenta',
            'darkred',
            'darkyellow',
            'down',
            'green',
            'grey',
            'left',
            'magenta',
            'red',
            'right',
            'up',
            'white',
            'yellow',
            ):
            expr = schemetools.Scheme(expr)
        elif isinstance(expr, str) and '::' in expr:
            expr = schemetools.Scheme(expr)
        elif isinstance(expr, tuple):
            expr = schemetools.SchemePair(expr[0], expr[1])
        elif isinstance(expr, str):
            if ' ' not in expr:
                expr = schemetools.Scheme(expr, quoting="'")
            else:
                expr = schemetools.Scheme(expr)
        else:
            expr = schemetools.Scheme(expr, quoting="'")
        return format(expr)

    @staticmethod
    def get_grob_override_format_contributions(component):
        r'''Get grob override format contributions for `component`.

        Returns alphabetized list of LilyPond grob overrides.
        '''
        from abjad.tools.scoretools.Leaf import Leaf
        result = []
        is_once = False
        if isinstance(component, Leaf):
            is_once = True
        result.extend(override(component)._list_format_contributions(
            'override', is_once=is_once))
        for string in result[:]:
            if 'NoteHead' in string and 'pitch' in string:
                result.remove(string)
        result = ['grob overrides', result]
        return result

    @staticmethod
    def get_grob_revert_format_contributions(component):
        '''Get grob revert format contributions.

        Returns alphabetized list of LilyPond grob reverts.
        '''
        from abjad.tools.scoretools.Leaf import Leaf

        result = []
        if not isinstance(component, Leaf):
            result.extend(override(component)._list_format_contributions(
                'revert'))
        return ['grob reverts', result]
