from abjad.system.AbjadValueObject import AbjadValueObject


class FormatSpecification(AbjadValueObject):
    """
    Format specification.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Storage formatting'

    __slots__ = (
        '_client',
        '_coerce_for_equality',
        '_repr_args_values',
        '_repr_is_bracketed',
        '_repr_is_indented',
        '_repr_kwargs_names',
        '_repr_text',
        '_storage_format_args_values',
        '_storage_format_forced_override',
        '_storage_format_is_bracketed',
        '_storage_format_is_indented',
        '_storage_format_kwargs_names',
        '_storage_format_text',
        '_template_names',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        coerce_for_equality=None,
        repr_args_values=None,
        repr_is_bracketed=None,
        repr_is_indented=None,
        repr_kwargs_names=None,
        repr_text=None,
        storage_format_args_values=None,
        storage_format_forced_override=None,
        storage_format_is_bracketed=None,
        storage_format_is_indented=True,
        storage_format_kwargs_names=None,
        storage_format_text=None,
        template_names=None,
        ):
        self._client = client
        self._coerce_for_equality = self._coerce_boolean(coerce_for_equality)
        self._repr_args_values = self._coerce_tuple(repr_args_values)
        self._repr_is_bracketed = self._coerce_boolean(repr_is_bracketed)
        self._repr_is_indented = self._coerce_boolean(repr_is_indented)
        self._repr_kwargs_names = self._coerce_tuple(repr_kwargs_names)
        self._repr_text = self._coerce_string(repr_text)
        self._storage_format_args_values = self._coerce_tuple(
            storage_format_args_values)
        self._storage_format_forced_override = storage_format_forced_override
        self._storage_format_is_bracketed = self._coerce_boolean(
            storage_format_is_bracketed)
        self._storage_format_is_indented = self._coerce_boolean(
            storage_format_is_indented)
        self._storage_format_kwargs_names = self._coerce_tuple(
            storage_format_kwargs_names)
        self._storage_format_text = self._coerce_string(storage_format_text)
        self._template_names = self._coerce_tuple(template_names)

    ### PRIVATE METHODS ###

    def _coerce_boolean(self, value):
        if value is not None:
            return bool(value)

    def _coerce_string(self, value):
        if value is not None:
            return str(value)

    def _coerce_tuple(self, value):
        if value is not None:
            return tuple(value)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def coerce_for_equality(self):
        return self._coerce_for_equality

    @property
    def repr_args_values(self):
        return self._repr_args_values

    @property
    def repr_is_bracketed(self):
        return self._repr_is_bracketed

    @property
    def repr_is_indented(self):
        return self._repr_is_indented

    @property
    def repr_kwargs_names(self):
        return self._repr_kwargs_names

    @property
    def repr_text(self):
        return self._repr_text

    @property
    def storage_format_args_values(self):
        return self._storage_format_args_values

    @property
    def storage_format_forced_override(self):
        return self._storage_format_forced_override

    @property
    def storage_format_is_bracketed(self):
        return self._storage_format_is_bracketed

    @property
    def storage_format_is_indented(self):
        return self._storage_format_is_indented

    @property
    def storage_format_kwargs_names(self):
        return self._storage_format_kwargs_names

    @property
    def storage_format_text(self):
        return self._storage_format_text

    @property
    def template_names(self):
        return self._template_names
