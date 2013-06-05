from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuToken(AbjadObject):
    '''Menu menu_token.

    Return menu menu_token.
    '''

    ### CLASS VARIABLES ###

    return_value_attributes = ('body', 'key', 'number', 'prepopulated')

    ### INITIALIZER ###

    def __init__(self, expr, number=None, is_keyed=False, return_value_attribute=None):
        if isinstance(expr, str):
            expr = (expr, )
        assert isinstance(expr, tuple), repr(expr)
        assert 1 <= len(expr) <= 4, repr(expr)
        self._number = number
        self._is_keyed = is_keyed
        assert return_value_attribute in self.return_value_attributes, repr(return_value_attribute)
        self._return_value_attribute = return_value_attribute
        if self.return_value_attribute == 'key':
            assert self.is_keyed or 1 < len(expr)
        body, key, existing_value, prepopulated_return_value = None, None, None, None
        if len(expr) == 1:
            body = expr[0]
            if self.is_keyed:
                key = body
        elif len(expr) == 2:
            key, body = expr
        elif len(expr) == 3:
            key, body, existing_value = expr
        elif len(expr) == 4:
            key, body, existing_value, prepopulated_return_value = expr
        self._key = key
        assert body
        self._body = body
        self._existing_value = existing_value
        self._prepopulated_return_value = prepopulated_return_value
        if self.return_value_attribute == 'number':
            return_value = str(self.number)
        elif self.return_value_attribute == 'body':
            return_value = self.body
        elif self.return_value_attribute == 'key':
            if self.key:
                return_value = self.key
            else:
                return_value = self.body
        elif self.return_value_attribute == 'prepopulated':
            assert prepopulated_return_value
            return_value = prepopulated_return_value
        self._return_value = return_value
        assert self.return_value
        if self.is_keyed:
            assert self.key
        matches = []
        if self.number:
            matches.append(str(self.number))
        if self.is_keyed:
            matches.append(self.key)
        self._matches = tuple(matches)
        normalized_body = stringtools.strip_diacritics_from_binary_string(self.body).lower()
        self._normalized_body = normalized_body
        
    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}()'.format(self._class_name)

    ### PRIVATE METHODS ###

    def _to_tuple(self):
        return self.key, self.body, self.existing_value, self.prepopulated_return_value

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def body(self):
        return self._body

    @property
    def existing_value(self):
        return self._existing_value

    @property
    def is_keyed(self):
        return self._is_keyed

    @property
    def key(self):
        return self._key

    @property
    def number(self):
        return self._number

    @property
    def prepopulated_return_value(self):
        return self._prepopulated_return_value

    @property
    def return_value(self):
        return self._return_value

    @property
    def return_value_attribute(self):
        return self._return_value_attribute

    ### PUBLIC METHODS ###

    def matches(self, user_input):
        if user_input in self._matches:
            return True
        if 3 <= len(user_input) and self._normalized_body.startswith(user_input):
            return True
