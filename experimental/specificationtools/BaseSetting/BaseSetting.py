from abjad.tools.abctools.AbjadObject import AbjadObject


class BaseSetting(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class for ``Setting`` and ``Directive``.

    Stopgap solution.

    Eventually ``Setting`` will inherit from ``Directive`` or vice versa.

    The purpose of the stopgap is to provide a shared namespace for inherited functionality.
    '''

    pass
