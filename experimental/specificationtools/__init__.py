from AttributeNameEnumeration import AttributeNameEnumeration
from AttributeRetrievalIndicator import AttributeRetrievalIndicator
from AttributeRetrievalRequest import AttributeRetrievalRequest
from BaseSetting import BaseSetting
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
from OrdinalConstant import OrdinalConstant
from VoiceDivisionList import VoiceDivisionList

_documentation_section = 'unstable'

__builtins__['Left'] = OrdinalConstant('x', -1, 'Left')
__builtins__['Right'] = OrdinalConstant('x', 1, 'Right')
__builtins__['Center'] = OrdinalConstant('x', 0, 'Left')
__builtins__['Up'] = OrdinalConstant('y', 1, 'Up')
__builtins__['Down'] = OrdinalConstant('y', -1, 'Down')
