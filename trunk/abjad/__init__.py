import platform

_python_version = platform.python_version()
if not _python_version.startswith('2.7'):
    print 'WARNING: Abjad no longer supports versions of Python less than 2.7!'
    print 'WARNING: Please upgrade your version of Python to 2.7!'

from abjad.tools.importtools._import_functions_in_package_to_namespace import _import_functions_in_package_to_namespace
from abjad.tools import *
from abjad.tools.chordtools import Chord
from abjad.tools.containertools import Container
from abjad.tools.durationtools import Duration
from abjad.tools.iotools import f
from abjad.tools.iotools import p
from abjad.tools.iotools import play
from abjad.tools.iotools import show
from abjad.tools.iotools import z
from abjad.tools.measuretools import Measure
from abjad.tools.notetools import Note
from abjad.tools.resttools import Rest
from abjad.tools.scoretools import Score
from abjad.tools.stafftools import Staff
from abjad.tools.tuplettools import Tuplet
from abjad.tools.voicetools import Voice
from fractions import Fraction
import os
import sys

# import Abjad exceptions in __builtins__ namespace
_exceptions_path = os.path.join(__path__[0], 'tools', 'exceptiontools')
_import_functions_in_package_to_namespace(_exceptions_path, __builtins__)

# load constants into __builtins__ namespace
__builtins__['Left'] = datastructuretools.OrdinalConstant('x', -1, 'Left')
__builtins__['Right'] = datastructuretools.OrdinalConstant('x', 1, 'Right')
__builtins__['Center'] = datastructuretools.OrdinalConstant('y', 0, 'Center')
__builtins__['Up'] = datastructuretools.OrdinalConstant('y', 1, 'Up')
__builtins__['Down'] = datastructuretools.OrdinalConstant('y', -1, 'Down')

del abctools
del cfg
del configurationtools
del datastructuretools
del decoratortools
del documentationtools
del exceptiontools
del importtools
del lilypondparsertools
del lilypondproxytools
del os
del platform
del sys
del tools
del wellformednesstools

__version__ = '2.9'
