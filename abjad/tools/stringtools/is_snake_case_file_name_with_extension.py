# -*- coding: utf-8 -*-
import re
import six
from abjad.tools.stringtools.is_snake_case \
    import underscore_delimited_lowercase_regex_body


underscore_delimited_lowercase_file_name_with_extension_regex_body = """
    {}
    \.
    [a-z,0-9]+
    """.format(underscore_delimited_lowercase_regex_body)

underscore_delimited_lowercase_file_name_with_extension_regex = re.compile(
    '^{}$'.format(underscore_delimited_lowercase_file_name_with_extension_regex_body),
    re.VERBOSE,
    )


def is_snake_case_file_name_with_extension(argument):
    r'''Is true when `argument` is a string and is underscore-delimited lowercase
    file name with extension.

    ..  container:: example

        ::

            >>> stringtools.is_snake_case_file_name_with_extension('foo_bar.blah')
            True

    Otherwise false:

    ..  container:: example

        ::

            >>> stringtools.is_snake_case_file_name_with_extension('foo.bar.blah')
            False

    Returns true or false.
    '''
    if not isinstance(argument, six.string_types):
        return False
    if argument == '':
        return True
    return bool(underscore_delimited_lowercase_file_name_with_extension_regex.match(argument))
