import re


def sort_dictionary_sortable_values(dictionary):
    """
    Sort lists which are values of a dictionary. May be used for better dict comparisons.

    Args:
        dictionary (dict):
            Dictionary whose values should be sorted.
    """
    for v in dictionary.values():
        if isinstance(v, list):
            v.sort()


def compare_logs(caplog, expected_logs):
    """
    Compare log messages between captured messages and expected ones.

    Expected messages can contain regexes.

    Args:
        caplog:
            Caplog generated by pytest.
        expected_logs ([str]):
            List of strings/regexes containing expected logs lines.
    """
    assert len(caplog.records) == len(expected_logs)

    for i in range(len(expected_logs)):
        log_line = caplog.records[i].getMessage()
        match = re.search(expected_logs[i], log_line)
        if match is None:
            raise AssertionError(
                "Captured log line '{0}' couldn't be matched with '{1}'".format(
                    log_line, expected_logs[i]
                )
            )