# -*- encoding: utf-8 -*-
import functools
import numbers
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from scoremanager.idetools import predicates


class PromptMakerMixin(AbjadObject):
    r'''Prompt maker mixin.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _abjad_import_statement(self):
        return 'from abjad import *'

    ### PRIVATE METHODS ###

    def _make_prompt(
        self,
        spaced_attribute_name,
        default_value=None,
        disallow_range=False,
        help_template=None,
        help_template_arguments=None,
        include_chevron=True,
        setup_statements=None,
        target_menu_section=None,
        validation_function=None,
        ):
        from scoremanager import idetools
        prompt = idetools.Prompt(
            default_value=default_value,
            disallow_range=disallow_range,
            help_template=help_template,
            help_template_arguments=help_template_arguments,
            include_chevron=include_chevron,
            message=spaced_attribute_name,
            setup_statements=setup_statements,
            target_menu_section=target_menu_section,
            validation_function=validation_function,
            )
        self._prompts.append(prompt)

    ### PUBLIC METHODS ###

    def append_articulation(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends articulation.

        Returns prompt.
        '''
        help_template = 'value'
        help_template += ' must successfully initialize articulation.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_ariculation_token,
            help_template=help_template,
            default_value=default_value,
            )

    def append_articulations(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends articulations.

        Returns prompt.
        '''
        help_template = 'value '
        help_template += ' must successfully initialize articulations.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.are_articulation_tokens,
            help_template=help_template,
            default_value=default_value,
            )

    def append_available_snake_case_package_name(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends available snake case package name.

        Returns prompt.
        '''
        help_template = 'value must be available '
        help_template += 'underscore-delimited lowercase package name.'
        validation_function = predicates.is_available_snake_case_package_name
        self._make_prompt(
            spaced_attribute_name,
            validation_function=validation_function,
            help_template=help_template,
            default_value=default_value,
            )

    def append_boolean(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends boolean.

        Returns prompt.
        '''
        help_template = 'value must be boolean.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_boolean,
            help_template=help_template,
            default_value=default_value,
            )

    def append_clef(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends clef.

        Returns prompt.
        '''
        help_template = 'value'
        help_template += ' must successfully initialize clef.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_clef_token,
            help_template=help_template,
            default_value=default_value,
            )

    def append_constellation_circuit_id_pair(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends constellation circuit ID pair.

        Returns prompt.
        '''
        help_template = 'value must be valid constellation circuit id pair.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=lambda x: True,
            help_template=help_template,
            default_value=default_value,
            )

    def append_dash_case_file_name(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends dash case file name.

        Returns prompt.
        '''
        help_template = 'value must be dash case file name.'
        self._make_prompt(
            spaced_attribute_name,
            help_template=help_template,
            validation_function=stringtools.is_dash_case_file_name,
            default_value=default_value,
            )

    def append_direction_string(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends direction string.

        Returns prompt.
        '''
        help_template = "value must be 'up or 'down'."
        self._make_prompt(
            spaced_attribute_name,
            help_template=help_template,
            validation_function=predicates.is_direction_string,
            default_value=default_value,
            )

    def append_duration(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends duration.

        Returns prompt.
        '''
        help_template = 'value must be duration.'
        setup_statements = []
        setup_statements.append(self._abjad_import_statement)
        setup_statements.append('evaluated_input = Duration({})')
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_duration_token,
            help_template=help_template,
            setup_statements=setup_statements,
            default_value=default_value,
            )

    def append_durations(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends durations.

        Returns prompt.
        '''
        help_template = 'value must be list of durations.'
        setup_statements = []
        setup_statements.append(self._abjad_import_statement)
        setup_statements.append('evaluated_input = [Duration(x) for x in {}]')
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.are_duration_tokens,
            help_template=help_template,
            setup_statements=setup_statements,
            default_value=default_value,
            )

    def append_dynamic(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends dynamic.

        Returns prompt.
        '''
        help_template = 'value'
        help_template += ' must successfully initialize dynamic.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_dynamic_token,
            help_template=help_template,
            default_value=default_value,
            )

    def append_dynamics(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends dynamics.

        Returns prompt.
        '''
        help_template = 'value must be list of dynamic initializers.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.are_dynamic_tokens,
            help_template=help_template,
            default_value=default_value,
            )

    def append_existing_package_name(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends existing package name.

        Returns prompt.
        '''
        help_template = 'value must be existing package name.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_existing_package_name,
            help_template=help_template,
            default_value=default_value,
            )

    def append_expr(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends expression.

        Returns prompt.
        '''
        help_template = 'value may be anything.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=lambda expr: True,
            help_template=help_template,
            default_value=default_value,
            )

    def append_hairpin_token(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends hairpin token.

        Returns prompt.
        '''
        help_template = 'value must be hairpin token.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_hairpin_token,
            help_template=help_template,
            default_value=default_value,
            )

    def append_hairpin_tokens(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends hairpin tokens.

        Returns prompt.
        '''
        help_template = 'value must be tuple of hairpin tokens.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.are_hairpin_tokens,
            help_template=help_template,
            default_value=default_value,
            )

    def append_identifier(
        self,
        spaced_attribute_name,
        allow_spaces=False,
        default_value=None,
        ):
        r'''Appends Python identifier.

        String beginning with a letter or underscore and containing only 
        letters, digits and underscores.

        Returns prompt.
        '''
        help_template = 'value must be valid Python identifier.'
        helper = lambda x: predicates.is_identifier(
            x, allow_spaces=allow_spaces)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=helper,
            help_template=help_template,
            default_value=default_value,
            )

    def append_integer(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends integer.

        Returns prompt.
        '''
        help_template = 'value must be integer.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_integer,
            help_template=help_template,
            default_value=default_value,
            )

    def append_integer_in_range(
        self,
        spaced_attribute_name,
        start=None,
        stop=None,
        allow_none=False,
        default_value=None,
        ):
        r'''Appends integer in range.

        Returns prompt.
        '''
        validation_function = functools.partial(
            predicates.is_integer_in_range,
            start=start,
            stop=stop,
            allow_none=allow_none,
            )
        help_template = 'value must be integer between {} and {}, inclusive.'
        self._make_prompt(
            spaced_attribute_name,
            help_template=help_template,
            validation_function=validation_function,
            help_template_arguments=(start, stop),
            default_value=default_value,
            )

    def append_integers(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends integers.

        Returns prompt.
        '''
        help_template = 'value must be tuple of integers.'
        function = lambda x: all(predicates.is_integer(y) for y in x)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=function,
            help_template=help_template,
            default_value=default_value,
            )

    def append_list(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends lists.

        Returns prompt.
        '''
        help_template = 'value must be list.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_list,
            help_template=help_template,
            default_value=default_value,
            )

    def append_lists(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends lists.

        Returns prompt.
        '''
        help_template = 'value must be tuple of lists.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.are_lists,
            help_template=help_template,
            default_value=default_value,
            )

    def append_markup(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends markup.

        Returns prompt.
        '''
        help_template = 'value must be markup.'
        setup_statements = []
        setup_statements.append(self._abjad_import_statement)
        statement = 'evaluated_input = markuptools.Markup({})'
        setup_statements.append(statement)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_markup,
            help_template=help_template,
            setup_statements=setup_statements,
            default_value=default_value,
            )

    def append_menu_section_item(
        self,
        spaced_attribute_name,
        target_menu_section,
        default_value=None,
        ):
        r'''Appends menu section item.

        Returns prompt.
        '''
        help_template = 'value must be menu section item.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_list,
            help_template=help_template,
            target_menu_section=target_menu_section,
            default_value=default_value,
            disallow_range=True,
            )

    def append_menu_section_range(
        self,
        spaced_attribute_name,
        target_menu_section,
        default_value=None,
        ):
        r'''Appends menu section range.

        Returns prompt.
        '''
        help_template = 'value must be argument range.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_list,
            help_template=help_template,
            target_menu_section=target_menu_section,
            default_value=default_value,
            )

    def append_named_pitch(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends named pitch.

        Returns prompt.
        '''
        help_template = 'value must be named pitch.'
        setup_statements = []
        setup_statements.append(self._abjad_import_statement)
        string = 'evaluated_input = pitchtools.NamedPitch({!r})'
        setup_statements.append(string)
        self._make_prompt(
            spaced_attribute_name,
            help_template=help_template,
            validation_function=predicates.is_named_pitch,
            setup_statements=setup_statements,
            default_value=default_value,
            )

    def append_nonnegative_integer(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends nonnegative integer.

        Returns prompt.
        '''
        help_template = 'value must be nonnegative integer.'
        function = lambda x: 0 < x
        self._make_prompt(
            spaced_attribute_name,
            validation_function=function,
            help_template=help_template,
            default_value=default_value,
            )

    def append_nonnegative_integers(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends nonnegative integers.

        Returns prompt.
        '''
        help_template = 'value must be tuple of nonnegative integers.'
        function = lambda x: all(isinstance(y, int) and 0 <= y for y in x)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=function,
            help_template=help_template,
            default_value=default_value,
            )

    def append_nonzero_integers(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends nonzero integers.

        Returns prompt.
        '''
        help_template = 'value must be tuple of nonzero integers.'
        function = lambda x: all(isinstance(y, int) and not y == 0 for y in x)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=function,
            help_template=help_template,
            default_value=default_value,
            )

    def append_number(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends number.

        Returns prompt.
        '''
        help_template = 'value must be number.'
        function = lambda x: isinstance(x, numbers.Number)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=function,
            help_template=help_template,
            default_value=default_value,
            )

    def append_paper_dimensions(
        self,
        spaced_attribute_name,
        default_value='8.5 x 11 in',
        ):
        r'''Appends paper dimensions.

        Returns prompt.
        '''
        help_template = "value must be of the form '8.5 x 11 in'."
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_paper_dimension_string,
            help_template=help_template,
            default_value=default_value,
            )

    def append_pitch_range(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends pitch range.

        Returns prompt.
        '''
        help_template = 'value must be pitch range.'
        setup_statements = []
        setup_statements.append(self._abjad_import_statement)
        setup_statements.append('evaluated_input = pitchtools.PitchRange({})')
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_pitch_range_or_none,
            help_template=help_template,
            setup_statements=setup_statements,
            default_value=default_value,
            )
        self._setup_statements[-1] = setup_statements

    def append_pitch_range_string(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends symbolic pitch range string.

        Returns prompt.
        '''
        help_template = 'value must be pitch range string. Ex: [A0, C8].'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=pitchtools.PitchRange.is_range_string,
            help_template=help_template,
            default_value=default_value,
            )

    def append_positive_integer(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends positive integer.

        Returns prompt.
        '''
        help_template = 'value must be positive integer.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=mathtools.is_positive_integer,
            help_template=help_template,
            default_value=default_value,
            )

    def append_positive_integer_power_of_two(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends positive integer power of two.

        Returns prompt.
        '''
        help_template = 'value must be positive integer power of two.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=mathtools.is_positive_integer_power_of_two,
            help_template=help_template,
            default_value=default_value,
            )

    def append_positive_integer_powers_of_two(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends positive integer powers of two.

        Returns prompt.
        '''
        help_template = 'value must be list or tuple of'
        help_template += ' positive integer powers of two.'
        validation_function = mathtools.all_are_positive_integer_powers_of_two
        self._make_prompt(
            spaced_attribute_name,
            validation_function=validation_function,
            help_template=help_template,
            default_value=default_value,
            )

    def append_positive_integers(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends positive integers.

        Returns prompt.
        '''
        help_template = 'value must be tuple of positive integers.'
        function = lambda expr: all(
            mathtools.is_positive_integer(x) for x in expr)
        self._make_prompt(
            spaced_attribute_name,
            validation_function=function,
            help_template=help_template,
            default_value=default_value,
            )

    def append_snake_case_file_name(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends snake case file name.

        Returns prompt.
        '''
        help_template = 'value must be snake case file name.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=stringtools.is_snake_case_file_name,
            help_template=help_template,
            default_value=default_value,
            )

    def append_snake_case_file_name_with_extension(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends snake case file name with extension.

        Returns prompt.
        '''
        help_template = 'value must be snake case file name with extension.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=\
                stringtools.is_snake_case_file_name_with_extension,
            help_template=help_template,
            default_value=default_value,
            )

    def append_snake_case_package_name(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends snake case package name.

        Returns prompt.
        '''
        help_template = 'value must be snake case package name, 3 <= length.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_snake_case_package_name,
            help_template=help_template,
            default_value=default_value,
            )

    def append_snake_case_string(
        self,
        spaced_attribute_name,
        default_value=None,
        allow_empty=False,
        ):
        r'''Appends snake case string.

        Returns prompt.
        '''
        def is_nonempty_snake_case_string(expr):
            if stringtools.is_snake_case(expr):
                return bool(expr)
            return False
        if allow_empty:
            help_template = 'value must be snake case string.'
            validation_function = stringtools.is_snake_case
        else:
            help_template = 'value must be nonempty snake case string.'
            validation_function = is_nonempty_snake_case_string
        self._make_prompt(
            spaced_attribute_name,
            validation_function=validation_function,
            help_template=help_template,
            default_value=default_value,
            )

    def append_space_delimited_lowercase_string(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends space-delimited lowercase string.

        Returns prompt.
        '''
        help_template = 'value must be space-delimited lowercase string.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=stringtools.is_space_delimited_lowercase,
            help_template=help_template,
            default_value=default_value,
            )

    def append_string(
        self,
        spaced_attribute_name,
        default_value=None,
        allow_empty=True,
        ):
        r'''Appends string.

        Returns prompt.
        '''
        if allow_empty:
            validation_function = predicates.is_string
            help_template = 'value must be string.'
        else:
            validation_function = predicates.is_nonempty_string
            help_template = 'value must be nonempty string.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=validation_function,
            help_template=help_template,
            default_value=default_value,
            )

    def append_string_or_none(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends string or none.

        Returns prompt.
        '''
        help_template = 'value must be string or none.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_string_or_none,
            help_template=help_template,
            default_value=default_value,
            )

    def append_strings(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends strings.

        Returns prompt.
        '''
        help_template = 'value must be tuple of strings.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.are_strings,
            help_template=help_template,
            default_value=default_value,
            )

    def append_tempo(
        self,
        spaced_attribute_name,
        default_value=None,
        ):
        r'''Appends tempo.

        Returns prompt.
        '''
        help_template = 'value must successfully initialize tempo.'
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_tempo_token,
            help_template=help_template,
            default_value=default_value,
            )

    def append_yes_no_string(
        self,
        spaced_attribute_name,
        default_value=None,
        include_chevron=False,
        ):
        r'''Appends yes / no string.

        Returns prompt.
        '''
        help_template = "value for '{}' must be 'y' or 'n'."
        self._make_prompt(
            spaced_attribute_name,
            validation_function=predicates.is_yes_no_string,
            help_template=help_template,
            default_value=default_value,
            include_chevron=include_chevron,
            )