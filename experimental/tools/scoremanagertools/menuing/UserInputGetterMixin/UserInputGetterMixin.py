import functools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.scoremanagertools import predicates


class UserInputGetterMixin(AbjadObject):

    ### PUBLIC METHODS ###

    def append_argument_range(self, 
        spaced_attribute_name, 
        argument_list, 
        default=None):
        message = 'value for {!r} must be argument range.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.argument_lists[-1] = argument_list
        test = lambda expr: \
            predicates.is_readable_argument_range_string_for_argument_list(
            expr, argument_list)
        self.tests.append(test)

    def append_articulation(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must successfully initialize articulation.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_articulation_token)

    def append_articulations(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must successfully initialize articulations.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.are_articulation_tokens)

    def append_available_underscore_delimited_lowercase_package_name(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be available '
        message += 'underscore-delimited lowercase package name '
        message += 'of length at least 3.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(
            predicates.is_available_underscore_delimited_lowercase_package_name)

    def append_boolean(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be boolean.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_boolean)

    def append_clef(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must successfully initialize clef mark.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_clef_token)

    def append_constellation_circuit_id_pair(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be valid constellation circuit id pair.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(lambda x: True)

    def append_direction_string(self, spaced_attribute_name, default=None):
        message = "value for {!r} must be 'up or 'down'."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_direction_string)

    def append_duration(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be duration.'
        self.append_something(spaced_attribute_name, message, default=default)
        execs = []
        execs.append('from abjad import *')
        execs.append('value = Duration({})')
        self.execs[-1] = execs
        self.tests.append(predicates.is_duration_token)

    def append_dynamic(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must successfully initialize dynamic mark.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_dynamic_token)

    def append_dynamics(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be list of dynamic mark initializers.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.are_dynamic_tokens)

    def append_existing_package_name(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be existing package name.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_existing_package_name)

    def append_expr(self, spaced_attribute_name, default=None):
        message = 'value for {!r} may be anything.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(lambda expr: True)

    def append_hairpin_token(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be hairpin menu_entry.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_hairpin_token)

    def append_hairpin_tokens(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be hairpin menu_entries.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.are_hairpin_tokens)

    def append_hyphen_delimited_lowercase_file_name(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be '
        message += 'hyphen-delimited lowercase file name.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(stringtools.is_dash_case_file_name)

    def append_integer(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be integer.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_integer)

    def append_integer_in_range(self, spaced_attribute_name,
        start=None, stop=None, allow_none=False, default=None):
        message = 'value for {!r} must be '
        message += 'integer between {} and {}, inclusive.'
        self.append_something(
            spaced_attribute_name, message, (start, stop), default=default)
        test = functools.partial(
            predicates.is_integer_in_range, 
            start=start, stop=stop, allow_none=allow_none)
        self.tests.append(test)

    def append_integers(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be integers.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(lambda x: all([predicates.is_integer(y) for y in x]))

    def append_list(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be list.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_list)

    def append_lists(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be lists.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.are_lists)

    def append_markup(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be markup.'
        self.append_something(spaced_attribute_name, message, default=default)
        execs = []
        execs.append('from abjad import *')
        execs.append('value = markuptools.Markup({})')
        self.execs[-1] = execs
        self.tests.append(predicates.is_markup)

    def append_material_package_maker_class_name(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be '
        message += 'uppercamelcase string ending in -Maker.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(
            lambda x: stringtools.is_upper_camel_case_string(x) 
            and x.endswith('Maker'))

    def append_named_chromatic_pitch(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be named chromatic pitch.'
        self.append_something(spaced_attribute_name, message, default=default)
        execs = []
        execs.append('from abjad import *')
        execs.append('value = pitchtools.NamedChromaticPitch({})')
        self.execs[-1] = execs
        self.tests.append(predicates.is_named_chromatic_pitch)

    def append_nonnegative_integers(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be nonnegative integers.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(
            lambda x: all([isinstance(y, int) and 0 <= y for y in x]))

    def append_nonzero_integers(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be nonzero integers.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(
            lambda x: all([isinstance(y, int) and not y == 0 for y in x]))

    def append_pitch_range(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be pitch range.'
        self.append_something(spaced_attribute_name, message, default=default)
        execs = []
        execs.append('from abjad import *')
        execs.append('value = pitchtools.PitchRange({})')
        self.execs[-1] = execs
        self.tests.append(predicates.is_pitch_range_or_none)

    def append_positive_integer_power_of_two(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be positive integer power of two.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(mathtools.is_positive_integer_power_of_two)

    def append_positive_integers(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be positive integers.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(
            lambda expr: all([mathtools.is_positive_integer(x) for x in expr]))

    def append_something(self, spaced_attribute_name, message,
        additional_message_arguments=None, default=None, include_chevron=True):
        assert isinstance(spaced_attribute_name, str)
        self.prompts.append(spaced_attribute_name)
        self.argument_lists.append([])
        self.execs.append([])
        if additional_message_arguments is None:
            additional_message_arguments = []
        self.helps.append(message.format(
            spaced_attribute_name, *additional_message_arguments))
        self.defaults.append(default)
        self.chevrons.append(include_chevron)

    def append_space_delimited_lowercase_string(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be space-delimited lowercase string.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(stringtools.is_space_delimited_lowercase_string)

    def append_string(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be string.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_string)

    def append_string_or_none(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be string or none.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_string_or_none)

    def append_strings(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must be strings.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.are_strings)

    def append_symbolic_pitch_range_string(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be '
        message += 'symbolic pitch range string. Ex: [A0, C8].'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(pitchtools.is_symbolic_pitch_range_string)

    # TODO: fix bug to make (Duration(1, 4), 72) work
    def append_tempo(self, spaced_attribute_name, default=None):
        message = 'value for {!r} must successfully initialize tempo mark.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_tempo_token)

    def append_underscore_delimited_lowercase_file_name(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be '
        message += 'underscore-delimited lowercase file name.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(
            stringtools.is_snake_case_file_name)

    def append_underscore_delimited_lowercase_file_name_with_extension(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be '
        message += 'underscore-delimited lowercase file name with extension.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(
            stringtools.is_snake_case_file_name_with_extension)

    def append_underscore_delimited_lowercase_package_name(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be '
        message += 'underscore-delimited lowercase package name '
        message += 'of length at least 3.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(
            predicates.is_snake_case_package_name)

    def append_underscore_delimited_lowercase_string(self, 
        spaced_attribute_name, default=None):
        message = 'value for {!r} must be '
        message += 'underscore-delimited lowercase string.'
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(stringtools.is_snake_case_string)

    def append_yes_no_string(self, 
        spaced_attribute_name, default=None, include_chevron=False):
        message = "value for '{}' must be 'y' or 'n'."
        self.append_something(
            spaced_attribute_name, message, 
            default=default, include_chevron=include_chevron)
        self.tests.append(predicates.is_yes_no_string)
