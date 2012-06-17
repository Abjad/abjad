from abjad.tools.abctools.AbjadObject import AbjadObject


class BaseSetting(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class for ``ContextSetting`` and ``Setting``.

    Stopgap solution.

    Eventually ``ContextSetting`` will inherit from ``Setting`` or vice versa.

    The purpose of the stopgap is to provide a shared namespace for inherited functionality.
    '''

    pass
