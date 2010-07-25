from abjad.tools.importtools.package_import import _package_import

_package_import(__path__[0], globals( ))

from _generator import _generator
