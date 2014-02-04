# -*- encoding: utf-8 -*-


def new(expr, **kwargs):
    r'''Makes new `expr` with optionally new ``kwargs``.

    Returns new object with the same type as `expr`.
    '''
    from abjad.tools import systemtools
    manager = systemtools.StorageFormatManager
    keyword_argument_dictionary = \
        manager.get_keyword_argument_dictionary(expr)
    positional_argument_dictionary = \
        manager.get_positional_argument_dictionary(expr)
    recursive_arguments = {}
    for key, value in kwargs.iteritems():
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
        else:
            raise KeyError(key)
    for key, pairs in recursive_arguments.iteritems():
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
        *positional_argument_values, **keyword_argument_dictionary)
    return result
