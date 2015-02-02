"""
Mock code that generates random student grades.
"""
import random
from . import GradeSource


class MockGradeSource(GradeSource):
    """
    Source of random student grades
    """
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    NAMES = ("Jamie", "Alex", "Sam", "Jordan", "Taylor")

    def is_supported(self):
        """
        Does self.host_block.runtime support this type of grade source?

        We return True in the XBlock workbench or an XBlock test environment.
        """
        try:
            from workbench.runtime import WorkbenchRuntime
            if isinstance(self.host_block.runtime, WorkbenchRuntime):
                return True
        except ImportError:
            pass
        from xblock.test.tools import TestRuntime
        return isinstance(self.host_block.runtime, TestRuntime)

    def get_grades(self, target_block_id, limit_hint=None):
        """
        Generate random grades for target_block_id and descendants.

        Results should be consistent for use in tests etc.
        """
        # Even though this is just a mock source, verify target_block_id and that the runtime can load blocks for us:
        self.host_block.runtime.get_block(target_block_id)
        # Seed a random generator consistent based on target_block_id:
        rand = random.Random(target_block_id)

        if limit_hint is None:
            limit_hint = rand.randint(5, 80)

        random_name = lambda: u"{first} {initial}.".format(
            first=rand.choice(self.NAMES),
            initial=rand.choice(self.ALPHABET)
        )
        random_grade = lambda: rand.randint(0, 100)

        return [(random_grade(), {"name": random_name()}) for _ in xrange(0, limit_hint)]
