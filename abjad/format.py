import dataclasses
import importlib
import inspect
import numbers
import types
import typing

import quicktions
import uqbar

INDENT = 4 * " "


@dataclasses.dataclass(slots=True)
class FormatSpecification:
    """
    Format specification.
    """

    coerce_for_equality: bool = False
    repr_args_values: typing.Optional[tuple] = None
    repr_is_bracketed: bool = False
    repr_is_indented: bool = False
    repr_keyword_names: typing.Optional[tuple] = None
    repr_text: typing.Optional[str] = None
    storage_format_args_values: typing.Optional[tuple] = None
    storage_format_forced_override: typing.Optional[str] = None
    storage_format_is_bracketed: bool = False
    storage_format_is_not_indented: bool = False
    storage_format_keyword_names: typing.Optional[tuple] = None
    storage_format_text: typing.Optional[str] = None
    template_names: typing.Optional[tuple] = None


def _dispatch_formatting(argument, as_storage_format=True, is_indented=True):
    if isinstance(argument, types.MethodType):
        return []
    elif isinstance(argument, type):
        return _format_class(argument, as_storage_format, is_indented)
    elif as_storage_format and hasattr(argument, "_get_format_specification"):
        pieces = _format_specced_object(argument, as_storage_format=as_storage_format)
        return list(pieces)
    elif not as_storage_format and hasattr(argument, "_get_format_specification"):
        pieces = _format_specced_object(argument, as_storage_format=as_storage_format)
        return list(pieces)
    elif isinstance(argument, (list, tuple)):
        return _format_sequence(argument, as_storage_format, is_indented)
    elif hasattr(argument, "_collection") and isinstance(argument._collection, dict):
        return _format_ordered_mapping(argument, as_storage_format, is_indented)
    elif isinstance(argument, dict):
        return _format_mapping(argument, as_storage_format, is_indented)
    elif isinstance(argument, float):
        return repr(round(argument, 15)).split("\n")
    return repr(argument).split("\n")


def _format_class(argument, as_storage_format, is_indented):
    if as_storage_format:
        root_package_name = _get_module_path_parts(argument)[0]
        root_package = importlib.import_module(root_package_name)
        parts = [root_package_name]
        if argument.__name__ not in dir(root_package):
            tools_package_name = _get_tools_package_name(argument)
            parts.append(tools_package_name)
        parts.append(argument.__name__)
        result = ".".join(parts)
    else:
        result = argument.__name__
    return [result]


def _format_mapping(argument, as_storage_format, is_indented):
    result = []
    prefix, infix, suffix = _get_whitespace(is_indented)
    result.append("{" + infix)
    for key, value in sorted(argument.items()):
        key_pieces = _dispatch_formatting(
            key, as_storage_format=as_storage_format, is_indented=is_indented
        )
        value_pieces = _dispatch_formatting(
            value, as_storage_format=as_storage_format, is_indented=is_indented
        )
        for line in key_pieces[:-1]:
            result.append(prefix + line)
        result.append(f"{prefix}{key_pieces[-1]}: {value_pieces[0]}")
        for line in value_pieces[1:]:
            result.append(prefix + line)
        result[-1] = result[-1] + suffix
    if not is_indented:
        result[-1] = result[-1].rstrip(suffix) + infix
    result.append(prefix + "}")
    return result


def _format_ordered_mapping(argument, as_storage_format, is_indented):
    result = []
    prefix, infix, suffix = _get_whitespace(is_indented)
    result.append("[" + infix)
    for item in list(argument.items()):
        item_pieces = _dispatch_formatting(
            item, as_storage_format=as_storage_format, is_indented=is_indented
        )
        for line in item_pieces:
            result.append(prefix + line)
        result[-1] = result[-1] + suffix
    if not is_indented:
        result[-1] = result[-1].rstrip(suffix) + infix
    result.append(prefix + "]")
    return result


