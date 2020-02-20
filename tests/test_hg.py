from unittest import TestCase

from hg import GarbageCollector


class GarbageCollectorTestCase(TestCase):

    def setUp(self) -> None:
        self.collector = GarbageCollector(
            repo=None
        )

    def test_constructor(self):
        """Test Garbage Collector construction."""
        self.assertIsInstance(self.collector, GarbageCollector)
