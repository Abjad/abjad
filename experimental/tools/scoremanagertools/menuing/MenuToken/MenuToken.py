from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuToken(list, AbjadObject):
    '''Menu token.

    The tuple-only code indicates the following:

        * a value-tuple token has length 3
        * a prepopulated return value tuple token has length 4

    Return menu token.
    '''

    ### INITIALIZER ###

    def __init__(self, *args):
        assert 1 <= len(args) <= 4, repr(args)
        for arg in args:
            self.append(arg)
        self._number = None

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({})'.format(self._class_name, ', '.join([repr(x) for x in self]))

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def is_string_token(self):
        return len(self) == 1 and isinstance(self[0], str)

    @property
    def is_tuple_token(self):
        return not self.is_string_token

    # TODO: this can probably deprecate in favor of self.token_to_key_body_and_existing_value
    @property
    def key_and_body(self):
        if self.is_string_token:
            key, body = None, self[0]
        else:
            key, body = self[:2]
        return key, body

    @property 
    def key_body_and_existing_value(self):
        if self.is_string_token:
            key, body, existing_value = None, self[0], None
        elif len(self) == 2:
            key, body, existing_value = self[0], self[1], None
        elif len(self) == 3:
            key, body, existing_value = self
        elif len(self) == 4:
            key, body, existing_value = self[:3]
        else:
            raise ValueError(self)
        return key, body, existing_value

    @property
    def key_body_existing_value_and_prepopulated_return_value(self):
        key = body = existing_value = prepopulated_return_value = None
        if self.is_string_token:
            body = self[0]
        elif len(self) == 2:
            key, body = self
        elif len(self) == 3:
            key, body, existing_value = self
        elif len(self) == 4:
            key, body, existing_value, prepopulated_return_value = self
        else:
            raise ValueError(self)
        return key, body, existing_value, prepopulated_return_value

    @property
    def number(self):
        return self._number

    ### PUBLIC METHODS ###

    def get_menu_token_return_value(self, return_value_attribute):
        if self.is_string_token:
            return self[0]
        else:
            if return_value_attribute == 'key':
                return self[0]
            elif return_value_attribute == 'body':
                return self[1]
            elif return_value_attribute == 'number':
                return
            elif return_value_attribute == 'prepopulated':
                return self[3]
            else:
                raise ValueError(return_value_attribute)

    # TODO: replace token.key_and_body and also
    #       replace token.get_menu_token_return_value().
    # TODO: unpack all menu tokens only once at runtime.
    def unpack(self, return_value_attribute):
        number = self.number
        key, body = self.key_and_body
        return_value = self.get_menu_token_return_value(return_value_attribute)
        return number, key, body, return_value

