import json

from repo_health.check_github import parse_build_duration_response


class TestCIDurationChecks:

    @staticmethod
    def read_json_data(file_path):
        with open(file_path) as f:
            return json.load(f)

    def test_no_ci_for_repo_response(self):
        data = self.read_json_data('tests/graphql_responses/ci_duration_response_empty.json')
        total_time, checks = parse_build_duration_response(data)

        assert not checks
        assert total_time == ''

    def test_single_check_ci_time(self):
        data = self.read_json_data('tests/graphql_responses/ci_duration_response_single.json')
        total_time, checks = parse_build_duration_response(data)

        assert len(checks) == 1
        assert total_time == '3 minutes 11 seconds'

    def test_multiple_checks_ci_time(self):
        data = self.read_json_data('tests/graphql_responses/ci_duration_response_multiple_runs.json')
        total_time, checks = parse_build_duration_response(data)

        assert len(checks) == 6
        assert total_time == '5 minutes 24 seconds'

    def test_multiple_suits_time(self):
        data = self.read_json_data('tests/graphql_responses/ci_duration_response_multiple_suits.json')
        total_time, checks = parse_build_duration_response(data)

        assert len(checks) == 7
        assert total_time == '10 minutes 10 seconds'

    def test_some_checks_in_progress(self):
        data = self.read_json_data('tests/graphql_responses/ci_duration_response_in_progress.json')
        total_time, checks = parse_build_duration_response(data)

        assert len(checks) == 1
        assert total_time == '2 minutes 0 seconds'

    def test_checks_sorting(self):
        data = self.read_json_data('tests/graphql_responses/ci_duration_response_multiple_runs.json')
        _, checks = parse_build_duration_response(data)

        assert len(checks) == 6

        # Slowest Check
        assert checks[0]['name'] == 'unit_tests (py38, django31)'
        assert checks[0]['duration'] == '5 minutes 23 seconds'

        # Fastest Check
        assert checks[-1]['name'] == 'quality_and_translations_tests'
        assert checks[-1]['duration'] == '3 minutes 8 seconds'
