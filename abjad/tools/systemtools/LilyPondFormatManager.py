# -*- encoding: utf-8 -*-
import inspect


class LilyPondFormatManager(object):
    r'''Manages LilyPond formatting logic.
    '''

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
    def format_lilypond_context_setting_in_with_block(name, value):
        r'''Formats LilyPond context setting `name` with `value`
        in with block.

        Returns string.
        '''
        name = name.split('_')
        first = name[0:1]
        rest = name[1:]
        rest = [x.title() for x in rest]
        name = first + rest
        name = ''.join(name)
        value = LilyPondFormatManager.format_lilypond_value(value)
        value_parts = value.split('\n')
        result = [r'{!s} = {!s}'.format(name, value_parts[0])]
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
        return format(expr, 'lilypond')

    @staticmethod
    def get_all_format_contributions(component):
        r'''Gets all format contributions for `component`.

        Returns nested dictionary.
        '''
        result = LilyPondFormatManager.get_all_mark_format_contributions(
            component)
        for slot, contributions in \
            LilyPondFormatManager.get_spanner_format_contributions(
                component).iteritems():
            if slot not in result:
                result[slot] = {}
            result[slot]['spanners'] = contributions
        settings = \
            LilyPondFormatManager.get_context_setting_format_contributions(
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
        r'''Gets all mark format contributions as nested dictionaries.

        The first level of keys represent format slots.

        The second level of keys represent format contributors
        (like 'articulations' and 'markup').

        Returns dictionary.
        '''
        from abjad.tools import marktools
        from abjad.tools import markuptools
        class_to_section = {
            marktools.Articulation: ('articulations', False),
            marktools.BendAfter: ('articulations', False),
            marktools.LilyPondCommand: ('lilypond command marks', False),
            marktools.LilyPondComment: ('comments', False),
            marktools.StemTremolo: ('stem tremolos', True),
            }
        contributions = {}
        marks = component._get_marks() + component._get_indicators()
        up_markup, down_markup, neutral_markup = [], [], []
        context_marks = []
        # organize marks attached directly to component
        for mark in marks:
            # nonprinting marks are skipped (eg, Annotation)
            if not hasattr(mark, '_lilypond_format'):
                continue
            # a recognized mark class
            section, singleton = None, False
            if mark.__class__ in class_to_section:
                section, singleton = class_to_section[mark.__class__]
            # context marks to be dealt with later
            elif isinstance(mark, marktools.ContextMark):
                if LilyPondFormatManager.is_formattable_context_mark_for_component(
                    mark, component):
                    context_marks.append(mark)
                    continue
            # markup to be dealt with later
            elif isinstance(mark, markuptools.Markup):
                if mark.direction is Up:
                    up_markup.append(mark)
                elif mark.direction is Down:
                    down_markup.append(mark)
                elif mark.direction in (Center, None):
                    neutral_markup.append(mark)
                continue
            # otherwise, test if mark is a subclass of a recognized mark
            else:
                mro = list(inspect.getmro(mark.__class__))
                while mro:
                    if mro[-1] in class_to_section:
                        section, singleton = class_to_section[mro[-1]]
                    mro.pop()
                if not section:
                    section, singleton = 'other marks', False
            # prepare the contributions dictionary
            format_slot = mark._format_slot
            if format_slot not in contributions:
                contributions[format_slot] = {}
            if section not in contributions[format_slot]:
                contributions[format_slot][section] = []
            # add the mark contribution
            contribution_list = contributions[format_slot][section]
            if len(contribution_list) and singleton:
                raise ExtraMarkError
            result = mark._lilypond_format
            assert isinstance(result, str)
            contribution_list.append(result)
            if section == 'articulations':
                contribution_list.sort()
        # handle context marks
        for parent in component._get_parentage(include_self=False):
            for mark in parent._start_marks:
                if not isinstance(mark, marktools.ContextMark):
                    continue
                if mark in context_marks:
                    continue
                if LilyPondFormatManager.is_formattable_context_mark_for_component(
                    mark, component):
                    context_marks.append(mark)
        #for candidate in context_mark_candidates:
        #    if candidate not in context_marks:
        #            context_marks.append(candidate)
        section = 'context marks'
        for mark in context_marks:
            format_slot = mark._format_slot
            result = LilyPondFormatManager.get_context_mark_format_pieces(mark)
            if format_slot not in contributions:
                contributions[format_slot] = {}
            if section not in contributions[format_slot]:
                contributions[format_slot][section] = []
            contributions[format_slot][section].extend(result)
        # handle markup
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
                result.extend(markup._get_format_pieces())
            else:
                if markup_list[0].direction is None:
                    markup = markuptools.Markup(markup_list[0], direction='-')
                    result.extend(markup._get_format_pieces())
                else:
                    result.extend(markup_list[0]._get_format_pieces())
        if result:
            if 'right' not in contributions:
                contributions['right'] = {}
            contributions['right']['markup'] = result
        for slot in contributions:
            for kind, value in contributions[slot].iteritems():
                contributions[slot][kind] = tuple(value)
        return contributions

    @staticmethod
    def get_context_mark_format_pieces(mark):
        r'''Gets context mark format pieces for `mark`.

        Returns list.
        '''
        from abjad.tools import marktools
        from abjad.tools import scoretools
        addenda = []
        mark_format = mark._lilypond_format
        if isinstance(mark_format, (tuple, list)):
            addenda.extend(mark_format)
        else:
            addenda.append(mark_format)
        # cosmetic mark is a hack to allow marks to format even
        # without effective context;
        # currently used only in metric grid formatting
        if mark._get_effective_context() is not None or \
            getattr(mark, '_is_cosmetic_mark', False) or \
            (isinstance(mark, marktools.TimeSignature) and
            isinstance(mark._start_component, scoretools.Measure)):
            return addenda
        addenda = [r'%%% ' + addendum + r' %%%' for addendum in addenda]
        return addenda

    @staticmethod
    def get_context_setting_format_contributions(component):
        r'''Gets context setting format contributions for `component`.

        Returns sorted list.
        '''
        result = []
        from abjad.tools.scoretools.Leaf import Leaf
        from abjad.tools.scoretools.Measure import Measure
        from abjad.tools.topleveltools import contextualize
        if isinstance(component, (Leaf, Measure)):
            for name, value in vars(contextualize(component)).iteritems():
                # if we've found a leaf LilyPondContextNamespace
                if name.startswith('_'):
                    for x, y in vars(value).iteritems():
                        if not x.startswith('_'):
                            result.append(
                                LilyPondFormatManager.format_lilypond_context_setting_inline(
                                    x, y, name))
                # otherwise we've found a default leaf context contextualize
                else:
                    # parse default context contextualize
                    result.append(
                        LilyPondFormatManager.format_lilypond_context_setting_inline(
                            name, value))
        else:
            for name, value in vars(contextualize(component)).iteritems():
                result.append(LilyPondFormatManager.format_lilypond_context_setting_in_with_block(
                    name, value))
        result.sort()
        return ['context settings', result]

    @staticmethod
    def get_grob_override_format_contributions(component):
        r'''Gets grob override format contributions for `component`.

        Returns alphabetized list of LilyPond grob overrides.
        '''
        from abjad.tools.scoretools import Leaf
        from abjad.tools.topleveltools.override import override
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
        '''Gets grob revert format contributions.

        Returns alphabetized list of LilyPond grob reverts.
        '''
        from abjad.tools.scoretools import Leaf
        from abjad.tools.topleveltools.override import override
        result = []
        if not isinstance(component, Leaf):
            result.extend(override(component)._list_format_contributions(
                'revert'))
        return ['grob reverts', result]

    @staticmethod
    def get_spanner_format_contributions(component):
        r'''Gets spanner format contributions for `component`.

        Dictionary keys equal to format slot;
        dictionary values equal to format contributions.
        '''
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
                for contribution in \
                    override(spanner)._list_format_contributions(
                    'override', is_once=False):
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
                for contribution in \
                    override(spanner)._list_format_contributions('revert'):
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
        return result

    @staticmethod
    def is_formattable_context_mark_for_component(mark, component):
        r'''Returns true if ContextMark `mark` can format for `component`.
        '''
        from abjad.tools import scoretools
        from abjad.tools import marktools
        if mark._start_component is None:
            return False
        if isinstance(mark._start_component, scoretools.Measure):
            if mark._start_component is component:
                if not isinstance(mark, marktools.TimeSignature):
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
