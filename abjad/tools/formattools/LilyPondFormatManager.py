# -*- encoding: utf-8 -*-

from abjad.tools import stringtools
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
    def get_all_format_contributions(component):
        r'''Get all format contributions for `component`.

        Returns nested dictionary.
        '''
        from abjad.tools import formattools
        result = formattools.get_all_mark_format_contributions(component)
        for slot, contributions in \
            formattools.get_spanner_format_contributions(
                component).iteritems():
            if slot not in result:
                result[slot] = {}
            result[slot]['spanners'] = contributions
        settings = formattools.get_context_setting_format_contributions(
            component)[1]
        if settings:
            result['context settings'] = settings
        overrides = LilyPondFormatManager.get_grob_override_format_contributions(component)[1]
        if overrides:
            result['grob overrides'] = overrides
        reverts = LilyPondFormatManager.get_grob_revert_format_contributions(component)[1]
        if reverts:
            result['grob reverts'] = reverts
        return result

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

    @staticmethod
    def make_lilypond_override_string(
        grob_name,
        grob_attribute,
        grob_value,
        context_name=None,
        is_once=False,
        ):
        '''Makes Lilypond override string.

        Does not include once indicator.

        Returns string.
        '''
        # parse input strings
        grob_name = stringtools.snake_case_to_upper_camel_case(grob_name)
        grob_attribute = LilyPondFormatManager.format_lilypond_attribute(
            grob_attribute)
        grob_value = LilyPondFormatManager.format_lilypond_value(grob_value)
        if context_name is not None:
            context_prefix = \
                stringtools.snake_case_to_upper_camel_case(context_name)
            context_prefix += '.'
        else:
            context_prefix = ''
        if is_once:
            once_prefix = r'\once '
        else:
            once_prefix = ''
        # return override string
        result = r'{}\override {}{} {} = {}'
        result = result.format(
            once_prefix,
            context_prefix,
            grob_name,
            grob_attribute,
            grob_value,
            )
        return result

    @staticmethod
    def make_lilypond_revert_string(
        grob_name, 
        grob_attribute, 
        context_name=None,
        ):
        '''Makes LilyPond revert string.

        Returns string.
        '''
        # parse input strings
        grob_name = stringtools.snake_case_to_upper_camel_case(grob_name)
        grob_attribute = LilyPondFormatManager.format_lilypond_attribute(
            grob_attribute)
        # change #'bound-details #'left #'text to #'bound-details
        grob_attribute = grob_attribute.split(' ')[0]
        context_prefix = ''
        if context_name is not None:
            context_prefix = \
                stringtools.snake_case_to_upper_camel_case(context_name)
            context_prefix += '.'
        # format revert string
        result = r'\revert {}{} {}'
        result = result.format(context_prefix, grob_name, grob_attribute)
        # return revert string
        return result
