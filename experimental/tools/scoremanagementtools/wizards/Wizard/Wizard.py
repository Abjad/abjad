import abc
from experimental.tools.scoremanagementtools.core.ScoreManagementObject import ScoreManagementObject


# TODO: extend repr to show target, if any
class Wizard(ScoreManagementObject):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    target_editor_class_name_suffix = 'Editor'

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        ScoreManagementObject.__init__(self, session=session)
        self.target = target

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def breadcrumb(self):
        pass

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def run(self, cache=False, clear=True, head=None, user_input=None):
        pass
