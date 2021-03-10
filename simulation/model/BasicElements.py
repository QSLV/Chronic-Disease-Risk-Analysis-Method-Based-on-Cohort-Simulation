from typing import List, Dict, Tuple
import numpy as np
import pandas as pd
import random


class Node(object):
    name: str

    def __init__(self, name):
        self.name = name


class Link(object):
    source: int
    target: int

    def __init__(self, source, target):
        self.source = source
        self.target = target


class NextState(object):
    cut: int
    next_idx: int

    def __init__(self, cut, next_idx):
        self.cut = cut
        self.next_idx = next_idx


class Person(object):
    # id
    idx: int
    # 当前state
    state: int
    # 状态历史
    state_history: List[int]
    # 状态历史对应年龄
    state_age_history: List[int]

    def __init__(self, idx: int, init_state: int, init_age: int):
        self.idx = idx
        self.state = init_state
        self.state_history = [init_state]
        self.state_age_history = [init_age]

    def __str__(self):
        return "id:%d state:%d age: state_history:" % (self.idx, self.state)

    def __repr__(self):
        return "Person(id:%d state:%d state_history:%s, state_age_history:%s)" % \
               (self.idx, self.state, self.state_history, self.state_age_history)