def _format_sequence(argument, as_storage_format, is_indented):
    result = []
    prefix, infix, suffix = _get_whitespace(is_indented)
    # just return the repr, if all contents are builtin types
    prototype = (bool, int, float, str, type(None))
    if all(isinstance(x, prototype) for x in argument):
        piece = repr(argument)
        if len(piece) < 50:
            return [repr(argument)]
    if isinstance(argument, list):
        braces = "[", "]"
    else:
        braces = "(", ")"
    result.append(braces[0] + infix)
    for x in argument:
        pieces = _dispatch_formatting(
            x, as_storage_format=as_storage_format, is_indented=is_indented
        )
        for line in pieces[:-1]:
            result.append(prefix + line)
        result.append(prefix + pieces[-1] + suffix)
    if not is_indented:
        if isinstance(argument, list) or 1 < len(argument):
            result[-1] = result[-1].rstrip(suffix)
        else:
            result[-1] = result[-1].rstrip()
    result.append(prefix + braces[1])
    return result


def _format_specced_object(argument, as_storage_format=True):
    if hasattr(argument, "_get_format_specification"):
        specification = argument._get_format_specification()
        if specification.storage_format_forced_override is not None:
            return [specification.storage_format_forced_override]
    formatting_keywords = _get_formatting_keywords(argument, as_storage_format)
    args_values = formatting_keywords["args_values"]
    as_storage_format = formatting_keywords["as_storage_format"]
    is_bracketed = formatting_keywords["is_bracketed"]
    is_indented = formatting_keywords["is_indented"]
    keyword_names = formatting_keywords["keyword_names"]
    text = formatting_keywords["text"]
    result = []
    if is_bracketed:
        result.append("<")
    if text is not None:
        result.append(text)
    else:
        prefix, infix, suffix = _get_whitespace(is_indented)
        class_name_prefix = _get_class_name_prefix(argument, as_storage_format)
        positional_argument_pieces = []
        for value in args_values:
            pieces = _dispatch_formatting(
                value,
                as_storage_format=as_storage_format,
                is_indented=is_indented,
            )
            for piece in pieces[:-1]:
                positional_argument_pieces.append(prefix + piece)
            positional_argument_pieces.append(prefix + pieces[-1] + suffix)
        keyword_argument_pieces = []
        for name in keyword_names:
            value = _get(argument, name)
            if value is None or isinstance(value, types.MethodType):
                continue
            pieces = _dispatch_formatting(
                value,
                as_storage_format=as_storage_format,
                is_indented=is_indented,
            )
            pieces[0] = f"{name}={pieces[0]}"
            for piece in pieces[:-1]:
                keyword_argument_pieces.append(prefix + piece)
            keyword_argument_pieces.append(prefix + pieces[-1] + suffix)
        if not positional_argument_pieces and not keyword_argument_pieces:
            result.append(f"{class_name_prefix}()")
        else:
            result.append(f"{class_name_prefix}({infix}")
            result.extend(positional_argument_pieces)
            if positional_argument_pieces and not keyword_argument_pieces:
                result[-1] = result[-1].rstrip(suffix) + infix
            else:
                result.extend(keyword_argument_pieces)
            if not as_storage_format:
                result[-1] = result[-1].rstrip(suffix) + infix
            if is_indented:
                result.append(f"{prefix})")
            else:
                result.append(")")
    if is_bracketed:
        result.append(">")
    if not is_indented:
        return ["".join(result)]
    return result


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


def _get_class_name_prefix(argument, as_storage_format) -> str:
    if not isinstance(argument, type):
        class_name = type(argument).__name__
    else:
        class_name = argument.__name__
    if as_storage_format:
        root_package_name = _get_module_path_parts(argument)[0]
        root_package = importlib.import_module(root_package_name)
        parts = []
        if root_package_name != "abjadext":
            parts.append(root_package_name)
        if class_name not in dir(root_package):
            name = _get_tools_package_name(argument)
            parts.append(name)
        parts.append(class_name)
        return ".".join(parts)
    return class_name


