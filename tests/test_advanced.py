# -*- coding: utf-8 -*-

from __future__ import absolute_import
from .context import loony

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(loony.main())


if __name__ == '__main__':
    unittest.main()
