import abc
from experimental.tools.scoremanagementtools.core.SCFObject import SCFObject


# TODO: extend repr to show target, if any
class Wizard(SCFObject):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    target_editor_class_name_suffix = 'Editor'

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        SCFObject.__init__(self, session=session)
        self.target = target

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def breadcrumb(self):
        pass

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def run(self, cache=False, clear=True, head=None, user_input=None):
        pass
