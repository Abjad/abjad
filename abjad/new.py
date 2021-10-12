import types

from . import format as _format


def new(argument, *arguments, **keywords):
    r"""
    Makes new ``argument`` with positional ``arguments`` and ``keywords``.

    ..  container:: example

        Makes markup with new direction:

        >>> markup = abjad.Markup(r'\markup \italic "Andante assai"', direction=abjad.Up)
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                ^ \markup \italic "Andante assai"
                d'4
                e'4
                f'4
            }

        >>> markup = abjad.new(markup, direction=abjad.Down)
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                _ \markup \italic "Andante assai"
                d'4
                e'4
                f'4
            }


    ..  container:: example

        REGRESSION. Can be used to set existing properties to none:

        >>> markup = abjad.Markup(r'\markup \italic "Andante assai"', direction=abjad.Up)
        >>> string = abjad.lilypond(markup)
        >>> print(string)
        ^ \markup \italic "Andante assai"

        >>> markup = abjad.new(markup, direction=None)
        >>> string = abjad.lilypond(markup)
        >>> print(string)
        \markup \italic "Andante assai"

    Returns new object with type equal to that of ``argument``.
    """
    if argument is None:
        return argument
    result = _format._inspect_signature(argument)
    signature_positional_names = result[0]
    signature_accepts_keywords = result[3]
    template_dict = _format.get_template_dict(argument)
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
                template_dict_ = _format.get_template_dict(argument)
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
    # _positional_arguments_name used, for example, in rhythm-makers
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
