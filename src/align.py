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


def local_align(chrom: str, pos: int, read: str, edits: str) -> tuple[str, str]:
    """Extract a local alignment from a chromosome and a pattern.

    This function works almost as align(), except that it doesn't
    align all of the chrom sequence but only a subsequence of it.

    Args:
        chrom (str): A (potentially large) chromosomal sequence.
        pos (int): The position in the chromosomal sequence, 0-indexed, where
                   the alignment starts.
        read (str): The read we have matched against the genome.
        edits (str): The sequence of edit operations.

    Returns:
        tuple[str, str]: The two rows in the local pairwise alignment

    >>> local_align("GTAACCACAGTCATA", 3, "ACAGAGTACAAA", "MDMMMMMMIMMMM")
    ('ACCACAGT-CATA', 'A-CAGAGTACAAA')
    """
    i, j = pos, 0
    row_x, row_y = [], []
    for op in edits:
        match op:
            case 'M':
                row_x.append(chrom[i])
                row_y.append(read[j])
                i += 1
                j += 1
            case 'D':
                row_x.append(chrom[i])
                row_y.append('-')
                i += 1
            case 'I':
                row_x.append('-')
                row_y.append(read[j])
                j += 1

    return "".join(row_x), "".join(row_y)
