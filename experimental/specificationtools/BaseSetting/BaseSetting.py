from abjad.tools.abctools.AbjadObject import AbjadObject


class BaseSetting(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class for ``ContextSetting`` and ``Directive``.

    Stopgap solution.

    Eventually ``ContextSetting`` will inherit from ``Directive`` or vice versa.

    The purpose of the stopgap is to provide a shared namespace for inherited functionality.
    '''

    pass
