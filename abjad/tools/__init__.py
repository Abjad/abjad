# -*- encoding: utf-8 -*-

from abjad.tools import systemtools
from abjad.tools import datastructuretools
from abjad.tools import mathtools

# load constants into __builtins__ namespace
__builtins__['Left'] = datastructuretools.OrdinalConstant('x', -1, 'Left')
__builtins__['Right'] = datastructuretools.OrdinalConstant('x', 1, 'Right')
__builtins__['Center'] = datastructuretools.OrdinalConstant('y', 0, 'Center')
__builtins__['Up'] = datastructuretools.OrdinalConstant('y', 1, 'Up')
__builtins__['Down'] = datastructuretools.OrdinalConstant('y', -1, 'Down')
__builtins__['Infinity'] = mathtools.Infinity()
__builtins__['NegativeInfinity'] = mathtools.NegativeInfinity()

systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    delete_systemtools=False,
    )
