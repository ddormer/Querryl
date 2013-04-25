import json

from twisted.python.failure import Failure
from twisted.trial.unittest import TestCase

from querryl.utils import FailureEncoder


class FailureEncoderTests(TestCase):
    """
    Tests for L{querryl.utils.FailureEncoder}.
    """
    def test_failureToJSON(self):
        """
        L{json.dumps} can handle a L{Failure} when using the L{FailureEncoder}.
        """
        result = json.dumps(
            Failure(Exception('an exception')), cls=FailureEncoder)
        self.assertEquals('{"error": "an exception"}', result)
