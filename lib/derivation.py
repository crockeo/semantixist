from lib.composition import Composer

class Node:
    def __init__(self, value=None, type=None, left_node=None, right_node=None):
        self._value = value
        self._type = type
        self._left_node = left_node
        self._right_node = right_node

    def __str__(self):
        return str(self.get_value())

    def __repr__(self):
        return str(self)

    def _derive(self):
        """
        Derives self._value and self._type from self._left_node and self._right_node.
        """
        self._value, self._type = Composer().compose(self._left_node, self._right_node)

    def get_value(self):
        if self._value is None:
            self._derive()
        return self._value

    def get_type(self):
        if self._type is None:
            self._derive()
        return self._type
