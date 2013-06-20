import functools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.scoremanagertools import predicates


class UserInputGetterMixin(AbjadObject):

    ### PRIVATE METHODS ###

    def _append_something(self, 
        spaced_attribute_name, 
        help_template=None,
        validation_function=None,
        additional_help_template_arguments=None, 
        default_value=None, 
        include_chevron=True,
        argument_list=None,
        ):
        assert isinstance(help_template, str)
        assert isinstance(spaced_attribute_name, str)
        self._prompt_strings.append(spaced_attribute_name)
        argument_list = argument_list or []
        self._argument_lists.append(argument_list)
        self._setup_statements.append([])
        if additional_help_template_arguments is None:
            additional_help_template_arguments = []
        help_string = help_template.format(
            spaced_attribute_name, *additional_help_template_arguments)
        self._help_strings.append(help_string)
        self._default_values.append(default_value)
        self._chevron_inclusion_indicators.append(include_chevron)
        if validation_function is not None:
            self._validation_functions.append(validation_function)

    ### PUBLIC METHODS ###

    def append_argument_range(self, 
        spaced_attribute_name, 
        argument_list, 
        default_value=None):
        validation_function = lambda expr: \
            predicates.is_readable_argument_range_string_for_argument_list(
            expr, argument_list)
        help_template = 'value for {!r} must be argument range.'
        self._append_something(
            spaced_attribute_name, 
            validation_function=validation_function, 
            help_template=help_template,
            argument_list=argument_list,
            default_value=default_value,
            )

    def append_articulation(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r}'
        help_template += ' must successfully initialize articulation.'
        self._append_something(
            spaced_attribute_name, 
            validation_function=predicates.is_ariculation_token,
            help_template=help_template,
            default_value=default_value,
            )

    def append_articulations(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} '
        help_template += ' must successfully initialize articulations.'
        self._append_something(
            spaced_attribute_name, 
            validation_function=predicates.are_articulation_tokens,
            help_template=help_template,
            default_value=default_value,
            )

    def append_available_underscore_delimited_lowercase_package_name(
        self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be available '
        help_template += 'underscore-delimited lowercase package name '
        help_template += 'of length at least 3.'
        self._append_something(
            spaced_attribute_name, 
            validation_function=predicates.is_available_underscore_delimited_lowercase_package_name,
            help_template=help_template, 
            default_value=default_value,
            )

    def append_boolean(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be boolean.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.is_boolean)

    def append_clef(
        self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must successfully initialize clef mark.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.is_clef_token)

    def append_constellation_circuit_id_pair(self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be valid constellation circuit id pair.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(lambda x: True)

    def append_direction_string(self, spaced_attribute_name, default_value=None):
        help_template = "value for {!r} must be 'up or 'down'."
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.is_direction_string)

    def append_duration(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be duration.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        setup_statements = []
        setup_statements.append('from abjad import *')
        setup_statements.append('value = Duration({})')
        self._setup_statements[-1] = setup_statements
        self._validation_functions.append(predicates.is_duration_token)

    def append_dynamic(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must successfully initialize dynamic mark.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.is_dynamic_token)

    def append_dynamics(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be list of dynamic mark initializers.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.are_dynamic_tokens)

    def append_existing_package_name(self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be existing package name.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.is_existing_package_name)

    def append_expr(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} may be anything.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(lambda expr: True)

    def append_hairpin_token(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be hairpin menu_entry.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.is_hairpin_token)

    def append_hairpin_tokens(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be hairpin menu_entries.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.are_hairpin_tokens)

    def append_hyphen_delimited_lowercase_file_name(self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be '
        help_template += 'hyphen-delimited lowercase file name.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(stringtools.is_dash_case_file_name)

    def append_integer(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be integer.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.is_integer)

    def append_integer_in_range(self, spaced_attribute_name,
        start=None, stop=None, allow_none=False, default_value=None):
        validation_function = functools.partial(
            predicates.is_integer_in_range, 
            start=start, stop=stop, allow_none=allow_none)
        help_template = 'value for {!r} must be '
        help_template += 'integer between {} and {}, inclusive.'
        self._append_something(
            spaced_attribute_name, 
            help_template=help_template, 
            validation_function=validation_function,
            additional_help_template_arguments=(start, stop), 
            default_value=default_value,
            )

    def append_integers(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be integers.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(lambda x: all([predicates.is_integer(y) for y in x]))

    def append_list(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be list.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.is_list)

    def append_lists(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be lists.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.are_lists)

    def append_markup(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be markup.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        setup_statements = []
        setup_statements.append('from abjad import *')
        setup_statements.append('value = markuptools.Markup({})')
        self._setup_statements[-1] = setup_statements
        self._validation_functions.append(predicates.is_markup)

    def append_material_package_maker_class_name(self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be '
        help_template += 'uppercamelcase string ending in -Maker.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(
            lambda x: stringtools.is_upper_camel_case_string(x) 
            and x.endswith('Maker'))

    def append_named_chromatic_pitch(self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be named chromatic pitch.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        setup_statements = []
        setup_statements.append('from abjad import *')
        setup_statements.append('value = pitchtools.NamedChromaticPitch({})')
        self._setup_statements[-1] = setup_statements
        self._validation_functions.append(predicates.is_named_chromatic_pitch)

    def append_nonnegative_integers(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be nonnegative integers.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(
            lambda x: all([isinstance(y, int) and 0 <= y for y in x]))

    def append_nonzero_integers(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be nonzero integers.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(
            lambda x: all([isinstance(y, int) and not y == 0 for y in x]))

    def append_pitch_range(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be pitch range.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        setup_statements = []
        setup_statements.append('from abjad import *')
        setup_statements.append('value = pitchtools.PitchRange({})')
        self._setup_statements[-1] = setup_statements
        self._validation_functions.append(predicates.is_pitch_range_or_none)

    def append_positive_integer_power_of_two(self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be positive integer power of two.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(mathtools.is_positive_integer_power_of_two)

    def append_positive_integers(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be positive integers.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(
            lambda expr: all([mathtools.is_positive_integer(x) for x in expr]))

    def append_space_delimited_lowercase_string(self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be space-delimited lowercase string.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(stringtools.is_space_delimited_lowercase_string)

    def append_string(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be string.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.is_string)

    def append_string_or_none(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be string or none.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.is_string_or_none)

    def append_strings(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be strings.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.are_strings)

    def append_symbolic_pitch_range_string(self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be '
        help_template += 'symbolic pitch range string. Ex: [A0, C8].'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(pitchtools.is_symbolic_pitch_range_string)

    # TODO: fix bug to make (Duration(1, 4), 72) work
    def append_tempo(self, spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must successfully initialize tempo mark.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(predicates.is_tempo_token)

    def append_underscore_delimited_lowercase_file_name(self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be '
        help_template += 'underscore-delimited lowercase file name.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(
            stringtools.is_snake_case_file_name)

    def append_underscore_delimited_lowercase_file_name_with_extension(self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be '
        help_template += 'underscore-delimited lowercase file name with extension.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(
            stringtools.is_snake_case_file_name_with_extension)

    def append_underscore_delimited_lowercase_package_name(self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be '
        help_template += 'underscore-delimited lowercase package name '
        help_template += 'of length at least 3.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(
            predicates.is_snake_case_package_name)

    def append_underscore_delimited_lowercase_string(self, 
        spaced_attribute_name, default_value=None):
        help_template = 'value for {!r} must be '
        help_template += 'underscore-delimited lowercase string.'
        self._append_something(spaced_attribute_name, help_template, default_value=default_value)
        self._validation_functions.append(stringtools.is_snake_case_string)

    def append_yes_no_string(self, 
        spaced_attribute_name, default_value=None, include_chevron=False):
        help_template = "value for '{}' must be 'y' or 'n'."
        self._append_something(
            spaced_attribute_name, help_template, 
            default_value=default_value, include_chevron=include_chevron)
        self._validation_functions.append(predicates.is_yes_no_string)
