# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.abctools import AbjadObject


class Job(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, number):
        self.number = number

    ### SPECIAL METHODS ###

    def __call__(self):
        self.result = [x for x in mathtools.yield_all_compositions_of_integer(self.number)]


@pytest.mark.skip()
def test_quantizationtools_ParallelJobHandler___call___01():

    jobs = [Job(x) for x in range(1, 11)]
    job_handler = quantizationtools.ParallelJobHandler()
    finished_jobs = job_handler(jobs)


@pytest.mark.skip()
def test_quantizationtools_ParallelJobHandler___call___02():

    job_id = 1
    definition = {
        2: {
            2: {
                2: None
                },
            3: None
            },
        5: None
        }
    search_tree = quantizationtools.UnweightedSearchTree(definition)
    q_event_proxies = [
        quantizationtools.QEventProxy(
            quantizationtools.SilentQEvent(0, ['A'], index=1), 0, 1),
        quantizationtools.QEventProxy(
            quantizationtools.SilentQEvent((1, 5), ['B'], index=2), 0, 1),
        quantizationtools.QEventProxy(
            quantizationtools.SilentQEvent((1, 4), ['C'], index=3), 0, 1),
        quantizationtools.QEventProxy(
            quantizationtools.SilentQEvent((1, 3), ['D'], index=4), 0, 1),
        quantizationtools.QEventProxy(
            quantizationtools.SilentQEvent((2, 5), ['E'], index=5), 0, 1),
        quantizationtools.QEventProxy(
            quantizationtools.SilentQEvent((1, 2), ['F'], index=6), 0, 1),
        quantizationtools.QEventProxy(
            quantizationtools.SilentQEvent((3, 5), ['G'], index=7), 0, 1),
        quantizationtools.QEventProxy(
            quantizationtools.SilentQEvent((2, 3), ['H'], index=8), 0, 1),
        quantizationtools.QEventProxy(
            quantizationtools.SilentQEvent((3, 4), ['I'], index=9), 0, 1),
        quantizationtools.QEventProxy(
            quantizationtools.SilentQEvent((4, 5), ['J'], index=10), 0, 1),
        quantizationtools.QEventProxy(
            quantizationtools.SilentQEvent(1, ['K'], index=11), 0, 1)
        ]
    job_a = quantizationtools.QuantizationJob(
        job_id, search_tree, q_event_proxies)
    job_b = quantizationtools.QuantizationJob(
        job_id, search_tree, q_event_proxies)

    assert job_a == job_b

    a_jobs = quantizationtools.SerialJobHandler()([job_a])
    b_jobs = quantizationtools.ParallelJobHandler()([job_b])

    assert len(a_jobs) == len(b_jobs)

    a_rtms = sorted([
        q_grid.root_node.rtm_format
        for q_grid in a_jobs[0].q_grids
        ])
    b_rtms = sorted([
        q_grid.root_node.rtm_format
        for q_grid in b_jobs[0].q_grids
        ])

    assert a_rtms == b_rtms

    assert sorted(a_jobs[0].q_grids, key=lambda x: x.root_node.rtm_format) == \
        sorted(b_jobs[0].q_grids, key=lambda x: x.root_node.rtm_format)
