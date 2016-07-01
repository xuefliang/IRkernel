import unittest
import test_ir

def get_test_ids(suite):
    for t_or_s in suite:
        if isinstance(t_or_s, unittest.TestSuite):
            yield from get_test_ids(t_or_s)
        else:
            yield t_or_s.id()

module_suite = unittest.defaultTestLoader.loadTestsFromModule(test_ir)
test_ids = list(get_test_ids(module_suite))

# this has to be this compex since an individual TestCase does not call setUpClass
# and suites do not expose the id/shortDescription of their child tests
suites = [unittest.defaultTestLoader.loadTestsFromName(id) for id in test_ids]
tests_per_suite = [list(suite) for suite in suites]
assert all(len(tests) == 1 for tests in tests_per_suite)
test_descs = [tests[0].shortDescription() or tests[0].id() for tests in tests_per_suite]
test_dict = dict(zip(test_descs, suites))

def get_msgs(results):
    return [msg for test, msg in results]

def run_test(desc):
    result = unittest.TestResult()
    test_dict[desc].run(result)
    return {
        'failures': get_msgs(result.errors) + get_msgs(result.failures) + get_msgs(result.unexpectedSuccesses),
        'skipped': get_msgs(result.skipped),
        'expected_failures': get_msgs(result.expectedFailures),
        'success': result.wasSuccessful()
    }
