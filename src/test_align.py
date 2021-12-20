"""Tests for the align module."""

from align import align, edits


def test_align() -> None:
    """Testing the align() function."""
    assert align(
        "accaaagta",
        "acaaatgtcca",
        "MDMMIMMMMIIM"
    ) == ("acca-aagt--a", "a-caaatgtcca")
    assert align(
        "a", "", "1D"
    ) == ("a", "-")


def test_edits() -> None:
    """Testing the edits() function."""
    assert edits(
        "acca-aagt--a", "a-caaatgtcca"
    ) == "MDMMIMMMMIIM"
    assert edits(
        "acgttcga",
        "aaa---aa"
    ) == "MMMDDDMM"
