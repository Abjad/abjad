from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuToken(list, AbjadObject):
    '''Menu token.

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
    def body(self):
        return self.key_body_and_existing_value[1]

    @property
    def is_string_token(self):
        return len(self) == 1 and isinstance(self[0], str)

    @property
    def key(self):
        return self.key_body_and_existing_value[0]

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

    @property
    def prepopulated_return_value(self):
        return self.key_body_existing_value_and_prepopulated_return_value[3]

    # TODO: harmonize this implementation with that in MenuSection.unpack_menu_tokens()
    @property
    def return_value(self):
        if self.is_string_token:
            return self[0]
        else:
            if self.return_value_attribute == 'key':
                return self[0]
            elif self.return_value_attribute == 'body':
                return self[1]
            elif self.return_value_attribute == 'number':
                return
            elif self.return_value_attribute == 'prepopulated':
                return self[3]
            else:
                raise ValueError(return_value_attribute)

    @property
    def return_value_attribute(self):
        return self._return_value_attribute
