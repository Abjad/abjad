# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_QuantizationJob___call___01():

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
    job = quantizationtools.QuantizationJob(
        job_id, search_tree, q_event_proxies)
    job()

    assert len(job.q_grids) == 10

    rtm_formats = [q_grid.root_node.rtm_format for q_grid in job.q_grids]
    rtm_formats.sort(reverse=True)

    assert rtm_formats == [
        '1',
        '(1 (1 1))',
        '(1 (1 1 1 1 1))',
        '(1 ((1 (1 1)) (1 (1 1))))',
        '(1 ((1 (1 1)) (1 (1 1 1))))',
        '(1 ((1 (1 1 1)) (1 (1 1))))',
        '(1 ((1 (1 1 1)) (1 (1 1 1))))',
        '(1 ((1 (1 1 1)) (1 ((1 (1 1)) (1 (1 1))))))',
        '(1 ((1 ((1 (1 1)) (1 (1 1)))) (1 (1 1 1))))',
        '(1 ((1 ((1 (1 1)) (1 (1 1)))) (1 ((1 (1 1)) (1 (1 1))))))'
        ], rtm_formats
