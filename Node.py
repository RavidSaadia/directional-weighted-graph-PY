import random as rnd


class Node:
    _id = 0

    def __init__(self, inside: dict, outside: dict, info: str, tag: float, pos: tuple):
        self._id += 1
        self._inside = inside
        self._outside = outside
        self._info = info
        self._tag = tag
        self._pos = pos

    def set_pos(self, pos: tuple = (rnd.random(), rnd.random(), rnd.random())):
        self._pos = pos

    def set_tag(self, tag: float):
        self._tag = tag

    def set_info(self, info: str):
        self._info = info

    def get_inside(self) -> dict:
        return self._inside

    def get_outside(self) -> dict:
        return self._outside

    def get_id(self) -> int:
        return self._id

    def get_tag(self) -> float:
        return self._tag

    def get_pos(self):
        return self._pos

    def get_info(self):
        return self._info