def _get_formatting_keywords(argument, as_storage_format=True):
    if hasattr(argument, "_get_format_specification"):
        specification = argument._get_format_specification()
    else:
        specification = FormatSpecification()
    via = "_get_format_specification()"
    if as_storage_format:
        args_values = specification.storage_format_args_values
        is_bracketed = specification.storage_format_is_bracketed
        is_indented = not specification.storage_format_is_not_indented
        keyword_names = specification.storage_format_keyword_names
        text = specification.storage_format_text
    else:
        args_values = specification.repr_args_values
        if args_values is None:
            args_values = specification.storage_format_args_values
        is_bracketed = specification.repr_is_bracketed
        is_indented = specification.repr_is_indented
        keyword_names = specification.repr_keyword_names
        if keyword_names is None:
            keyword_names = specification.storage_format_keyword_names
        text = specification.repr_text
        if text is None:
            text = specification.storage_format_text
    result = _inspect_signature(argument)
    signature_positional_names = result[0]
    signature_keyword_names = result[1]
    signature_accepts_args = result[2]
    if keyword_names is None:
        keyword_names = signature_keyword_names
    if args_values is None:
        args_values = tuple(_get(argument, _) for _ in signature_positional_names)
    if args_values:
        keyword_names = list(keyword_names)
        names = signature_positional_names
        if not signature_accepts_args:
            names += signature_keyword_names
        names = names[: len(args_values)]
        for name in names:
            if name in keyword_names:
                keyword_names.remove(name)
        keyword_names = tuple(keyword_names)
    return dict(
        args_values=args_values,
        as_storage_format=as_storage_format,
        is_bracketed=is_bracketed,
        is_indented=is_indented,
        keyword_names=keyword_names,
        text=text,
        via=via,
    )


def _get_module_path_parts(subject):
    if isinstance(subject, type):
        class_ = subject
    elif type(subject) is subject.__class__:
        class_ = type(subject)
    class_name = class_.__name__
    parts = class_.__module__.split(".")
    while parts and parts[-1] == class_name:
        parts.pop()
    parts.append(class_name)
    return parts


def _get_tools_package_name(argument):
    parts = _get_module_path_parts(argument)
    if parts[0] == "abjadext":
        return parts[1]
    if parts[0] == "abjad":
        for part in reversed(parts):
            if part == parts[-1]:
                continue
            return part
    return ".".join(parts[:-1])


def _get_whitespace(is_indented):
    if is_indented:
        return "    ", "\n", ",\n"
    return "", "", ", "


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
        # Python 3 allow keyword only parameters:
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


def _make_hashable(value):
    if isinstance(value, dict):
        value = tuple(value.items())
    elif isinstance(value, list):
        value = tuple(value)
    elif isinstance(value, (set, frozenset)):
        value = tuple(value)
    return value


def _to_evaluable_string(argument):
    if argument is None:
        pass
    elif isinstance(argument, str):
        argument = repr(argument)
    elif argument.__class__ is quicktions.Fraction:
        argument = f"quicktions.{argument!r}"
    elif isinstance(argument, quicktions.Fraction):
        argument = f"abjad.{argument!r}"
    elif isinstance(argument, numbers.Number):
        argument = str(argument)
    elif isinstance(argument, (list, tuple)):
        item_strings = []
        item_count = len(argument)
        for item in argument:
            item_string = _to_evaluable_string(item)
            item_strings.append(item_string)
        items = ", ".join(item_strings)
        if isinstance(argument, list):
            argument = f"[{items}]"
        elif isinstance(argument, tuple):
            if item_count == 1:
                items += ","
            argument = f"({items})"
        else:
            raise Exception(repr(argument))
    elif isinstance(argument, slice):
        argument = repr(argument)
    elif isinstance(argument, uqbar.enums.StrictEnumeration):
        argument = f"abjad.{argument!r}"
    # abjad object
    elif not inspect.isclass(argument):
        try:
            argument = storage(argument)
        except (TypeError, ValueError):
            try:
                argument = storage(argument)
            except (TypeError, ValueError):
                raise Exception(f"can not make storage format: {argument!r}.")
    # abjad class
    elif inspect.isclass(argument) and "abjad" in argument.__module__:
        argument = f"abjad.{argument.__name__}"
    # builtin class [like tuple used in classes=(tuple,)]
    elif inspect.isclass(argument) and "abjad" not in argument.__module__:
        argument = argument.__name__
    else:
        raise Exception(f"can not make evaluable string: {argument!r}.")
    return argument


