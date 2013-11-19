# -*- encoding: utf-8 -*-


class LilyPondFormatManager(object):
    r'''Manages LilyPond formatting logic.
    '''

    ### CLASS VARIABLES ###

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

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_context_mark_format_pieces(context_mark):
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        assert isinstance(context_mark, indicatortools.ContextMark), \
            repr(context_mark)
        addenda = []
        context_mark_format = context_mark._lilypond_format
        if isinstance(context_mark_format, (tuple, list)):
            addenda.extend(context_mark_format)
        else:
            addenda.append(context_mark_format)
        if context_mark._get_effective_context() is not None:
            return addenda
        if isinstance(context_mark, indicatortools.TimeSignature):
            if isinstance(context_mark._start_component, scoretools.Measure):
                return addenda
        addenda = [r'%%% {} %%%'.format(x) for x in addenda]
        return addenda

    @staticmethod
    def _is_formattable_context_mark(mark, component):
        from abjad.tools import scoretools
        from abjad.tools import indicatortools
        if mark._start_component is None:
            return False
        if isinstance(mark._start_component, scoretools.Measure):
            if mark._start_component is component:
                if not isinstance(mark, indicatortools.TimeSignature):
                    return True
                elif component.always_format_time_signature:
                    return True
                else:
                    previous_measure = \
                        scoretools.get_previous_measure_from_component(
                            mark._start_component)
                    if previous_measure is not None:
                        previous_effective_time_signature = \
                            previous_measure.time_signature
                    else:
                        previous_effective_time_signature = None
                    if not mark == previous_effective_time_signature:
                        return True
        elif mark._format_slot == 'right':
            if mark._start_component is component:
                return True
        elif mark._start_component is component:
            return True
        else:
            if mark._get_effective_context() in \
                component._get_parentage(include_self=True):
                if mark._get_effective_context() not in \
                    component._get_parentage(include_self=False):
                    if mark._start_component.start == component.start:
                        return True
        return False

    @staticmethod
    def _populate_mark_format_contributions(component, bundle):
        from abjad.tools import indicatortools
        from abjad.tools import markuptools
        from abjad.tools import systemtools
        from abjad.tools.agenttools.InspectionAgent import inspect
        manager = LilyPondFormatManager
        items = component._get_context_marks() + component._get_indicators()
        up_markup, down_markup, neutral_markup = [], [], []
        context_marks = []
        wrappers = []
        # organize items attached to component
        for item in items:
            format_slot_subsection = None
            # skip nonprinting items like annotation
            if not hasattr(item, '_lilypond_format'):
                continue
            if isinstance(item, indicatortools.Articulation):
                format_slot_subsection = 'articulations'
            elif isinstance(item, indicatortools.BarLine):
                format_slot_subsection = 'commands'
            elif isinstance(item, indicatortools.BendAfter):
                format_slot_subsection = 'articulations'
            elif isinstance(item, indicatortools.LilyPondCommand):
                format_slot_subsection = 'commands'
            elif isinstance(item, indicatortools.LilyPondComment):
                format_slot_subsection = 'comments'
            elif isinstance(item, indicatortools.StemTremolo):
                format_slot_subsection = 'stem_tremolos'
            # store formattable context marks attached to component
            elif isinstance(item, indicatortools.ContextMark):
                if manager._is_formattable_context_mark(item, component):
                    context_marks.append(item)
                continue
            # store wrappers for later handling
            elif isinstance(item, indicatortools.IndicatorWrapper):
                wrappers.append(item)
                continue
            # store markup for later handling
            elif isinstance(item, markuptools.Markup):
                if item.direction is Up:
                    up_markup.append(item)
                elif item.direction is Down:
                    down_markup.append(item)
                elif item.direction in (Center, None):
                    neutral_markup.append(item)
                continue
            # otherwise the item is something else
            else:
                message = 'can not identify where to put item: {!r}.'
                message = message.format(item)
                raise Exception(message)
            format_slot = item._format_slot
            format_slot = bundle.get(format_slot)
            contributions = format_slot.get(format_slot_subsection)
            contribution = item._lilypond_format
            contributions.append(contribution)
            if format_slot_subsection == 'articulations':
                contributions.sort()
        # add formattable context marks attached to parents of component
        for parent in inspect(component).get_parentage(include_self=False):
            for context_mark in parent._start_context_marks:
                assert isinstance(context_mark, indicatortools.ContextMark)
                if context_mark in context_marks:
                    continue
                if manager._is_formattable_context_mark(context_mark, component):
                    context_marks.append(context_mark)
        # handle context marks
        for context_mark in context_marks:
            assert isinstance(context_mark, indicatortools.ContextMark)
            format_pieces = manager._get_context_mark_format_pieces(context_mark)
            format_slot = context_mark._format_slot
            bundle.get(format_slot).context_marks.extend(format_pieces)
        # TODO: insert wrapper handling code here
        # handle markup
        for markup_list in (up_markup, down_markup, neutral_markup):
            if not markup_list:
                continue
            elif 1 < len(markup_list):
                contents = []
                for markup in markup_list:
                    contents += markup.contents
                direction = markup_list[0].direction
                if direction is None:
                    direction = '-'
                command = markuptools.MarkupCommand('column', contents)
                markup = markuptools.Markup(command, direction=direction)
                format_pieces = markup._get_format_pieces()
                bundle.right.markup[:] = format_pieces
            else:
                if markup_list[0].direction is None:
                    markup = markuptools.Markup(markup_list[0], direction='-')
                    format_pieces = markup._get_format_pieces()
                    bundle.right.markup[:] = format_pieces
                else:
                    format_pieces = markup_list[0]._get_format_pieces()
                    bundle.right.markup[:] = format_pieces

    @staticmethod
    def _populate_context_setting_format_contributions(component, bundle):
        result = []
        from abjad.tools.topleveltools import contextualize
        from abjad.tools import scoretools
        manager = LilyPondFormatManager
        if isinstance(component, (scoretools.Leaf, scoretools.Measure)):
            for name, value in vars(contextualize(component)).iteritems():
                # if we've found a leaf context namespace
                if name.startswith('_'):
                    for x, y in vars(value).iteritems():
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
        else:
            for name, value in vars(contextualize(component)).iteritems():
                string = manager.format_lilypond_context_setting_in_with_block(
                    name, value)
                result.append(string)
        result.sort()
        bundle.context_settings[:] = result

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
        bundle.grob_overrides[:] = contributions

    @staticmethod
    def _populate_grob_revert_format_contributions(component, bundle):
        from abjad.tools import scoretools
        from abjad.tools.topleveltools.override import override
        if not isinstance(component, scoretools.Leaf):
            manager = override(component)
            contributions = manager._list_format_contributions('revert')
            bundle.grob_reverts[:] = contributions

    @staticmethod
    def _populate_spanner_format_contributions(component, bundle):
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools.override import override
        result = {
            'after': [],
            'before': [],
            'closing': [],
            'opening': [],
            'right': [],
        }
        if isinstance(component, scoretools.Container):
            before_contributions = result['before']
            after_contributions = result['after']
        else:
            before_contributions = result['opening']
            after_contributions = result['closing']
        stop_contributions = []
        other_contributions = []
        for spanner in component._get_parentage()._get_spanners():
            # override contributions (in before slot)
            if spanner._is_my_first_leaf(component):
                contributions = override(spanner)._list_format_contributions(
                    'override', 
                    is_once=False,
                    )
                for contribution in contributions:
                    before_contributions.append((spanner, contribution, None))
            # contributions for before slot
            for contribution in spanner._format_before_leaf(component):
                before_contributions.append((spanner, contribution, None))
            # contributions for after slot
            contributions = spanner._format_after_leaf(component)
            for contribution in contributions:
                after_contributions.append((spanner, contribution, None))
            # revert contributions (in after slot)
            if spanner._is_my_last_leaf(component):
                manager = override(spanner)
                contributions = manager._list_format_contributions('revert')
                for contribution in contributions:
                    triple = (spanner, contribution, None)
                    if triple not in after_contributions:
                        after_contributions.append(triple)
            # contributions for right slot
            contributions = spanner._format_right_of_leaf(component)
            if contributions:
                if spanner._is_my_last_leaf(component):
                    for contribution in contributions:
                        triple = (spanner, contribution, None)
                        stop_contributions.append(triple)
                else:
                    for contribution in contributions:
                        triple = (spanner, contribution, None)
                        other_contributions.append(triple)
        result['right'] = stop_contributions + other_contributions
        for key in result.keys():
            if not result[key]:
                del(result[key])
            else:
                result[key].sort(key=lambda x: x[0].__class__.__name__)
                result[key] = [x[1] for x in result[key]]
        for format_slot, contributions in result.iteritems():
            # contributions can no be any of these:
            # 1 contribution: (')',)
            # 2 contributions: ('[', '(')
            # 3 contributions: ('[', '(', '~')
            # 4 contributions: ('[', ']', '(', ')')
            # and so on such that no length constraint can be assumed
            if isinstance(contributions, list):
                contributions = tuple(contributions)
            assert isinstance(contributions, tuple), repr(contributions)
            bundle.get(format_slot).spanners[:] = contributions

    ### PUBLIC METHODS ###

    @staticmethod
    def bundle_format_contributions(component):
        r'''Gets all format contributions for `component`.

        Returns LilyPond format bundle.
        '''
        from abjad.tools import systemtools
        manager = LilyPondFormatManager
        bundle = systemtools.LilyPondFormatBundle()
        manager._populate_mark_format_contributions(component, bundle)
        manager._populate_spanner_format_contributions(component, bundle)
        manager._populate_context_setting_format_contributions(component, bundle)
        manager._populate_grob_override_format_contributions(component, bundle)
        manager._populate_grob_revert_format_contributions(component, bundle)
        bundle.make_immutable()
        return bundle

    @staticmethod
    def format_lilypond_attribute(attribute):
        r'''Formats LilyPond attribute according to Scheme formatting
        conventions.

        Returns string.
        '''
        assert isinstance(attribute, str), repr(attribute)
        attribute = attribute.replace('__', " #'")
        result = attribute.replace('_', '-')
        result = "#'{}".format(result)
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
            result.append('\t' + part)
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
        elif isinstance(expr, tuple):
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
        from abjad.tools import stringtools
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

    @staticmethod
    def report_component_format_contributions(component, verbose=False):
        r'''Reports `component` format contributions.

            >>> staff = Staff("c'4 [ ( d'4 e'4 f'4 ] )")
            >>> override(staff[0]).note_head.color = 'red'

        ::

            >>> print systemtools.LilyPondFormatManager.report_component_format_contributions(staff[0])
            slot 1:
                grob overrides:
                    \once \override NoteHead #'color = #red
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

            >>> print systemtools.LilyPondFormatManager.report_spanner_format_contributions(spanner)
            c8  before: []
                after: []
                right: ['[']
            <BLANKLINE>
            d8  before: []
                after: []
                right: []
            <BLANKLINE>
            e8  before: []
                after: []
                right: []
            <BLANKLINE>
            f8  before: []
                after: []
                right: [']']

        Returns none or return string.
        '''
        result = ''
        for leaf in spanner.leaves:
            result += str(leaf)
            result += '\tbefore: %s\n' % spanner._format_before_leaf(leaf)
            result += '\t after: %s\n' % spanner._format_after_leaf(leaf)
            result += '\t right: %s\n' % spanner._format_right_of_leaf(leaf)
            result += '\n'
        if result[-1] == '\n':
            result = result[:-1]
        return result
