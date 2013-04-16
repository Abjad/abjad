import re
import numbers
from experimental.tools.musicexpressiontools.PayloadExpression import PayloadExpression


class PitchClassTransformExpression(PayloadExpression):
    '''Pitch-class transform expression.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None):
        if isinstance(payload, type(self)):
            payload = payload.payload
        assert isinstance(payload, str), repr(payload)
        PayloadExpression.__init__(self, payload=payload)
        simple_strings = self._parse_complex_transform_string(payload)
        transform_functions = [self._simple_string_to_transform_function(x) for x in simple_strings]
        self._transform_functions = transform_functions

    ### SPECIAL METHODS ###

    def __call__(self, pitch_number):
        assert isinstance(pitch_number, numbers.Number), repr(pitch_number)
        result = pitch_number
        for transform_function in reversed(self.transform_functions):
            result = transform_function(result)
        return result

    ### PRIVATE METHODS ###

    def _parse_complex_transform_string(self, complex_string):
        simple_string_pattern = re.compile(r"""(M[0-9]+|T[0-9]+|I)""")
        simple_strings = simple_string_pattern.findall(complex_string)
        return simple_strings

    def _simple_string_to_transform_function(self, simple_string):
        if simple_string.startswith('T'):
            index = int(simple_string.replace('T', ''))
            return lambda x: (x + index) % 12
        elif simple_string == 'I':
            return lambda x: (12 - x) % 12
        elif simple_string.startswith('M'):
            index = int(simple_string.replace('M', ''))
            return lambda x: (index * x) % 12
        else:
            raise ValueError(simple_string)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def transform_functions(self):
        '''Pitch-class transform expression transform functions.

        Return list.
        '''
        return self._transform_functions
