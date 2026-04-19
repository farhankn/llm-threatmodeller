from pathlib import Path

from threatcli.evaluation.runner import discover_fixtures


def test_discover_fixtures_finds_expected_cases() -> None:
    fixtures = discover_fixtures([Path("tests/fixtures")])
    fixture_names = {path.name for path in fixtures}
    assert "tri_01" in fixture_names
    assert "adv_01" in fixture_names

