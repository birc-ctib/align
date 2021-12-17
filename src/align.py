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
    i, j = 0, 0
    row_x, row_y = [], []
    for op in edits:
        match op:
            case 'M':
                row_x.append(x[i])
                row_y.append(y[j])
                i += 1
                j += 1
            case 'D':
                row_x.append(x[i])
                row_y.append('-')
                i += 1
            case 'I':
                row_x.append('-')
                row_y.append(y[j])
                j += 1

    return "".join(row_x), "".join(row_y)


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
    assert len(x) == len(y)
    edits = [None] * len(x)
    for i, _ in enumerate(x):
        if x[i] == '-':
            edits[i] = 'I'
        elif y[i] == '-':
            edits[i] = 'D'
        else:
            edits[i] = 'M'
    return "".join(edits)
