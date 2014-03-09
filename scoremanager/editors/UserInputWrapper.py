# -*- encoding: utf-8 -*-
import collections


class UserInputWrapper(collections.OrderedDict):
    r'''User input wrapper.

    ..  container:: example

        ::

            >>> wrapper = scoremanager.editors.UserInputWrapper()
            >>> wrapper['flavor'] = 'cherry'
            >>> wrapper['duration'] = Duration(1, 4)

    '''

    ### INITIALIZER ###

    def __init__(self, *arg):
        collections.OrderedDict.__init__(self, *arg)
        self._user_input_module_import_statements = []

    ### PUBLIC PROPERTIES ###

    @property
    def editable_lines(self):
        r'''Editable lines of user input wrapper.

        ..  container:: example

            ::

                >>> wrapper.editable_lines
                ["flavor: 'cherry'", 'duration: Duration(1, 4)']

        Returns list.
        '''
        pairs = list(self.iteritems())
        lines = []
        for pair in pairs:
            key, value = pair
            key = key.replace('_', ' ')
            if value is None:
                line = '{}: '.format(key)
            else:
                line = '{}: {!r}'.format(key, value)
            lines.append(line)
        return lines

    # TODO: maybe replace with __format__
    @property
    def formatted_lines(self):
        r'''Formatted lines of user input wrapper.

        ..  container:: example

            ::

                >>> for line in wrapper.formatted_lines:
                ...     print line
                user_input_wrapper = UserInputWrapper([
                    ('flavor', 'cherry'),
                    ('duration', durationtools.Duration(1, 4))])

        Returns list.
        '''
        result = []
        items = self.list_items()
        if not items:
            result.append(
                'user_input_wrapper = {}([])'.format(type(self).__name__))
        else:
            result.append(
                'user_input_wrapper = {}(['.format(type(self).__name__))
            for name, value in items[:-1]:
                template = '\t({!r}, {!r}),'
                if hasattr(value, '_storage_format_specification'):
                    template = '\t({!r}, {:storage}),'
                line = template.format(name, value)
                result.append(line)
            name, value = items[-1]
            template = '\t({!r}, {!r})])'
            if hasattr(value, '_storage_format_specification'):
                template = '\t({!r}, {:storage})])'
            line = template.format(name, value)
            result.append(line)
        return result

    @property
    def is_complete(self):
        r'''Is true when user input wrapper is complete.
        Otherwise false.

        ..  container:: example

            ::

                >>> wrapper.is_complete
                True

        Returns boolean.
        '''
        return bool(None not in self.itervalues())

    @property
    def is_empty(self):
        r'''Is true when user input wrapper is empty.
        Otherwise false.

        ..  container:: example

            ::

                >>> wrapper.is_empty
                False

        Returns boolean.
        '''
        return all(x is None for x in self.itervalues())

    @property
    def is_partially_complete(self):
        r'''Is true when user input wrapper is partially complete.
        Otherwise false.

        ..  container:: example

            ::

                >>> wrapper.is_partially_complete
                False

        Returns boolean.
        '''
        return not self.is_complete and not self.is_empty

    @property
    def user_input_module_import_statements(self):
        r'''User input module import statments.

        ..  container:: example

            ::

                >>> wrapper.user_input_module_import_statements
                ['from scoremanager.editors import UserInputWrapper']

        Returns sorted list.
        '''
        result = [
            'from scoremanager.editors import UserInputWrapper']
        result.extend(self._user_input_module_import_statements)
        result.sort()
        return result

    ### PUBLIC METHODS ###

    def clear(self):
        r'''Clears user input wrapper.

        Returns none.
        '''
        for key in self:
            self[key] = None

    def list_items(self):
        r'''Lists items in user input wrapper.

        ..  container:: example

            ::

                >>> for item in wrapper.list_items():
                ...     item
                ('flavor', 'cherry')
                ('duration', Duration(1, 4))

        Returns list.
        '''
        return list(self.iteritems())

    def list_keys(self):
        r'''Lists keys in user input wrapper.

        ..  container:: example

            ::

                >>> for key in wrapper.list_keys():
                ...     key
                'flavor'
                'duration'

        Returns list.
        '''
        return list(self.iterkeys())

    def list_values(self):
        r'''Lists values in user input wrapper.

        ..  container:: example

            ::

                >>> for value in wrapper.list_values():
                ...     value
                'cherry'
                Duration(1, 4)

        Returns list.
        '''
        return list(self.itervalues())
