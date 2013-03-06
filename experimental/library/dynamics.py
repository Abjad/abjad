from experimental.tools.handlertools.dynamics import *
__all__ = []


hairpins = NoteAndChordHairpinHandler(('p', '<', 'f'))
__all__.append('hairpins')

mantenimenti = RestTerminatedMantenimentiHandler()
__all__.append('mantenimenti')

swells = NoteAndChordSwellHandler(('p', '<', 'f', '>', 'p'))
__all__.append('swells')
