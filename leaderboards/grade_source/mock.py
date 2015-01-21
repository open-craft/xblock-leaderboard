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
        """
        return True

    def get_grades(self, target_block_id, limit_hint=None):
        """
        Generate random grades for target_block_id and descendants.

        Results should be consistent for use in tests etc.
        """
        # Seed a random generator consistent based on target_block_id:
        seed = 42
        for letter in unicode(target_block_id):
            seed += ord(letter)
        rand = random.Random(seed)

        if limit_hint is None:
            limit_hint = rand.randint(5, 80)

        return [
            (
                rand.randint(0, 100),
                {"name": u"{first} {initial}.".format(first=rand.choice(self.NAMES), initial=rand.choice(self.ALPHABET))}
            )
            for _ in xrange(0, limit_hint)
        ]
