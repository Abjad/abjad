from abjad.tools import documentationtools
from experimental.developerscripttools.DeveloperScript import DeveloperScript
import argparse
import importlib
import os


class CountLinesScript(DeveloperScript):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def alias(self):
        return 'lines'

    @property
    def long_description(self):
        return None

    @property
    def scripting_group(self):
        return 'count'

    @property
    def short_description(self):
        return 'Collect linecount statistics on all modules in PATH.'

    @property
    def version(self):
        return 1.0 

