from experimental.tools.handlertools import *
__all__ = []


hairpins = NoteAndChordHairpinHandler(('p', '<', 'f'))
__all__.append('hairpins')

mantenimenti = RestTerminatedMantenimentiHandler()
__all__.append('mantenimenti')

swells = TwoStageHairpinHandler(('p', '<', 'f', '>', 'p'))
__all__.append('swells')
