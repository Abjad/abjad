from abjad.tools.abctools import AbjadObject


class CodeBlock(AbjadObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_exceptions',
        '_displayed_lines',
        '_executed_lines',
        '_hide',
        '_processed_results',
        '_strip_prompt',
        )

    ### INITIALIZER ###

    def __init__(self,
        displayed_lines,
        allow_exceptions=False,
        executed_lines=None,
        hide=False,
        strip_prompt=False,
        ):
        self._allow_exception = bool(allow_exceptions)
        self._displayed_lines = tuple(displayed_lines)
        self._executed_lines = None
        if executed_lines is not None:
            self._executed_lines = tuple(executed_lines)
        self._hide = bool(hide)
        self._processed_results = []
        self._strip_prompt = bool(strip_prompt)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def allow_exceptions(self):
        return self._allow_exceptions

    @property
    def displayed_lines(self):
        return self._displayed_lines

    @property
    def executed_lines(self):
        return self._executed_lines

    @property
    def hide(self):
        return self._hide

    @property
    def processed_results(self):
        return self._processed_results

    @property
    def strip_prompt(self):
        return self._strip_prompt


