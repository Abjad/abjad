# -*- coding: utf-8 -*-
import types


def new(expr, **kwargs):
    r'''Makes new `expr` with optional new `kwargs`.

    Returns new object with the same type as `expr`.
    '''
    from abjad.tools import systemtools
    if expr is None:
        return expr
    agent = systemtools.StorageFormatAgent(expr)
    template_dict = agent.get_template_dict()
    recursive_arguments = {}
    for key, value in kwargs.items():
        if '__' in key:
            key, divider, subkey = key.partition('__')
            if key not in recursive_arguments:
                recursive_arguments[key] = []
            pair = (subkey, value)
            recursive_arguments[key].append(pair)
            continue
        if key in template_dict or agent.signature_accepts_kwargs:
            template_dict[key] = value
        elif isinstance(getattr(expr, key, None), types.MethodType):
            method = getattr(expr, key)
            result = method(value)
            if isinstance(result, type(expr)):
                expr = result
                template_dict.update(systemtools.StorageFormatAgent(
                    expr).get_template_dict())
        else:
            message = '{} has no key {!r}'.format(type(expr), key)
            raise KeyError(message)
    for key, pairs in recursive_arguments.items():
        recursed_object = getattr(expr, key)
        if recursed_object is None:
            continue
        recursive_template_dict = dict(pairs)
        recursed_object = new(recursed_object, **recursive_template_dict)
        if key in template_dict:
            template_dict[key] = recursed_object
    positional_values = []
    for name in agent.signature_positional_names:
        if name in template_dict:
            positional_values.append(template_dict.pop(name))
    result = type(expr)(*positional_values, **template_dict)
    return result
