# -*- encoding: utf-8 -*-

import inspect

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
        result = LilyPondFormatManager.get_all_mark_format_contributions(
            component)
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
        overrides = \
            LilyPondFormatManager.get_grob_override_format_contributions(
                component)[1]
        if overrides:
            result['grob overrides'] = overrides
        reverts = LilyPondFormatManager.get_grob_revert_format_contributions(
            component)[1]
        if reverts:
            result['grob reverts'] = reverts
        return result

    @staticmethod
    def get_all_mark_format_contributions(component):
        r'''Get all mark format contributions as nested dictionaries.

        The first level of keys represent format slots.

        The second level of keys represent format contributor
        ('articulations', 'markup', etc.).

        Returns dict.
        '''
        from abjad.tools import formattools
        from abjad.tools import marktools
        from abjad.tools import markuptools
        class_to_section = {
            marktools.Articulation: ('articulations', False),
            marktools.BendAfter: ('articulations', False),
            marktools.LilyPondCommandMark: ('lilypond command marks', False),
            marktools.LilyPondComment: ('comments', False),
            marktools.StemTremolo: ('stem tremolos', True),
            }
        contributions = {}
        marks = component._get_marks()
        up_markup, down_markup, neutral_markup = [], [], []
        context_marks = []
        ### organize marks attached directly to component ###
        for mark in marks:
            ### non-printing marks are skipped (i.e. Annotation) ###
            if not hasattr(mark, '_lilypond_format'):
                continue
            ### a recognized mark class ###
            section, singleton = None, False
            if mark.__class__ in class_to_section:
                section, singleton = class_to_section[mark.__class__]
            ### context marks to be dealt with later ###
            elif isinstance(mark, marktools.ContextMark):
                if formattools.is_formattable_context_mark_for_component(
                    mark, component):
                    context_marks.append(mark)
                    continue
            ### markup to be dealt with later ###
            elif isinstance(mark, markuptools.Markup):
                if mark.direction is Up:
                    up_markup.append(mark)
                elif mark.direction is Down:
                    down_markup.append(mark)
                elif mark.direction in (Center, None):
                    neutral_markup.append(mark)
                continue
            ### otherwise, test if mark is a subclass of a recognized mark ###
            else:
                mro = list(inspect.getmro(mark.__class__))
                while mro:
                    if mro[-1] in class_to_section:
                        section, singleton = class_to_section[mro[-1]]
                    mro.pop()
                if not section:
                    section, singleton = 'other marks', False
            ### prepare the contributions dictionary ###
            format_slot = mark._format_slot
            if format_slot not in contributions:
                contributions[format_slot] = {}
            if section not in contributions[format_slot]:
                contributions[format_slot][section] = []
            ### add the mark contribution ###
            contribution_list = contributions[format_slot][section]
            if len(contribution_list) and singleton:
                raise ExtraMarkError
            result = mark._lilypond_format
            assert isinstance(result, str)
            contribution_list.append(result)
            if section == 'articulations':
                contribution_list.sort()
        ### handle context marks ###
        for parent in component._get_parentage(include_self=False):
            for mark in parent._start_marks:
                if not isinstance(mark, marktools.ContextMark):
                    continue
                if mark in context_marks:
                    continue
                if formattools.is_formattable_context_mark_for_component(
                    mark, component):
                    context_marks.append(mark)
        #for candidate in context_mark_candidates:
        #    if candidate not in context_marks:
        #            context_marks.append(candidate)
        section = 'context marks'
        for mark in context_marks:
            format_slot = mark._format_slot
            result = formattools.get_context_mark_format_pieces(mark)
            if format_slot not in contributions:
                contributions[format_slot] = {}
            if section not in contributions[format_slot]:
                contributions[format_slot][section] = []
            contributions[format_slot][section].extend(result)
        ### handle markup ###
        result = []
        for markup_list in (up_markup, down_markup, neutral_markup):
            if not markup_list:
                pass
            elif 1 < len(markup_list):
                contents = []
                for m in markup_list:
                    contents += m.contents
                direction = markup_list[0].direction
                if direction is None:
                    direction = '-'
                command = markuptools.MarkupCommand('column', contents)
                markup = markuptools.Markup(command, direction=direction)
                result.extend(markup._get_format_pieces(is_indented=True))
            else:
                if markup_list[0].direction is None:
                    markup = markuptools.Markup(markup_list[0])
                    markup.direction = '-'
                    result.extend(markup._get_format_pieces(is_indented=True))
                else:
                    result.extend(markup_list[0]._get_format_pieces(
                        is_indented=True))
        if result:
            if 'right' not in contributions:
                contributions['right'] = {}
            contributions['right']['markup'] = result
        for slot in contributions:
            for kind, value in contributions[slot].iteritems():
                contributions[slot][kind] = tuple(value)
        return contributions

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
