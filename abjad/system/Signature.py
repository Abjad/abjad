from abjad.system.AbjadValueObject import AbjadValueObject


class Signature(AbjadValueObject):
    """
    Signature.

    Decorates expression-enabled methods.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_argument_list_callback',
        '_is_operator',
        '_markup_maker_callback',
        '_method_name',
        '_method_name_callback',
        '_string_template_callback',
        '_subscript',
        '_superscript',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        argument_list_callback=None,
        is_operator=None,
        markup_maker_callback=None,
        method_name=None,
        method_name_callback=None,
        string_template_callback=None,
        subscript=None,
        superscript=None,
        ):
        self._argument_list_callback = argument_list_callback
        self._is_operator = is_operator
        self._markup_maker_callback = markup_maker_callback
        self._method_name = method_name
        self._method_name_callback = method_name_callback
        self._string_template_callback = string_template_callback
        self._subscript = subscript
        self._superscript = superscript

    ### SPECIAL METHODS ###

    def __call__(self, method):
        """
        Calls signature decorator on ``method``.

        Returns ``method`` with metadata attached.
        """
        method.argument_list_callback = self.argument_list_callback
        method.is_operator = self.is_operator
        method.markup_maker_callback = self.markup_maker_callback
        method.method_name = self.method_name
        method.method_name_callback = self.method_name_callback
        method.string_template_callback = self.string_template_callback
        method.subscript = self.subscript
        method.superscript = self.superscript
        method.has_signature_decorator = True
        return method

    ### PUBLIC PROPERTIES ###

    @property
    def argument_list_callback(self):
        """
        Gets argument list callback.

        Returns string or none.
        """
        return self._argument_list_callback

    @property
    def is_operator(self):
        """
        Is true when method typesets like operator.

        Returns true, false or none.
        """
        return self._is_operator

    @property
    def markup_maker_callback(self):
        """
        Gets markup maker callback.

        Returns string or none.
        """
        return self._markup_maker_callback

    @property
    def method_name(self):
        """
        Gets method name.

        Returns string or none.
        """
        return self._method_name

    @property
    def method_name_callback(self):
        """
        Gets method name callback.

        Returns string or none.
        """
        return self._method_name_callback

    @property
    def string_template_callback(self):
        """
        Gets string template callback.

        Returns string or none.
        """
        return self._string_template_callback

    @property
    def subscript(self):
        """
        Gets subscript.

        Returns string or none.
        """
        return self._subscript

    @property
    def superscript(self):
        """
        Gets superscript.

        Returns string or none.
        """
        return self._superscript
