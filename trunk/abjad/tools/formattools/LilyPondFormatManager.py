# -*- encoding: utf-8 -*-

from abjad.tools.abctools import AbjadObject


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

        if '_lilypond_format' in dir(expr) and not isinstance(expr, str):
            return format(expr)
        elif expr is True:
            return '##t'
        elif expr is False:
            return '##f'
        elif expr is Up:
            return '#up'
        elif expr is Down:
            return '#down'
        elif expr is Left:
            return '#left'
        elif expr is Right:
            return '#right'
        elif expr is Center:
            return '#center'
        elif isinstance(expr, int) or isinstance(expr, float) or expr in (
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
            return '#%s' % expr
        elif isinstance(expr, str) and '::' in expr:
            return '#%s' % expr
        elif isinstance(expr, tuple):
            return "#'(%s . %s)" % expr
        elif isinstance(expr, str) and ' ' not in expr:
            return "#'%s" % expr
        elif isinstance(expr, str) and ' ' in expr:
            return '"%s"' % expr
        else:
            return "#'%s" % expr
