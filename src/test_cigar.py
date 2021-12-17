"""Tests for the cigar module."""

from cigar import (
    split_pairs,
    cigar_to_edits,
    split_blocks,
    edits_to_cigar
)


def test_split_pairs() -> None:
    """Testing the split_pairs() function."""
    assert split_pairs("1M1I1D1M1I1D") == [
        (1, 'M'), (1, 'I'), (1, 'D'),
        (1, 'M'), (1, 'I'), (1, 'D'),
    ]
    assert split_pairs("2M2I2D") == [
        (2, 'M'), (2, 'I'), (2, 'D'),
    ]
    assert split_pairs("1M2I3D") == [
        (1, 'M'), (2, 'I'), (3, 'D'),
    ]
    assert split_pairs("3M2I1D") == [
        (3, 'M'), (2, 'I'), (1, 'D'),
    ]
    assert split_pairs("") == [
    ]


def test_cigar_to_edits() -> None:
    """Testing the cigar_to_edits() function."""
    assert cigar_to_edits("1M1D1I1M1I1D") == "MDIMID"
    assert cigar_to_edits("2M2D2I2M2I2D") == "MMDDIIMMIIDD"
    assert cigar_to_edits("1M2D3I2M1I2D") == "MDDIIIMMIDD"
    assert cigar_to_edits("") == ""


def test_split_blocks() -> None:
    """Testing the split_blocks() function."""
    assert split_blocks("MID") == ["M", "I", "D"]
    assert split_blocks("MIIDDD") == ["M", "II", "DDD"]
    assert split_blocks("MIIDDDMMMDDI") == ["M", "II", "DDD", "MMM", "DD", "I"]
    assert split_blocks("") == []


def test_edits_to_cigar() -> None:
    """Testing the edits_to_cigar() function."""
    assert edits_to_cigar("MDIMID") == "1M1D1I1M1I1D"
    assert edits_to_cigar("MMDDIIMMIIDD") == "2M2D2I2M2I2D"
    assert edits_to_cigar("MDDIIIMMIDD") == "1M2D3I2M1I2D"
    assert edits_to_cigar("") == ""
