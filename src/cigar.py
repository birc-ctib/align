"""A module for translating between alignments and edits sequences."""

import re


def split_pairs(cigar: str) -> list[tuple[int, str]]:
    """Split a CIGAR string into a list of integer-operation pairs.

    Args:
        cigar (str): A CIGAR string

    Returns:
        list[tuple[int, str]]: A list of pairs, where the first element is
        an integer and the second an edit operation.

    >>> split_pairs("1M1D6M1I4M")
    [(1, 'M'), (1, 'D'), (6, 'M'), (1, 'I'), (4, 'M')]

    """
    return [(int(i), op) for i, op in re.findall(r"(\d+)([^\d]+)", cigar)]


def cigar_to_edits(cigar: str) -> str:
    """Expand the compressed CIGAR encoding into the full list of edits.

    Args:
        cigar (str): A CIGAR string

    Returns:
        str: The edit operations the CIGAR string describes.

    >>> cigar_to_edits("1M1D6M1I4M")
    'MDMMMMMMIMMMM'

    """
    return ""


def split_blocks(x: str) -> list[str]:
    """Split a string into blocks of equal character.

    Args:
        x (str): A string, but we sorta think it would be edits.

    Returns:
        list[str]: A list of blocks.

    >>> split_blocks('MDMMMMMMIMMMM')
    ['M', 'D', 'MMMMMM', 'I', 'MMMM']

    """
    return [m[0] for m in re.findall(r"((.)\2*)", x)]


def edits_to_cigar(edits: str) -> str:
    """Encode a sequence of edits as a CIGAR.

    Args:
        edits (str): A sequence of edit operations

    Returns:
        str: The CIGAR encoding of edits.

    >>> edits_to_cigar('MDMMMMMMIMMMM')
    '1M1D6M1I4M'

    """
    return ""
