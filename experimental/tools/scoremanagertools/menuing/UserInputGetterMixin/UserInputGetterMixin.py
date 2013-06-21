import functools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.scoremanagertools import predicates


class UserInputGetterMixin(AbjadObject):

    ### PRIVATE METHODS ###

    def _make_prompt(self, 
        spaced_attribute_name, 
        help_template=None,
        validation_function=None,
        additional_help_template_arguments=None, 
        setup_statements=None,
        default_value=None, 
        include_chevron=True,
        target_menu_section=None,
        ):
        from experimental.tools import scoremanagertools
        prompt = scoremanagertools.menuing.UserInputGetterPrompt(
            spaced_attribute_name, 
            help_template=help_template,
            validation_function=validation_function,
            additional_help_template_arguments=\
                additional_help_template_arguments, 
            setup_statements=setup_statements,
            default_value=default_value, 
            include_chevron=include_chevron,
            target_menu_section=target_menu_section,
            )
        self._prompts.append(prompt)

    ### PUBLIC METHODS ###

    def append_menu_section_range(
        self, 
        spaced_attribute_name, 
        target_menu_section, 
        default_value=None):
        help_template = 'value for {!r} must be argument range.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_string, 
            help_template=help_template,
            target_menu_section=target_menu_section,
            default_value=default_value,
            )

    def append_articulation(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r}'
        help_template += ' must successfully initialize articulation.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_ariculation_token,
            help_template=help_template,
            default_value=default_value,
            )

    def append_articulations(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} '
        help_template += ' must successfully initialize articulations.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.are_articulation_tokens,
            help_template=help_template,
            default_value=default_value,
            )

    def append_available_snake_case_package_name(
        self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be available '
        help_template += 'underscore-delimited lowercase package name '
        help_template += 'of length at least 3.'
        validation_function = predicates.is_available_snake_case_package_name
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=validation_function,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_boolean(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be boolean.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_boolean,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_clef(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r}'
        help_template += ' must successfully initialize clef mark.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_clef_token,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_constellation_circuit_id_pair(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r}'
        help_template += ' must be valid constellation circuit id pair.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=lambda x: True,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_dash_case_file_name(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be dash case file name.'
        self._make_prompt(
            spaced_attribute_name, 
            help_template, 
            validation_function=stringtools.is_dash_case_file_name,
            default_value=default_value,
            )

    def append_direction_string(
        self, spaced_attribute_name, default_value=None):
        help_template = "value for {!r} must be 'up or 'down'."
        self._make_prompt(
            spaced_attribute_name, 
            help_template=help_template, 
            validation_function=predicates.is_direction_string,
            default_value=default_value,
            )

    def append_duration(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be duration.'
        setup_statements = []
        setup_statements.append('from abjad import *')
        setup_statements.append('value = Duration({})')
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_duration_token,
            help_template=help_template, 
            setup_statements=setup_statements,
            default_value=default_value,
            )

    def append_dynamic(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r}'
        help_template += ' must successfully initialize dynamic mark.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_dynamic_token,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_dynamics(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r}'
        help_template += ' must be list of dynamic mark initializers.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.are_dynamic_tokens,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_existing_package_name(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be existing package name.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_existing_package_name,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_expr(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} may be anything.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=lambda expr: True,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_hairpin_token(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be hairpin menu_entry.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_hairpin_token,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_hairpin_tokens(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be hairpin menu_entries.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.are_hairpin_tokens,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_integer(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be integer.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_integer,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_integer_in_range(
        self, spaced_attribute_name,
        start=None, stop=None, allow_none=False, default_value=None):
        validation_function = functools.partial(
            predicates.is_integer_in_range, 
            start=start, stop=stop, allow_none=allow_none)
        help_template = 'value for {!r} must be '
        help_template += 'integer between {} and {}, inclusive.'
        self._make_prompt(
            spaced_attribute_name, 
            help_template=help_template, 
            validation_function=validation_function,
            additional_help_template_arguments=(start, stop), 
            default_value=default_value,
            )

    def append_integers(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be integers.'
        function = lambda x: all([predicates.is_integer(y) for y in x])
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=function,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_list(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be list.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_list,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_lists(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be lists.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.are_lists,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_markup(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be markup.'
        setup_statements = []
        setup_statements.append('from abjad import *')
        setup_statements.append('value = markuptools.Markup({})')
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_markup,
            help_template=help_template, 
            setup_statements=setup_statements,
            default_value=default_value,
            )

    def append_material_package_maker_class_name(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be '
        help_template += 'uppercamelcase string ending in -Maker.'
        function = lambda x: \
            stringtools.is_upper_camel_case_string(x) and \
            x.endswith('Maker')
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=function,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_named_chromatic_pitch(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be named chromatic pitch.'
        setup_statements = []
        setup_statements.append('from abjad import *')
        setup_statements.append('value = pitchtools.NamedChromaticPitch({})')
        self._make_prompt(
            spaced_attribute_name, 
            help_template=help_template, 
            validation_function=predicates.is_named_chromatic_pitch,
            setup_statements=setup_statements,
            default_value=default_value,
            )

    def append_nonnegative_integers(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be nonnegative integers.'
        function = lambda x: all(isinstance(y, int) and 0 <= y for y in x)
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=function,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_nonzero_integers(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be nonzero integers.'
        function = lambda x: all(isinstance(y, int) and not y == 0 for y in x)
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=function,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_pitch_range(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be pitch range.'
        setup_statements = []
        setup_statements.append('from abjad import *')
        setup_statements.append('value = pitchtools.PitchRange({})')
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_pitch_range_or_none,
            help_template=help_template, 
            setup_statements=setup_statements,
            default_value=default_value,
            )
        self._setup_statements[-1] = setup_statements

    def append_positive_integer_power_of_two(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r}'
        help_template += ' must be positive integer power of two.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=mathtools.is_positive_integer_power_of_two,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_positive_integers(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be positive integers.'
        function = lambda expr: all(
            mathtools.is_positive_integer(x) for x in expr)
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=function,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_snake_case_file_name(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be '
        help_template += 'underscore-delimited lowercase file name.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=stringtools.is_snake_case_file_name,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_snake_case_file_name_with_extension(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be '
        help_template += 'snake case file name with extension.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=\
                stringtools.is_snake_case_file_name_with_extension,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_snake_case_package_name(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be '
        help_template += 'underscore-delimited lowercase package name '
        help_template += 'of length at least 3.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_snake_case_package_name,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_snake_case_string(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be '
        help_template += 'underscore-delimited lowercase string.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=stringtools.is_snake_case_string,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_space_delimited_lowercase_string(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} '
        help_template += ' must be space-delimited lowercase string.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=stringtools.is_space_delimited_lowercase_string,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_string(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be string.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_string,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_string_or_none(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be string or none.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_string_or_none,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_strings(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be strings.'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.are_strings,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_symbolic_pitch_range_string(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} '
        help_template += ' must be symbolic pitch range string.'
        help_template += ' Ex: [A0, C8].'
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=pitchtools.is_symbolic_pitch_range_string,
            help_template=help_template, 
            default_value=default_value,
            )

    # TODO: fix bug to make (Duration(1, 4), 72) work
    def append_tempo(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must successfully initialize tempo mark.'
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
        include_chevron=False):
        help_template = "value for '{}' must be 'y' or 'n'."
        self._make_prompt(
            spaced_attribute_name, 
            validation_function=predicates.is_yes_no_string,
            help_template=help_template, 
            default_value=default_value, 
            include_chevron=include_chevron,
            )
