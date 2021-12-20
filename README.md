# Processing local alignments

You are probably all familiar with sequence alignments, at least I assume that you are, so reading a pair-wise alignment such as

```
ACCACAGT-CATA
A-CAGAGTACAAA
```

is second nature to you.

Writing an alignment as one sequence on top of another, with gaps inserted for indels to make the sequences have equal length, is a visually pleasing way to display alignments, but it has its drawback when it comes to local alignments in long genomic sequences.

In applications where you map short reads against a full genome, you will have hundreds of thousands if not millions of local alignments, where each local alignment is an approximative match of a read against the genome.

We cannot store this as a full alignment a short read against a full genome--and even if we could, it would not be helpful to scroll through millions of lines of gaps to try to find where the read sits in the genome. Instead, you need to store the genomic location, i.e., a chromosome and a position, and a local alignment that starts there.

If, for example, chromsome 14 at location 123,345 and 10 bases forward looks like this

```
...ACGTACGTAC...
   ^
   `- location 123,456
```

you might want to show a local match there as

```
ACGTAC-GTAC
AC-AACTGTCC
```

with some mark-up that specifies where the sequence from the genome comes from, e.g.

```
> chrom14-123,456
ACGTAC-GTAC
@ read 678,901
AC-AACTGTCC
```

or something to that affect.

This wouldn't necessarily be a bad way to represent mapped reads, but it is not how it is usually done. The so-called [SAM file format](https://en.wikipedia.org/wiki/SAM_(file_format)) doesn't included the genome-part of the pairwise alignment, but instead it stores the location (as above), the read sequence, and a description of the alignment, from which we can reconstruct it.

For most practical purposes, there is no benefit to one representation over another; the second one is just the one most tools expect. We can automatically translate between the two representations, and that is what this project is about.

## CIGARs, edits, and pairwise alignments

We won't work with the SAM format here, it has a lot of fields that we are not interested in, but we will explore how it represents alignments, how we can create one of our familiar local alignments from its representation, and how we can translate a familiar pairwise alignment into the format it uses.

To understand the dual representation of an alignment, we need to think of what the familiar alignment means in terms of how one sequence gets edited into another. In a simple alignment like this one:

```
ACCACAGT-CATA
A-CAGAGTACAAA
```

we can describe how to get from the first to the second sequence by going through the columns one by one. First we see an `A` over an `A`, and we can say that to get from the first sequence to the second, we just *match* the two. We will abbreviate that `M`. For the next column, we have a `C` over a gap, so to go from the first sequence to the second, we need to *delete* a character; we abbreviate this `D`. 

For the next two columns we match again, since we go from a `C` to a `C` and an `A` to an `A`. Then we see a `C` over a `G`. To go from the first sequence to the second, we need to substitute a `C` to a `G`. It would be natural to abbreviate this `S`, but we are going to use `M` for *mismatch*. I'm aware that we already used `M` for match, but it turns out to work out, because both of the `M` operations put a symbol from the first sequence on top of a symbol from the second, and the difference between matches and substitutions only matter if we wish to count how close the sequences are; it doesn't matter for describing the alignment.

Later in the sequence we have a column that puts a gap above an `A`. This is an *insertion* operation--it inserts a character to change the first sequence into the second--and we abbreviate it as `I`.

The same alignment, with the edits annotation written below it, looks like this:

```
ACCACAGT-CATA
A-CAGAGTACAAA
MDMMMMMMIMMMM
```

This sequence of edits, `MDMMMMMMIMMMM`, is a complete description of the alignment. If you have the two original sequences, `ACCACAGTCATA` and `ACAGAGTACAAA`, and the edits description, you can reconstruct the alignment. There are three differnt edit operations: `M`, `D`, and `I`. When you see an `M`, you remove the first letter from each of your sequences and make a column out of them. When you see a `D`, you take the first letter in the first second and make a column of it and a gap. If you see an `I`, you make a column of a gap and the first character in the second sequence.

```
Seq A = ACCACAGTCATA ; Seq B = ACAGAGTACAAA; Op = 'M' => Column (A,A)
Seq A = CCACAGTCATA  ; Seq B = CAGAGTACAAA ; Op = 'D' => Column (C,-)
Seq A = CACAGTCATA   ; Seq B = CAGAGTACAAA ; Op = 'M' => Column (C,C)
Seq A = ACAGTCATA    ; Seq B = AGAGTACAAA  ; Op = 'M' => Column (A,A)
Seq A = CAGTCATA     ; Seq B = GAGTACAAA   ; Op = 'M' => Column (C,G)
Seq A = AGTCATA      ; Seq B = AGTACAAA    ; Op = 'M' => Column (A,A)
Seq A = GTCATA       ; Seq B = GTACAAA     ; Op = 'M' => Column (G,G)
Seq A = TCATA        ; Seq B = TACAAA      ; Op = 'M' => Column (T,T)
Seq A = CATA         ; Seq B = ACAAA       ; Op = 'I' => Column (-,A)
Seq A = CATA         ; Seq B = CAAA        ; Op = 'M' => Column (C,C)
Seq A = ATA          ; Seq B = AAA         ; Op = 'M' => Column (A,A)
Seq A = TA           ; Seq B = AA          ; Op = 'M' => Column (T,A)
Seq A = A            ; Seq B = A           ; Op = 'M' => Column (A,A)
```

You will write two functions, `align()` and `edits()` that translate between the two representations. The `align()` function takes two sequences and a list of edits, represented as a string, and returns the two rows in the corresponding alignment. The function `edits()` takes the two rows of the pairwise alignment and returns the edits sequence as a string.

 - [ ] Implement the `align()` function according to the specifications in the documentation string and the description below.
 - [ ] Implement the `edits()` function according to the specifications in the documentation string and the description below.
 

The edits in the SAM format are not represented exactly as we have done, however; they are represented in the [CIGAR format](https://drive5.com/usearch/manual/cigar.html). You can follow the link to see a full description--the format is simple and the description is short--but the short comparison is that the CIGAR format has a few more operations and encode them in a slightly different way.

The CIGAR format can distinguish between matches and substitutions and various other things, but most tools do not use these extra codes and stick to those we used above. We are not going to explore these extra codes here; they do not add anything qualitatively to how we manipulate alignments, they only allow us to specify in more detail when a match is a match or what kind of mismatch we have if we have a mismatch.

The different encoding, however, is interesting, and we will examine it more.

In the CIGAR format, the sequence of edits above, `MDMMMMMMIMMMM`, is represented as `1M1D6M1I4M`. All reads come as pairs, where the first element is an integer and the second an operation, and you read `<i><op>` as "the next *i* operations are *op* operations". So, you expand the sequence `1M1D6M1I4M` as

```
1M => M      (1 M operation)
1D => D      (1 D operation)
6M => MMMMMM (6 M operations)
1I => I      (1 I operation)
4M => MMMM   (4 M operations)
```

and if you concatenate the result,

```python
>>> "".join(["M","D","MMMMMM","I","MMMM"])
'MDMMMMMMIMMMM'
```

you get the same sequence of edits as we had before.

Getting the numbers and operations out of a CIGAR string can be a little tricky, but I have provided a function for you, `split_pairs()`, that does this. Call it with a valid CIGAR string, i.e. a string the consists of pairs of integers and operations, and you get a list back with the integer-operation pair.

Going the other direction requires that we identify blocks of the same operation. We could split the string `'MDMMMMMMIMMMM'` into the list of blocks `['M','D','MMMMMM','I','MMMM']`, and from that we could get the number we have to put in front of each operation using `len()`:

```python
>>> [len(block) for block in ['M','D','MMMMMM','I','MMMM']]
[1, 1, 6, 1, 4]
```

and we can get the operation in each block by taking the first character:

```python
>>> [block[0] for block in ['M','D','MMMMMM','I','MMMM']]
['M', 'D', 'M', 'I', 'M']
```

To get the CIGAR from the blocks, we just need to combine the two. To get the blocks, you can use the function `split_blocks()` that I have written for you, but you are, of course, also welcome to write your own.

You will write two functions for working with CIGAR strings: `cigar_to_edits()` that translates a CIGAR string into a sequence of edits, and `edits_to_cigar()` that translates a string of edits into a CIGAR string.

- [ ] Implement the `cigar_to_edits()` function according to the specifications.
 - [ ] Implement the `edits_to_cigar()` function according to the specifications.
 

## Setting up the template code

You sometimes need to install Python modules for use in your own programs. One way to do this is to use the `pip` tool distributed with Python. This tool can read the modules you need from a file and install them, including their dependencies. To do that, use the command

```sh
> python3 -m pip install -r requirements.txt
```

where `requirements.txt` contains the list of modules you want to install. There is an example `requirements.txt` in this repository that installs the `pytest` tool. Try installing it.

In the example `requirements.txt` we install a modules for testing code, `pytest`.

## Testing your code

We use two types of tests on projects in CTiB, `doctest` which is part of the standard Python library and `pytest` which we need to install. You can use them to test your code in your repository, but we also run tests every time you commit to GitHub, so we can keep track of your progress along the way.

The `doctest` module will validate if a function matches the behaviour we have described in its documentatiton string; if the documentation includes code that evaluates the function, `doctest` will test if it actually does what we claim.

You can run it on the included template code by running

```sh
> python3 -m doctest src/*.py
```

The `pytest` tool makes it easy for you to write so-called "unit tests"--small test functions that validates that different aspects of your code is working. It looks for Python files whose name starts with `test_`, and in them, it will locate all functions whose names start with `test_` and run them. There is already a test file in this repository, so you can try running `pytest` with the command

```sh
> python3 -m pytest src
```

Both tests will fail right now because there are tests to check if you have implemented the functions you need for this project, and for obvious reasons, you haven't done that yet. However, when you have implemented what you neeed to do, the tests will pass, and that will tell you that you have succeeded in your task.

Whenever you make changes to your code, you should run `doctest` and `pytest` to ensure that everything is still working. If you add new code, you can include documentation strings so `doctest` can keep you honest about the documentation. If you want more detailed testing, you can add another test, as a `test_*` function in an existing file or in a new `test_*.py` file.

When you push changes from your repository to GitHub, GitHub will also run tests on your code, and you can see the results in the `Feedback` pull request or in the `Actions` window on your repository.

## Template code

In the `src/align.py` file you will find the functions `align()` and `edits()` with a description of what their interface should be. You need to implement these.

The file `src/test_align.py` contains code for testing the functions in `src/align.py`. You are welcome to, and encouraged to, add to the tests.

In the `src/cigar.py` file you will find the functions `cigar_to_edits()` and `edits_to_cigar()` with a description of what their interface should be. You need to implement these. In the same file, you can find the helper functions `split_pairs()` and `split_blocks()` that I have written for you.

The file `src/test_cibar.py` contains code for testing the functions in `src/cigar.py`. You are welcome to, and encouraged to, add to the tests.


## Building a command-line tool

There is a fifth Python file in `src`, `src/main.py`, that will show you have to build a command-line program in Python. Generally, you can run any Python code by calling `python3` with the file that contains the code, e.g.

```sh
> python3 foo.py
```

will run any code in the file `foo.py`. However, there is a little more to writing command-line tools than this. For a tool to be useful, the user needs a mechanism to provide input to program, in some case also a way to provide optional flags, and the user needs to get the results of running the code back.

The way the user informs the program about which flags/options to use and where to find input and where to write output is through command-line arguments, and the actual data that goes into the program and comes out again goes through files (or "streams", which are essentially the same thing).

The file `src/main.py` shows you a very rudementary way of handling this in Python; in later projects we will see more advanced (and better) techniques.

You do not need to modify anything in this file, but I encourage you to read it, to get an idea about how you can turn your own code into something that works as a command-line tool. It won't be long before you will need to know how to do this.

For this project, though, once you have implemented the functions in `src/align.py` and `src/cigar.py`, you can use `src/main.py` as a command-line tool.

It is the kind of tool that functions as a wrapper around more than one command, just like the `git` command is really multiple commands (`git commit`, `git push`, `git pull`, ...). Such wrapped commands are often called *sub-commands*, and you pick the right sub-command via the first argument. For `src/main.py`, you can either call the tool with

```sh
> python3 src/main.py from_cig
```

or with

```sh
> python3 src/main.py to_cig
```

The first command translates from CIGAR strings to pairwise alignments, and the second translate the other way.

The input format for the two commands differs, as one would expect since they translate in opposite directions. The input to `from_cig` is one line per alignment with the two sequences and a CIGAR string, separated by tabs. The output is three lines per alignment; a row per aligned sequence and a blank line after that. The input to `to_cig` is the output format from `from_cig` and the output is the input format for `from_cig`. Again, as one would expect if they are translating in opposite directions.


Right now, both commands expect to get the input from `stdin` and they will write the output to `stdout`, so you could, for example, use the `from_cig` subcommand as

```sh
> cat data/cigs.in | python3 src/main.py from_cig
```
or

```sh
> python3 src/main.py from_cig < data/cigs.in
```

to translate the data in `data/cigs.in` into pairwise alignments, or use

If you want the output to go to a file, you must redirect it

```sh
> python3 src/main.py from_cig < data/cigs.in > output.out
```

You can pipe the commands to translate both ways, and

```sh
> cat data/cigs.in | python3 src/main.py from_cig | python3 src/main.py to_cig
```

should give us our input back again.


Working only with `stdin` and `stdout` is a very primitive interface, and a user will typically expect that a program that can read a file can also take a filename as an argument, and while not all programs accept a filename for the output, it is common enough that we should consider providing it.

If you give the commands one more argument, they will interpret that is a file you want them to read their input from, so the two commands above could also be written as

```sh
> python3 src/main.py from_cig data/cigs.in
```

or

```sh
> python3 src/main.py to_cig data/alignments.in
```

One more argument, and you are specifying the output file as well, so

```sh
> python3 src/main.py from_cig data/cigs.in my-cigs.out
```

would write the result to `my-cigs.out`.

The other command we support, `to_cig`, should also be able to handle file arguments.

The arguments that a program gets are put in `sys.argv`, with the name of the program at `sys.argv[0]` and any following arguments after that. The number of real arguments this thus always `len(sys.argv) - 1`. You can test how many you have by checking `len(sys.argv)`:

```python
if len(sys.argv) == 1:
    # zero arguments -- this is an error since we need at least the subcommand
elif len(sys.argv) == 2:
    # one argument -- sys.argv[1] is the subcommand; files are stdin and stdout
elif len(sys.argv) == 3:
    # two arguments -- use sys.argv[2] for input and stdout for output
elif len(sys.argv) == 4:
    # two arguments -- use sys.argv[2] for input and sys.argv[3] for output
else:
    # more than two arguments; that is an error
```

To open an input file, a file you want to read from, use `open("filename")` or `open("filename", "r")`, and to open an output file, a file you want to write to, use `open("filename", "w")`.

 - [ ] Extend both programs such that if `len(sys.argv) in [3, 4]`, the program should read from a file you open as `open(sys.argv[2])`.
 - [ ] Extend both programs such that if `len(sys.argv) == 4`, the program should write to a file you open as `open(sys.argv[3], "w")`.

 If you have more than three arguments, terminate the program with `sys.exit(1)` to indicate an error.
 

 We are not doing any sensible tests in the arguments in this project, so you will not get user-friendly error messages if you provide input files that do not exist, or try to write to a file you do not have permission to write to. That is something we will improve upon in later projects.

Writing `python3 program.py` to run the program `program.py` doesn't look like other programs on the command-line, where we would usually just write `program` to run `program`. There isn't anything wrong with that, it just says that we use Python to execute the program. There are, however, ways of making Python programs look more like other programs. Several, in fact. But, you guessed it, we leave that for future projects. We have already covered a lot in one project, and once you have everything up and running, you can pad yourself on the shoulders and take a short break before we continue.
