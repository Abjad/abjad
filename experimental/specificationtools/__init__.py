from AttributeNameEnumeration import AttributeNameEnumeration
from AttributeRetrievalIndicator import AttributeRetrievalIndicator
from AttributeRetrievalRequest import AttributeRetrievalRequest
from Callback import Callback
from ContextDictionary import ContextDictionary
from ContextProxy import ContextProxy
from ContextSelection import ContextSelection
from Directive import Directive
from DirectiveInventory import DirectiveInventory
from Division import Division
from DivisionList import DivisionList
from DivisionRetrievalRequest import DivisionRetrievalRequest
from HandlerRequest import HandlerRequest
from PartIndicator import PartIndicator
from RegionDivisionList import RegionDivisionList
from ResolvedSetting import ResolvedSetting
from ScopedValue import ScopedValue
from ScoreObjectIndicator import ScoreObjectIndicator
from ScoreSpecification import ScoreSpecification
from SegmentDivisionList import SegmentDivisionList
from SegmentInventory import SegmentInventory
from SegmentSpecification import SegmentSpecification
from Selection import Selection
from Setting import Setting
from SettingInventory import SettingInventory
from Specification import Specification
from StatalServer import StatalServer
from StatalServerRequest import StatalServerRequest
from TemporalCursor import TemporalCursor
from TemporalScope import TemporalScope
from ValueRetrievalIndicator import ValueRetrievalIndicator
from ValueRetrievalRequest import ValueRetrievalRequest
from VectorConstant import VectorConstant
from VoiceDivisionList import VoiceDivisionList

_documentation_section = 'unstable'

__builtins__['left'] = VectorConstant('x', -1, 'left')
__builtins__['right'] = VectorConstant('x', 1, 'right')
__builtins__['up'] = VectorConstant('y', 1, 'up')
__builtins__['down'] = VectorConstant('y', -1, 'down')
