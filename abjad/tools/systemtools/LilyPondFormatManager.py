from abjad.enumerations import Up, Down, Left, Right, Center
from abjad.tools.abctools.AbjadObject import AbjadObject


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

    indent = 4 * ' '

    ### PRIVATE METHODS ###

    @staticmethod
    def _collect_indicators(component):
        import abjad
        wrappers = []
        parentage = abjad.inspect(component).get_parentage(include_self=True)
        for parent in parentage:
            wrappers_ = abjad.inspect(parent).wrappers()
            wrappers.extend(wrappers_)
            if hasattr(parent, '_spanners'):
                wrappers_ = parent._get_spanner_indicators(unwrap=False)
                wrappers.extend(wrappers_)
        up_markup_wrappers = []
        down_markup_wrappers = []
        neutral_markup_wrappers = []
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
            elif wrapper.annotation is not None or wrapper.spanner is not None:
                continue
            # skip comments and commands unless attached directly to us
            elif (wrapper.context is None and
                hasattr(wrapper.indicator, '_format_leaf_children') and
                not getattr(wrapper.indicator, '_format_leaf_children') and
                wrapper.component is not component):
                continue
            # store markup wrappers
            elif isinstance(wrapper.indicator, abjad.Markup):
                if wrapper.indicator.direction is Up:
                    up_markup_wrappers.append(wrapper)
                elif wrapper.indicator.direction is Down:
                    down_markup_wrappers.append(wrapper)
                elif wrapper.indicator.direction in (abjad.Center, None):
                    neutral_markup_wrappers.append(wrapper)
            # store context wrappers
            elif wrapper.context is not None:
                if wrapper._is_formattable_for_component(component):
                    context_wrappers.append(wrapper)
            # store noncontext wrappers
            else:
                noncontext_wrappers.append(wrapper)
        indicators = (
            up_markup_wrappers,
            down_markup_wrappers,
            neutral_markup_wrappers,
            context_wrappers,
            noncontext_wrappers,
            )
        return indicators

    @staticmethod
    def _populate_context_setting_format_contributions(component, bundle):
        import abjad
        result = []
        manager = LilyPondFormatManager
        if isinstance(component, abjad.Context):
            for name, value in vars(abjad.setting(component)).items():
                string = manager.format_lilypond_context_setting_in_with_block(
                    name, value)
                result.append(string)
        else:
            contextualizer = abjad.setting(component)
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
    def _populate_context_wrapper_format_contributions(
        component,
        bundle,
        context_wrappers,
        ):
        for wrapper in context_wrappers:
            format_pieces = wrapper._get_format_pieces()
            if isinstance(format_pieces, type(bundle)):
                bundle.update(format_pieces)
            else:
                format_slot = wrapper.indicator._format_slot
                bundle.get(format_slot).indicators.extend(format_pieces)

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
            up_markup_wrappers,
            down_markup_wrappers,
            neutral_markup_wrappers,
            context_wrappers,
            noncontext_wrappers,
            ) = LilyPondFormatManager._collect_indicators(component)
        manager._populate_markup_format_contributions(
            component,
            bundle,
            up_markup_wrappers,
            down_markup_wrappers,
            neutral_markup_wrappers,
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
        up_markup_wrappers,
        down_markup_wrappers,
        neutral_markup_wrappers,
        ):
        import abjad
        for wrappers in (
            up_markup_wrappers,
            down_markup_wrappers,
            neutral_markup_wrappers,
            ):
            if not wrappers:
                continue
            elif 1 < len(wrappers):
                direction = wrappers[0].indicator.direction
                if direction is None:
                    direction = '-'
                wrappers = wrappers[:]
                wrappers.sort(key=lambda _: -_.indicator.stack_priority)
                lines = [
                    abjad.Markup.line(
                        [_.indicator],
                        deactivate=_.deactivate,
                        tag=_.tag,
                        )
                    for _ in wrappers
                    ]
                markup = abjad.Markup.column(lines, direction=direction)
                format_pieces = markup._get_format_pieces()
                bundle.right.markup.extend(format_pieces)
            else:
                wrapper = wrappers[0]
                if wrapper.indicator.direction is None:
                    markup = abjad.Markup(wrappers[0].indicator, direction='-')
                else:
                    markup = wrapper.indicator
                format_pieces = markup._get_format_pieces()
                format_pieces = LilyPondFormatManager.tag(
                    format_pieces,
                    wrapper.tag,
                    deactivate=wrapper.deactivate,
                    )
                bundle.right.markup.extend(format_pieces)

    @staticmethod
    def _populate_noncontext_wrapper_format_contributions(
        component,
        bundle,
        noncontext_wrappers,
        ):
        for wrapper in noncontext_wrappers:
            indicator = wrapper.indicator
            if hasattr(indicator, '_get_lilypond_format_bundle'):
                bundle_ = indicator._get_lilypond_format_bundle()
                if wrapper.tag:
                    bundle_.tag_format_contributions(
                        wrapper.tag,
                        deactivate=wrapper.deactivate,
                        )
                if bundle_ is not None:
                    bundle.update(bundle_)

    @staticmethod
    def _populate_spanner_format_contributions(component, bundle):
        import abjad
        if not hasattr(component, '_spanners'):
            return
        pairs = []
        for spanner in abjad.inspect(component).get_spanners():
            spanner_bundle = spanner._get_lilypond_format_bundle(component)
            spanner_bundle.tag_format_contributions(
                spanner._tag,
                deactivate=spanner._deactivate,
                )
            pair = (spanner, spanner_bundle)
            pairs.append(pair)
        pairs.sort(key=lambda _: type(_[0]).__name__)
        for spanner, spanner_bundle in pairs:
            bundle.update(spanner_bundle)

    ### PUBLIC METHODS ###

    @staticmethod
    def align_tags(string, n):
        r'''Line-breaks `string` and aligns tags starting a column `n`.

        Returns new string.
        '''
        assert isinstance(n, int), repr(n)
        lines = []
        for line in string.split('\n'):
            if '%!' not in line:
                lines.append(line)
                continue
            location = line.find('%!')
            left = line[:location].rstrip()
            right = line[location:]
            pad = n - len(left)
            if pad < 1:
                pad = 1
            line = left + pad * ' ' + right
            lines.append(line)
        string = '\n'.join(lines)
        return string

    @staticmethod
    def bundle_format_contributions(component):
        r'''Gets all format contributions for `component`.

        Returns LilyPond format bundle.
        '''
        import abjad
        manager = LilyPondFormatManager
        bundle = abjad.LilyPondFormatBundle()
        manager._populate_indicator_format_contributions(component, bundle)
        manager._populate_spanner_format_contributions(component, bundle)
        manager._populate_context_setting_format_contributions(
            component, bundle)
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
        elif argument in (Up, Down, Left, Right, Center):
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
    def left_shift_tags(text, realign=None):
        r'''Left shifts tags in `strings` and realigns to column `realign`.

        Returns new text.
        '''
        import abjad
        strings = text.split('\n')
        strings_ = [] 
        for string in strings:
            if '%@% ' not in string or '%!' not in string:
                strings_.append(string)
                continue
            if not string.startswith(4 * ' '):
                strings_.append(string)
                continue
            string_ = string[4:]
            tag_start = string_.find('%!')
            string_ = list(string_)
            string_[tag_start:tag_start] = 4 * ' '
            string_ = ''.join(string_)
            strings_.append(string_)
        text = '\n'.join(strings_)
        if realign is not None:
            text = LilyPondFormatManager.align_tags(text, n=realign)
        return text

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
        from abjad.tools.datastructuretools.String import String
        grob = String(grob).to_upper_camel_case()
        attribute = LilyPondFormatManager.format_lilypond_attribute(attribute)
        value = LilyPondFormatManager.format_lilypond_value(value)
        if context is not None:
            context = String(context).capitalize_start() + '.'
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
    def make_lilypond_revert_string(grob, attribute, context=None) -> str:
        r'''Makes LilyPond revert string.

        ..  container:: example

            >>> abjad.LilyPondFormatManager.make_lilypond_revert_string(
            ...     'glissando',
            ...     'bound_details__right__arrow',
            ...     )
            '\\revert Glissando.bound-details.right.arrow'

        '''
        from abjad.tools.datastructuretools.String import String
        grob = String(grob).to_upper_camel_case()
        dotted = LilyPondFormatManager.format_lilypond_attribute(attribute)
        if context is not None:
            context = String(context).to_upper_camel_case()
            context += '.'
        else:
            context = ''
        result = r'\revert {}{}.{}'
        result = result.format(context, grob, dotted)
        return result

    @staticmethod
    def make_lilypond_tweak_string(
        attribute,
        value,
        grob=None,
        hyphen=True,
        ):
        r'''Makes Lilypond \tweak string.

        Returns string.
        '''
        from abjad.tools.datastructuretools.String import String
        if grob is not None:
            grob = String(grob).to_upper_camel_case()
            grob += '.'
        else:
            grob = ''
        attribute = LilyPondFormatManager.format_lilypond_attribute(attribute)
        value = LilyPondFormatManager.format_lilypond_value(value)
        string = rf'\tweak {grob}{attribute} {value}'
        if hyphen:
            string = '- ' + string
        return string

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

    @staticmethod
    def tag(strings, tag, deactivate=None):
        r'''Tags `strings` with `tag`.

        Returns list of tagged strings.
        '''
        if not tag:
            return strings
        if not strings:
            return strings
        if deactivate is not None:
            assert isinstance(deactivate, type(True)), repr(deactivate)
        length = max([len(_) for _ in strings])
        strings_ = []
        for string in strings:
            if '%!' not in string:
                pad = length - len(string)
            else:
                pad = 0
            tag_ = pad * ' ' + ' ' + '%!' + ' ' + str(tag)
            string = string + tag_
            strings_.append(string)
        if deactivate is True:
            strings_ = ['%@% ' + _ for _ in strings_]
        return strings_
