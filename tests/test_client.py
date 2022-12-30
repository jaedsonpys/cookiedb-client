import sys

import bupytest

sys.path.insert(0, './')


class TestClient(bupytest.UnitTest):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    bupytest.this()
