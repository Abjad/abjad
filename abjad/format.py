import inspect
import types

INDENT = 4 * " "


def _get(argument, name):
    value = None
    try:
        value = getattr(argument, name, None)
        if value is None:
            value = getattr(argument, "_" + name, None)
        if value is None:
            value = getattr(argument, "_" + name.rstrip("_"), None)
    except AttributeError:
        try:
            value = argument[name]
        except (TypeError, KeyError):
            value = None
    return value


def _inspect_signature(subject):
    positional_names = []
    keyword_names = []
    accepts_args = False
    accepts_keywords = False
    if not isinstance(subject, type):
        subject = type(subject)
    try:
        signature = inspect.signature(subject)
    except ValueError:
        return (
            positional_names,
            keyword_names,
            accepts_args,
            accepts_keywords,
        )
    for name, parameter in signature.parameters.items():
        if parameter.kind == inspect._POSITIONAL_OR_KEYWORD:
            if parameter.default == parameter.empty:
                positional_names.append(name)
            else:
                keyword_names.append(name)
        elif (
            hasattr(inspect, "_KEYWORD_ONLY")
            and parameter.kind == inspect._KEYWORD_ONLY
        ):
            keyword_names.append(name)
        elif parameter.kind == inspect._VAR_POSITIONAL:
            accepts_args = True
        elif parameter.kind == inspect._VAR_KEYWORD:
            accepts_keywords = True
    return (positional_names, keyword_names, accepts_args, accepts_keywords)


def _get_template_dict(argument):
    template_names = None
    keyword_names = ()
    if template_names is None:
        result = _inspect_signature(argument)
        signature_positional_names = result[0]
        signature_keyword_names = result[1]
        template_names = list(signature_positional_names)
        template_names.extend(signature_keyword_names)
        template_names.extend(keyword_names)
        template_names = sorted(set(template_names))
    template_dict = dict()
    for name in template_names:
        template_dict[name] = _get(argument, name)
    return template_dict


def new(argument, *arguments, **keywords):
    """
    Makes new ``argument`` with positional ``arguments`` and ``keywords``.

    Returns new object with type equal to that of ``argument``.
    """
    if argument is None:
        return argument
    result = _inspect_signature(argument)
    signature_positional_names = result[0]
    signature_accepts_keywords = result[3]
    template_dict = _get_template_dict(argument)
    if not (template_dict):
        message = "low-level class not equipped for new():\n"
        message += f"   {repr(argument)}"
        raise Exception(message)
    recursive_arguments = {}
    for key, value in keywords.items():
        if "__" in key:
            key, divider, subkey = key.partition("__")
            if key not in recursive_arguments:
                recursive_arguments[key] = []
            pair = (subkey, value)
            recursive_arguments[key].append(pair)
            continue
        if key in template_dict or signature_accepts_keywords:
            template_dict[key] = value
        elif isinstance(getattr(argument, key, None), types.MethodType):
            method = getattr(argument, key)
            result = method(value)
            if isinstance(result, type(argument)):
                argument = result
                template_dict_ = _get_template_dict(argument)
                template_dict.update(template_dict_)
        else:
            raise KeyError(f"{type(argument)} has no key {key!r}.")
    for key, pairs in recursive_arguments.items():
        recursed_object = getattr(argument, key)
        if recursed_object is None:
            continue
        recursive_template_dict = dict(pairs)
        recursed_object = new(recursed_object, **recursive_template_dict)
        if key in template_dict:
            template_dict[key] = recursed_object
    positional_values = []
    for name in signature_positional_names:
        if name in template_dict:
            positional_values.append(template_dict.pop(name))
    positional_name = getattr(argument, "_positional_arguments_name", None)
    if positional_name is not None:
        assert isinstance(positional_name, str), repr(positional_name)
        positional_values_ = getattr(argument, positional_name)
        positional_values.extend(positional_values_)
    if arguments == (None,):
        positional_values = []
    elif arguments != ():
        positional_values = list(arguments)
    result = type(argument)(*positional_values, **template_dict)
    for name in getattr(argument, "_private_attributes_to_copy", []):
        value = getattr(argument, name, None)
        setattr(result, name, value)
    return result
