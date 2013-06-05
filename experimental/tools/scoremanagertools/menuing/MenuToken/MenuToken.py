from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuToken(list, AbjadObject):
    '''Menu token.

    Return menu token.
    '''

    ### CLASS VARIABLES ###

    return_value_attributes = ('body', 'key', 'number', 'prepopulated')

    ### INITIALIZER ###

    def __init__(self, expr, number=None, is_keyed=False, return_value_attribute=None):
        if isinstance(expr, str):
            self.append(expr)
        elif isinstance(expr, (tuple, type(self))):
            assert 1 <= len(expr) <= 4, repr(expr)
            for x in expr:
                self.append(x)
        else:
            raise TypeError(expr)
        self._number = number
        self._is_keyed = is_keyed
        assert return_value_attribute in self.return_value_attributes, repr(return_value_attribute)
        self._return_value_attribute = return_value_attribute
        if self.return_value_attribute == 'key':
            assert self.is_keyed or 1 < len(self)
        body, key, existing_value, prepopulated_return_value = None, None, None, None
        if len(self) == 1:
            body = self[0]
            if self.is_keyed:
                key = body
        elif len(self) == 2:
            key, body = self
        elif len(self) == 3:
            key, body, existing_value = self
        elif len(self) == 4:
            key, body, existing_value, prepopulated_return_value = self
        self._key = key
        assert body
        self._body = body
        self._existing_value = existing_value
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
        return '{}({})'.format(self._class_name, ', '.join([repr(x) for x in self]))

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
