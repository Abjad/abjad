from abjad.tools.abctools import AbjadObject


class LilyPondFormatManager(AbjadObject):
    r'''Manages LilyPond formatting logic.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'LilyPond formatting'

    __slots__ = ()

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
        context_wrappers = []
        noncontext_wrappers = []
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
            elif (wrapper.context is None and
                hasattr(wrapper.indicator, '_format_leaf_children') and
                not getattr(wrapper.indicator, '_format_leaf_children') and
                wrapper.component is not component):
                continue
            # store markup
            elif isinstance(wrapper.indicator, abjad.Markup):
                if wrapper.indicator.direction == abjad.Up:
                    up_markup.append(wrapper.indicator)
                elif wrapper.indicator.direction == abjad.Down:
                    down_markup.append(wrapper.indicator)
                elif wrapper.indicator.direction in (abjad.Center, None):
                    neutral_markup.append(wrapper.indicator)
            # store context wrappers
            elif wrapper.context is not None:
                if wrapper._is_formattable_for_component(component):
                    context_wrappers.append(wrapper)
            # store noncontext wrappers
            else:
                noncontext_wrappers.append(wrapper)
        indicators = (
            up_markup,
            down_markup,
            neutral_markup,
            context_wrappers,
            noncontext_wrappers,
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
        import abjad
        result = []
        once = isinstance(component, abjad.Leaf)
        grob = abjad.override(component)
        contributions = grob._list_format_contributions(
            'override',
            once=once,
            )
        for string in result[:]:
            if 'NoteHead' in string and 'pitch' in string:
                contributions.remove(string)
        try:
            written_pitch = component.written_pitch
            arrow = written_pitch.arrow
        except AttributeError:
            arrow = None
        if arrow in (abjad.Up, abjad.Down):
            contributions_ = written_pitch._list_format_contributions()
            contributions.extend(contributions_)
        bundle.grob_overrides.extend(contributions)

    @staticmethod
    def _populate_grob_revert_format_contributions(component, bundle):
        import abjad
        if not isinstance(component, abjad.Leaf):
            manager = abjad.override(component)
            contributions = manager._list_format_contributions('revert')
            bundle.grob_reverts.extend(contributions)

    @staticmethod
    def _populate_indicator_format_contributions(component, bundle):
        manager = LilyPondFormatManager
        (
            up_markup,
            down_markup,
            neutral_markup,
            context_wrappers,
            noncontext_wrappers,
            ) = LilyPondFormatManager._collect_indicators(component)
        manager._populate_markup_format_contributions(
            component,
            bundle,
            up_markup,
            down_markup,
            neutral_markup,
            )
        manager._populate_context_wrapper_format_contributions(
            component,
            bundle,
            context_wrappers,
            )
        manager._populate_noncontext_wrapper_format_contributions(
            component,
            bundle,
            noncontext_wrappers,
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
    def _populate_noncontext_wrapper_format_contributions(
        component,
        bundle,
        noncontext_wrappers,
        ):
        for noncontext_wrapper in noncontext_wrappers:
            indicator = noncontext_wrapper.indicator
            if hasattr(indicator, '_get_lilypond_format_bundle'):
                indicator_bundle = indicator._get_lilypond_format_bundle()
                if indicator_bundle is not None:
                    bundle.update(indicator_bundle)

    @staticmethod
    def _populate_context_wrapper_format_contributions(
        component,
        bundle,
        context_wrappers,
        ):
        for context_wrapper in context_wrappers:
            format_pieces = context_wrapper._get_format_pieces()
            if isinstance(format_pieces, type(bundle)):
                bundle.update(format_pieces)
            else:
                format_slot = context_wrapper.indicator._format_slot
                bundle.get(format_slot).indicators.extend(format_pieces)

    @staticmethod
    def _populate_spanner_format_contributions(
        component,
        bundle,
        ):
        import abjad
        pairs = []
        parentage = abjad.inspect(component).get_parentage()
        for spanner in abjad.select(parentage)._get_spanners():
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
        import abjad
        if '_get_lilypond_format' in dir(argument) and not isinstance(argument, str):
            pass
        elif argument in (True, False):
            argument = abjad.Scheme(argument)
        elif argument in (
            abjad.Up, abjad.Down, abjad.Left, abjad.Right, abjad.Center):
            argument = abjad.Scheme(repr(argument).lower())
        elif isinstance(argument, int) or isinstance(argument, float):
            argument = abjad.Scheme(argument)
        elif argument in LilyPondFormatManager.lilypond_color_constants:
            argument = abjad.Scheme(argument)
        elif isinstance(argument, str) and '::' in argument:
            argument = abjad.Scheme(argument)
        elif isinstance(argument, tuple) and len(argument) == 2:
            argument = abjad.SchemePair(argument)
        elif isinstance(argument, str) and ' ' not in argument:
            argument = abjad.Scheme(argument, quoting="'")
        elif isinstance(argument, str) and ' ' in argument:
            argument = abjad.Scheme(argument)
        else:
            argument = abjad.Scheme(argument, quoting="'")
        return format(argument, 'lilypond')

    @staticmethod
    def make_lilypond_override_string(
        grob,
        attribute,
        value,
        context=None,
        once=False,
        ):
        r'''Makes Lilypond override string.

        Returns string.
        '''
        import abjad
        grob = abjad.String(grob).to_upper_camel_case()
        attribute = LilyPondFormatManager.format_lilypond_attribute(attribute)
        value = LilyPondFormatManager.format_lilypond_value(value)
        if context is not None:
            context = abjad.String(context).to_upper_camel_case()
            context += '.'
        else:
            context = ''
        if once is True:
            once = r'\once '
        else:
            once = ''
        result = r'{}\override {}{}.{} = {}'
        result = result.format(once, context, grob, attribute, value)
        return result

    @staticmethod
    def make_lilypond_revert_string(grob, attribute, context=None):
        r'''Makes LilyPond revert string.

        Returns string.
        '''
        import abjad
        grob = abjad.String(grob).to_upper_camel_case()
        attribute = LilyPondFormatManager.format_lilypond_attribute(attribute)
        attribute = attribute.split('.')[0]
        if context is not None:
            context = abjad.String(context).to_upper_camel_case()
            context += '.'
        else:
            context = ''
        result = r'\revert {}{}.{}'
        result = result.format(context, grob, attribute)
        return result

    @staticmethod
    def make_lilypond_tweak_string(attribute, value, grob=None):
        r'''Makes Lilypond \tweak string.

        Returns string.
        '''
        import abjad
        if grob is not None:
            grob = abjad.String(grob).to_upper_camel_case()
            grob += '.'
        else:
            grob = ''
        attribute = LilyPondFormatManager.format_lilypond_attribute(attribute)
        value = LilyPondFormatManager.format_lilypond_value(value)
        result = r'- \tweak {}{} {}'
        result = result.format(grob, attribute, value)
        return result

    @staticmethod
    def report_component_format_contributions(component, verbose=False):
        r'''Reports `component` format contributions.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 [ ( d'4 e'4 f'4 ] )")
            >>> abjad.override(staff[0]).note_head.color = 'red'

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

            >>> staff = abjad.Staff("c8 d e f")
            >>> spanner = abjad.Beam()
            >>> abjad.attach(spanner, staff[:])

            >>> manager = abjad.LilyPondFormatManager
            >>> print(manager.report_spanner_format_contributions(spanner))
            c8	abjad.LilyPondFormatBundle(
                    right=abjad.SlotContributions(
                        spanner_starts=['['],
                        ),
                    )
            d8	abjad.LilyPondFormatBundle()
            e8	abjad.LilyPondFormatBundle()
            f8	abjad.LilyPondFormatBundle(
                    right=abjad.SlotContributions(
                        spanner_stops=[']'],
                        ),
                    )

        Returns string or none.
        '''
        result = []
        for leaf in spanner.leaves:
            bundle = spanner._get_lilypond_format_bundle(leaf)
            bundle_pieces = format(bundle).split('\n')
            result.append('{!s}\t{}'.format(leaf, bundle_pieces[0]))
            for piece in bundle_pieces[1:]:
                result.append('\t{}'.format(piece))
        result = '\n'.join(result)
        return result
