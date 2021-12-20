"""A module for translating between alignments and edits sequences."""


def align(x: str, y: str, edits: str) -> tuple[str, str]:
    """Align two sequences from a sequence of edits.

    Args:
        x (str): The first sequence to align.
        y (str): The second sequence to align
        edits (str): The list of edits to apply, given as a string

    Returns:
        tuple[str, str]: The two rows in the pairwise alignment

    >>> align("ACCACAGTCATA", "ACAGAGTACAAA", "MDMMMMMMIMMMM")
    ('ACCACAGT-CATA', 'A-CAGAGTACAAA')

    """
    return "", ""


def edits(x: str, y: str) -> str:
    """Extract the edit operations from a pairwise alignment.

    Args:
        x (str): The first row in the pairwise alignment.
        y (str): The second row in the pairwise alignment.

    Returns:
        str: The list of edit operations as a string.

    >>> edits('ACCACAGT-CATA', 'A-CAGAGTACAAA')
    'MDMMMMMMIMMMM'

    """
    return ""