def _wrap_arguments(frame):
    try:
        frame_info = inspect.getframeinfo(frame)
        function_name = frame_info.function
        argument_info = inspect.getargvalues(frame)
        # bound method
        if argument_info.args and argument_info.args[0] == "self":
            self = argument_info.locals["self"]
            function = getattr(self, function_name)
            signature = inspect.signature(function)
            argument_names = argument_info.args[1:]
        # function
        else:
            function = frame.f_globals[function_name]
            signature = inspect.signature(function)
            argument_names = argument_info.args[:]
        argument_strings = []
        for argument_name in argument_names:
            argument_value = argument_info.locals[argument_name]
            parameter = signature.parameters[argument_name]
            # positional argument
            if parameter.default == inspect.Parameter.empty:
                argument_value = _to_evaluable_string(argument_value)
                argument_string = argument_value
                argument_strings.append(argument_string)
            # keyword argument
            elif argument_value != parameter.default:
                argument_string = "{argument_name}={argument_value}"
                argument_value = _to_evaluable_string(argument_value)
                argument_string = argument_string.format(
                    argument_name=argument_name,
                    argument_value=argument_value,
                )
                argument_strings.append(argument_string)
        arguments = ", ".join(argument_strings)
    finally:
        del frame
    return arguments


def compare_objects(object_1, object_2) -> bool:
    """
    Compares ``object_1`` to ``object_2``.
    """
    if hasattr(object_1, "_get_format_specification"):
        specification = object_1._get_format_specification()
        coerce_for_equality = specification.coerce_for_equality
    else:
        coerce_for_equality = False

    if coerce_for_equality:
        try:
            object_2 = type(object_1)(object_2)
        except (TypeError, ValueError):
            return False
    elif not isinstance(object_2, type(object_1)):
        return False
    template_1 = get_template_dict(object_1)
    template_2 = get_template_dict(object_2)
    return template_1 == template_2


def get_hash_values(argument):
    """
    Gets hash values of ``argument``.
    """
    values = []
    if isinstance(argument, type):
        values.append(argument)
    else:
        values.append(type(argument))
    template_items = sorted(get_template_dict(argument).items())
    values.extend(_make_hashable(v) for k, v in template_items)
    return tuple(values)


def get_template_dict(argument):
    """
    Gets template dictionary of ``argument``.
    """
    if hasattr(argument, "_get_format_specification"):
        specification = argument._get_format_specification()
        template_names = specification.template_names
        keyword_names = specification.storage_format_keyword_names or ()
    else:
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


def get_repr(argument):
    """
    Gets repr format of ``argument``.
    """
    pieces = _format_specced_object(argument, as_storage_format=False)
    return "".join(pieces)


def storage(argument):
    """
    Gets storage format of ``argument``.
    """
    if isinstance(argument, dict):
        pieces = _dispatch_formatting(argument)
        pieces[-1] = pieces[-1] + "\n"
        pieces.append(")")
        pieces = ["    " + _ for _ in pieces]
        pieces.insert(0, "dict(\n")
        result = "".join(pieces)
    else:
        pieces = _format_specced_object(argument, as_storage_format=True)
        result = "".join(pieces)
    return result
