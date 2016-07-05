# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LilyPondFormatManager(AbjadObject):
    r'''Manages LilyPond formatting logic.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'LilyPond formatting'

    lilypond_color_constants = (
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
        )

    indent = '    '

    ### PRIVATE METHODS ###

    @staticmethod
    def _collect_indicators(component):
        from abjad.tools import markuptools
        from abjad.tools.topleveltools import inspect_
        expressions = []
        for parent in inspect_(component).get_parentage(include_self=True):
            result = inspect_(parent).get_indicators(unwrap=False)
            expressions.extend(result)
            result = parent._get_spanner_indicators(unwrap=False)
            expressions.extend(result)
        up_markup = []
        down_markup = []
        neutral_markup = []
        scoped_expressions = []
        nonscoped_expressions = []
        # classify expressions attached to component
        for expression in expressions:
            # skip nonprinting indicators like annotation
            indicator = expression.indicator
            if not hasattr(indicator, '_lilypond_format') and \
                not hasattr(indicator, '_get_lilypond_format_bundle'):
                continue
            elif expression.is_annotation:
                continue
            # skip comments and commands unless attached directly to us
            elif expression.scope is None and \
                hasattr(expression.indicator, '_format_leaf_children') and \
                not getattr(expression.indicator, '_format_leaf_children') and\
                expression.component is not component:
                continue
            # store markup
            elif isinstance(expression.indicator, markuptools.Markup):
                if expression.indicator.direction == Up:
                    up_markup.append(expression.indicator)
                elif expression.indicator.direction == Down:
                    down_markup.append(expression.indicator)
                elif expression.indicator.direction in (Center, None):
                    neutral_markup.append(expression.indicator)
            # store scoped expressions
            elif expression.scope is not None:
                if expression._is_formattable_for_component(component):
                    scoped_expressions.append(expression)
            # store nonscoped expressions
            else:
                nonscoped_expressions.append(expression)
        indicators = (
            up_markup,
            down_markup,
            neutral_markup,
            scoped_expressions,
            nonscoped_expressions,
            )
        return indicators

    @staticmethod
    def _populate_context_setting_format_contributions(component, bundle):
        result = []
        from abjad.tools.topleveltools import set_
        from abjad.tools import scoretools
        manager = LilyPondFormatManager
        if isinstance(component, scoretools.Context):
            for name, value in vars(set_(component)).items():
                string = manager.format_lilypond_context_setting_in_with_block(
                    name, value)
                result.append(string)
        #if isinstance(component, (scoretools.Leaf, scoretools.Measure)):
        else:
            contextualizer = set_(component)
            variables = vars(contextualizer)
            for name, value in variables.items():
                # if we've found a leaf context namespace
                if name.startswith('_'):
                    for x, y in vars(value).items():
                        if not x.startswith('_'):
                            string = \
                                manager.format_lilypond_context_setting_inline(
                                    x, y, name)
                            result.append(string)
                # otherwise we've found a default leaf context setting
                else:
                    # parse default context setting
                    string = manager.format_lilypond_context_setting_inline(
                        name, value)
                    result.append(string)
        result.sort()
        bundle.context_settings.extend(result)

    @staticmethod
    def _populate_grob_override_format_contributions(component, bundle):
        from abjad.tools import scoretools
        from abjad.tools.topleveltools.override import override
        result = []
        is_once = isinstance(component, scoretools.Leaf)
        contributions = override(component)._list_format_contributions(
            'override',
            is_once=is_once,
            )
        for string in result[:]:
            if 'NoteHead' in string and 'pitch' in string:
                contributions.remove(string)
        bundle.grob_overrides.extend(contributions)

    @staticmethod
    def _populate_grob_revert_format_contributions(component, bundle):
        from abjad.tools import scoretools
        from abjad.tools.topleveltools.override import override
        if not isinstance(component, scoretools.Leaf):
            manager = override(component)
            contributions = manager._list_format_contributions('revert')
            bundle.grob_reverts.extend(contributions)

    @staticmethod
    def _populate_indicator_format_contributions(component, bundle):
        manager = LilyPondFormatManager
        (
            up_markup,
            down_markup,
            neutral_markup,
            scoped_expressions,
            nonscoped_expressions,
            ) = LilyPondFormatManager._collect_indicators(component)
        manager._populate_markup_format_contributions(
            component,
            bundle,
            up_markup,
            down_markup,
            neutral_markup,
            )
        manager._populate_scoped_expression_format_contributions(
            component,
            bundle,
            scoped_expressions,
            )
        manager._populate_nonscoped_expression_format_contributions(
            component,
            bundle,
            nonscoped_expressions,
            )

    @staticmethod
    def _populate_markup_format_contributions(
        component,
        bundle,
        up_markup,
        down_markup,
        neutral_markup,
        ):
        from abjad.tools import markuptools
        for markup_list in (up_markup, down_markup, neutral_markup):
            if not markup_list:
                continue
            elif 1 < len(markup_list):
                direction = markup_list[0].direction
                if direction is None:
                    direction = '-'
                markup_list = markup_list[:]
                markup_list.sort(key=lambda x: -x.stack_priority)
                markup = markuptools.Markup.column(
                    markup_list,
                    direction=direction,
                    )
                format_pieces = markup._get_format_pieces()
                bundle.right.markup.extend(format_pieces)
            else:
                if markup_list[0].direction is None:
                    markup = markuptools.Markup(markup_list[0], direction='-')
                    format_pieces = markup._get_format_pieces()
                    bundle.right.markup.extend(format_pieces)
                else:
                    format_pieces = markup_list[0]._get_format_pieces()
                    bundle.right.markup.extend(format_pieces)

    @staticmethod
    def _populate_nonscoped_expression_format_contributions(
        component,
        bundle,
        nonscoped_expressions,
        ):
        for nonscoped_expression in nonscoped_expressions:
            indicator = nonscoped_expression.indicator
            if hasattr(indicator, '_get_lilypond_format_bundle'):
                indicator_bundle = indicator._get_lilypond_format_bundle(
                    component)
                if indicator_bundle is not None:
                    bundle.update(indicator_bundle)

    @staticmethod
    def _populate_scoped_expression_format_contributions(
        component,
        bundle,
        scoped_expressions,
        ):
        for scoped_expression in scoped_expressions:
            format_pieces = scoped_expression._get_format_pieces()
            if isinstance(format_pieces, type(bundle)):
                bundle.update(format_pieces)
            else:
                format_slot = scoped_expression.indicator._format_slot
                bundle.get(format_slot).indicators.extend(format_pieces)

    @staticmethod
    def _populate_spanner_format_contributions(
        component,
        bundle,
        ):
        pairs = []
        for spanner in component._get_parentage()._get_spanners():
            spanner_bundle = spanner._get_lilypond_format_bundle(component)
            pair = (spanner, spanner_bundle)
            pairs.append(pair)
        pairs.sort(key=lambda x: type(x[0]).__name__)
        for spanner, spanner_bundle in pairs:
            bundle.update(spanner_bundle)

    ### PUBLIC METHODS ###

    @staticmethod
    def bundle_format_contributions(component):
        r'''Gets all format contributions for `component`.

        Returns LilyPond format bundle.
        '''
        from abjad.tools import systemtools
        manager = LilyPondFormatManager
        bundle = systemtools.LilyPondFormatBundle()
        manager._populate_indicator_format_contributions(component, bundle)
        manager._populate_spanner_format_contributions(component, bundle)
        manager._populate_context_setting_format_contributions(
            component, bundle)
        manager._populate_grob_override_format_contributions(component, bundle)
        manager._populate_grob_revert_format_contributions(component, bundle)
        bundle.alphabetize()
        bundle.make_immutable()
        return bundle

    @staticmethod
    def format_lilypond_attribute(attribute):
        r'''Formats LilyPond attribute according to Scheme formatting
        conventions.

        Returns string.
        '''
        assert isinstance(attribute, str), repr(attribute)
        attribute = attribute.replace('__', ".")
        result = attribute.replace('_', '-')
        return result

    @staticmethod
    def format_lilypond_context_setting_in_with_block(name, value):
        r'''Formats LilyPond context setting `name` with `value`
        in LilyPond with-block.

        Returns string.
        '''
        assert isinstance(name, str), repr(name)
        name = name.split('_')
        first = name[0:1]
        rest = name[1:]
        rest = [x.title() for x in rest]
        name = first + rest
        name = ''.join(name)
        value = LilyPondFormatManager.format_lilypond_value(value)
        value_parts = value.split('\n')
        result = r'{!s} = {!s}'.format(name, value_parts[0])
        result = [result]
        for part in value_parts[1:]:
            result.append(LilyPondFormatManager.indent + part)
        return '\n'.join(result)

    @staticmethod
    def format_lilypond_context_setting_inline(name, value, context=None):
        r'''Formats LilyPond context setting `name` with `value` in
        `context`.

        Returns string.
        '''
        name = name.split('_')
        first = name[0:1]
        rest = name[1:]
        rest = [x.title() for x in rest]
        name = first + rest
        name = ''.join(name)
        value = LilyPondFormatManager.format_lilypond_value(value)
        if context is not None:
            context_string = context[1:]
            context_string = context_string.split('_')
            context_string = [x.title() for x in context_string]
            context_string = ''.join(context_string)
            context_string += '.'
        else:
            context_string = ''
        result = r'\set {}{} = {}'
        result = result.format(context_string, name, value)
        return result

    @staticmethod
    def format_lilypond_value(expr):
        r'''Formats LilyPond `expr` according to Scheme formatting
        conventions.

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
        elif expr in LilyPondFormatManager.lilypond_color_constants:
            expr = schemetools.Scheme(expr)
        elif isinstance(expr, str) and '::' in expr:
            expr = schemetools.Scheme(expr)
        elif isinstance(expr, tuple) and len(expr) == 2:
            expr = schemetools.SchemePair(expr[0], expr[1])
        elif isinstance(expr, str) and ' ' not in expr:
            expr = schemetools.Scheme(expr, quoting="'")
        elif isinstance(expr, str) and ' ' in expr:
            expr = schemetools.Scheme(expr)
        else:
            expr = schemetools.Scheme(expr, quoting="'")
        return format(expr, 'lilypond')

    @staticmethod
    def make_lilypond_override_string(
        grob_name,
        grob_attribute,
        grob_value,
        context_name=None,
        is_once=False,
        ):
        '''Makes Lilypond override string.

        Does not include 'once'.

        Returns string.
        '''
        from abjad.tools import stringtools
        # parse input strings
        grob_name = stringtools.to_upper_camel_case(grob_name)
        grob_attribute = LilyPondFormatManager.format_lilypond_attribute(
            grob_attribute)
        grob_value = LilyPondFormatManager.format_lilypond_value(grob_value)
        if context_name is not None:
            context_prefix = \
                stringtools.to_upper_camel_case(context_name)
            context_prefix += '.'
        else:
            context_prefix = ''
        if is_once:
            once_prefix = r'\once '
        else:
            once_prefix = ''
        # return override string
        result = r'{}\override {}{}.{} = {}'
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
        from abjad.tools import stringtools
        # parse input strings
        grob_name = stringtools.to_upper_camel_case(grob_name)
        grob_attribute = LilyPondFormatManager.format_lilypond_attribute(
            grob_attribute)
        # change #'bound-details #'left #'text to #'bound-details
        grob_attribute = grob_attribute.split('.')[0]
        context_prefix = ''
        if context_name is not None:
            context_prefix = stringtools.to_upper_camel_case(context_name)
            context_prefix += '.'
        # format revert string
        result = r'\revert {}{}.{}'
        result = result.format(context_prefix, grob_name, grob_attribute)
        # return revert string
        return result

    @staticmethod
    def report_component_format_contributions(component, verbose=False):
        r'''Reports `component` format contributions.

            >>> staff = Staff("c'4 [ ( d'4 e'4 f'4 ] )")
            >>> override(staff[0]).note_head.color = 'red'

        ::

            >>> manager = systemtools.LilyPondFormatManager
            >>> print(manager.report_component_format_contributions(staff[0]))
            slot 1:
                grob overrides:
                    \once \override NoteHead.color = #red
            slot 3:
            slot 4:
                leaf body:
                    c'4 [ (
            slot 5:
            slot 7:

        Returns string.
        '''
        return component._report_format_contributors()

    @staticmethod
    def report_spanner_format_contributions(spanner):
        r'''Reports spanner format contributions for every leaf
        to which spanner attaches.

            >>> staff = Staff("c8 d e f")
            >>> spanner = spannertools.Beam()
            >>> attach(spanner, staff[:])

        ::

            >>> manager = systemtools.LilyPondFormatManager
            >>> print(manager.report_spanner_format_contributions(spanner))
            c8	systemtools.LilyPondFormatBundle(
                    right=LilyPondFormatBundle.SlotContributions(
                        spanner_starts=['['],
                        ),
                    )
            d8	systemtools.LilyPondFormatBundle()
            e8	systemtools.LilyPondFormatBundle()
            f8	systemtools.LilyPondFormatBundle(
                    right=LilyPondFormatBundle.SlotContributions(
                        spanner_stops=[']'],
                        ),
                    )

        Returns none or return string.
        '''
        result = []
        for leaf in spanner._get_leaves():
            bundle = spanner._get_lilypond_format_bundle(leaf)
            bundle_pieces = format(bundle).split('\n')
            result.append('{!s}\t{}'.format(leaf, bundle_pieces[0]))
            for piece in bundle_pieces[1:]:
                result.append('\t{}'.format(piece))
        result = '\n'.join(result)
        return result
