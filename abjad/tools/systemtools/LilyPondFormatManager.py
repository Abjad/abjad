# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LilyPondFormatManager(AbjadObject):
    r'''Manages LilyPond formatting logic.

    ::

        >>> import abjad

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'LilyPond formatting'

    __slots__ = (
        )

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
        import abjad
        wrappers = []
        parentage = abjad.inspect(component).get_parentage(include_self=True)
        for parent in parentage:
            wrappers_ = abjad.inspect(parent).get_indicators(unwrap=False)
            wrappers.extend(wrappers_)
            wrappers_ = parent._get_spanner_indicators(unwrap=False)
            wrappers.extend(wrappers_)
        up_markup = []
        down_markup = []
        neutral_markup = []
        scoped_wrappers = []
        nonscoped_wrappers = []
        # classify wrappers attached to component
        for wrapper in wrappers:
            # skip nonprinting indicators like annotation
            indicator = wrapper.indicator
            if (not hasattr(indicator, '_get_lilypond_format') and
                not hasattr(indicator, '_get_lilypond_format_bundle')
                ):
                continue
            elif wrapper.is_annotation or wrapper.is_piecewise:
                continue
            # skip comments and commands unless attached directly to us
            elif (wrapper.scope is None and
                hasattr(wrapper.indicator, '_format_leaf_children') and
                not getattr(wrapper.indicator, '_format_leaf_children') and
                wrapper.component is not component
                ):
                continue
            # store markup
            elif isinstance(wrapper.indicator, abjad.Markup):
                if wrapper.indicator.direction == Up:
                    up_markup.append(wrapper.indicator)
                elif wrapper.indicator.direction == Down:
                    down_markup.append(wrapper.indicator)
                elif wrapper.indicator.direction in (Center, None):
                    neutral_markup.append(wrapper.indicator)
            # store scoped wrappers
            elif wrapper.scope is not None:
                if wrapper._is_formattable_for_component(component):
                    scoped_wrappers.append(wrapper)
            # store nonscoped wrappers
            else:
                nonscoped_wrappers.append(wrapper)
        indicators = (
            up_markup,
            down_markup,
            neutral_markup,
            scoped_wrappers,
            nonscoped_wrappers,
            )
        return indicators

    @staticmethod
    def _populate_context_setting_format_contributions(component, bundle):
        result = []
        from abjad.tools.topleveltools import setting
        from abjad.tools import scoretools
        manager = LilyPondFormatManager
        if isinstance(component, scoretools.Context):
            for name, value in vars(setting(component)).items():
                string = manager.format_lilypond_context_setting_in_with_block(
                    name, value)
                result.append(string)
        else:
            contextualizer = setting(component)
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
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        from abjad.tools import topleveltools
        result = []
        is_once = isinstance(component, scoretools.Leaf)
        grob = topleveltools.override(component)
        contributions = grob._list_format_contributions(
            'override',
            is_once=is_once,
            )
        for string in result[:]:
            if 'NoteHead' in string and 'pitch' in string:
                contributions.remove(string)
        try:
            written_pitch = component.written_pitch
            arrow = written_pitch.arrow
        except AttributeError:
            arrow = None
        if arrow in (Up, Down):
            contributions_ = written_pitch._list_format_contributions()
            contributions.extend(contributions_)
        bundle.grob_overrides.extend(contributions)

    @staticmethod
    def _populate_grob_revert_format_contributions(component, bundle):
        from abjad.tools import scoretools
        from abjad.tools import topleveltools
        if not isinstance(component, scoretools.Leaf):
            manager = topleveltools.override(component)
            contributions = manager._list_format_contributions('revert')
            bundle.grob_reverts.extend(contributions)

    @staticmethod
    def _populate_indicator_format_contributions(component, bundle):
        import abjad
        manager = LilyPondFormatManager
        (
            up_markup,
            down_markup,
            neutral_markup,
            scoped_wrappers,
            nonscoped_wrappers,
            ) = LilyPondFormatManager._collect_indicators(component)
        manager._populate_markup_format_contributions(
            component,
            bundle,
            up_markup,
            down_markup,
            neutral_markup,
            )
        manager._populate_scoped_wrapper_format_contributions(
            component,
            bundle,
            scoped_wrappers,
            )
        manager._populate_nonscoped_wrapper_format_contributions(
            component,
            bundle,
            nonscoped_wrappers,
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
                markup_list = [
                    markuptools.Markup.line([_]) for _ in markup_list]
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
    def _populate_nonscoped_wrapper_format_contributions(
        component,
        bundle,
        nonscoped_wrappers,
        ):
        for nonscoped_wrapper in nonscoped_wrappers:
            indicator = nonscoped_wrapper.indicator
            if hasattr(indicator, '_get_lilypond_format_bundle'):
                indicator_bundle = indicator._get_lilypond_format_bundle()
                if indicator_bundle is not None:
                    bundle.update(indicator_bundle)

    @staticmethod
    def _populate_scoped_wrapper_format_contributions(
        component,
        bundle,
        scoped_wrappers,
        ):
        for scoped_wrapper in scoped_wrappers:
            format_pieces = scoped_wrapper._get_format_pieces()
            if isinstance(format_pieces, type(bundle)):
                bundle.update(format_pieces)
            else:
                format_slot = scoped_wrapper.indicator._format_slot
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
        pairs.sort(key=lambda _: type(_[0]).__name__)
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
    def format_lilypond_value(argument):
        r'''Formats LilyPond `argument` according to Scheme formatting
        conventions.

        Returns string.
        '''
        from abjad.tools import schemetools
        if '_get_lilypond_format' in dir(argument) and not isinstance(argument, str):
            pass
        elif argument in (True, False):
            argument = schemetools.Scheme(argument)
        elif argument in (Up, Down, Left, Right, Center):
            argument = schemetools.Scheme(repr(argument).lower())
        elif isinstance(argument, int) or isinstance(argument, float):
            argument = schemetools.Scheme(argument)
        elif argument in LilyPondFormatManager.lilypond_color_constants:
            argument = schemetools.Scheme(argument)
        elif isinstance(argument, str) and '::' in argument:
            argument = schemetools.Scheme(argument)
        elif isinstance(argument, tuple) and len(argument) == 2:
            argument = schemetools.SchemePair(argument)
        elif isinstance(argument, str) and ' ' not in argument:
            argument = schemetools.Scheme(argument, quoting="'")
        elif isinstance(argument, str) and ' ' in argument:
            argument = schemetools.Scheme(argument)
        else:
            argument = schemetools.Scheme(argument, quoting="'")
        return format(argument, 'lilypond')

    @staticmethod
    def make_lilypond_override_string(
        grob_name,
        grob_attribute,
        grob_value,
        context_name=None,
        is_once=False,
        ):
        r'''Makes Lilypond override string.

        Does not include 'once'.

        Returns string.
        '''
        import abjad
        grob_name = abjad.String(grob_name).to_upper_camel_case()
        grob_attribute = LilyPondFormatManager.format_lilypond_attribute(
            grob_attribute)
        grob_value = LilyPondFormatManager.format_lilypond_value(grob_value)
        if context_name is not None:
            context_prefix = abjad.String(context_name).to_upper_camel_case()
            context_prefix += '.'
        else:
            context_prefix = ''
        if is_once:
            once_prefix = r'\once '
        else:
            once_prefix = ''
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
        r'''Makes LilyPond revert string.

        Returns string.
        '''
        import abjad
        grob_name = abjad.String(grob_name).to_upper_camel_case()
        grob_attribute = LilyPondFormatManager.format_lilypond_attribute(
            grob_attribute)
        # change #'bound-details #'left #'text to #'bound-details
        grob_attribute = grob_attribute.split('.')[0]
        context_prefix = ''
        if context_name is not None:
            context_prefix = abjad.String(context_name).to_upper_camel_case()
            context_prefix += '.'
        result = r'\revert {}{}.{}'
        result = result.format(context_prefix, grob_name, grob_attribute)
        return result

    @staticmethod
    def make_lilypond_tweak_string(
        grob_attribute,
        grob_value,
        grob_name=None,
        ):
        r'''Makes Lilypond \tweak string.

        Returns string.
        '''
        import abjad
        if grob_name is not None:
            grob_name = abjad.String(grob_name).to_upper_camel_case()
            grob_string = grob_name + '.'
        else:
            grob_string = ''
        grob_attribute = LilyPondFormatManager.format_lilypond_attribute(
            grob_attribute)
        grob_value = LilyPondFormatManager.format_lilypond_value(grob_value)
        result = r'- \tweak {}{} {}'
        result = result.format(
            grob_string,
            grob_attribute,
            grob_value,
            )
        return result

    @staticmethod
    def report_component_format_contributions(component, verbose=False):
        r'''Reports `component` format contributions.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 [ ( d'4 e'4 f'4 ] )")
                >>> abjad.override(staff[0]).note_head.color = 'red'

            ::

                >>> manager = abjad.LilyPondFormatManager
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
        r'''Reports spanner format contributions for every leaf in `spanner`.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c8 d e f")
                >>> spanner = abjad.Beam()
                >>> abjad.attach(spanner, staff[:])

            ::

                >>> manager = abjad.LilyPondFormatManager
                >>> print(manager.report_spanner_format_contributions(spanner))
                c8	systemtools.LilyPondFormatBundle(
                        right=systemtools.SlotContributions(
                            spanner_starts=['['],
                            ),
                        )
                d8	systemtools.LilyPondFormatBundle()
                e8	systemtools.LilyPondFormatBundle()
                f8	systemtools.LilyPondFormatBundle(
                        right=systemtools.SlotContributions(
                            spanner_stops=[']'],
                            ),
                        )

        Returns string or none.
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
