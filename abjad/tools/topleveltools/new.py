# -*- coding: utf-8 -*-
import types


def new(expr, **kwargs):
    r'''Makes new `expr` with optional new `kwargs`.

    Returns new object with the same type as `expr`.
    '''
    def update_dictionaries(
        expr,
        keyword_argument_dictionary,
        positional_argument_dictionary,
        ):
        keyword_argument_dictionary.update(
            manager.get_keyword_argument_dictionary(expr)
            )
        if hasattr(expr, '_storage_format_specification'):
            specification = expr._storage_format_specification
            keyword_argument_names = specification._keyword_argument_names or ()
            for name in keyword_argument_names:
                keyword_argument_dictionary[name] = getattr(expr, name)
        positional_argument_dictionary.update(
            manager.get_positional_argument_dictionary(expr)
            )

    from abjad.tools import systemtools
    if expr is None:
        return expr

    manager = systemtools.StorageFormatManager

    keyword_argument_dictionary = {}
    positional_argument_dictionary = {}
    update_dictionaries(
        expr,
        keyword_argument_dictionary,
        positional_argument_dictionary,
        )

    recursive_arguments = {}
    for key, value in kwargs.items():
        if '__' in key:
            key, divider, subkey = key.partition('__')
            if key not in recursive_arguments:
                recursive_arguments[key] = []
            pair = (subkey, value)
            recursive_arguments[key].append(pair)
            continue
        if key in positional_argument_dictionary:
            positional_argument_dictionary[key] = value
        elif key in keyword_argument_dictionary:
            keyword_argument_dictionary[key] = value
        elif manager.accepts_kwargs(expr):
            keyword_argument_dictionary[key] = value
        elif isinstance(getattr(expr, key, None), types.MethodType):
            method = getattr(expr, key)
            result = method(value)
            if isinstance(result, type(expr)):
                expr = result
                update_dictionaries(
                    expr,
                    keyword_argument_dictionary,
                    positional_argument_dictionary,
                    )
        else:
            message = '{} has no key {!r}'.format(type(expr), key)
            raise KeyError(message)

    for key, pairs in recursive_arguments.items():
        recursed_object = getattr(expr, key)
        if recursed_object is None:
            continue
        recursive_keyword_argument_dictionary = dict(pairs)
        recursed_object = new(
            recursed_object,
            **recursive_keyword_argument_dictionary
            )
        if key in positional_argument_dictionary:
            positional_argument_dictionary[key] = recursed_object
        elif key in keyword_argument_dictionary:
            keyword_argument_dictionary[key] = recursed_object

    positional_argument_values = []
    positional_argument_names = getattr(
        expr, '_positional_argument_names', None) or \
        manager.get_positional_argument_names(expr)
    for positional_argument_name in positional_argument_names:
        positional_argument_value = positional_argument_dictionary[
            positional_argument_name]
        positional_argument_values.append(positional_argument_value)

    result = type(expr)(
        *positional_argument_values,
        **keyword_argument_dictionary
        )

    return result
