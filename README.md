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

If, for example, chromsome 14 at locattion 123,345 and 10 bases forward looks like this

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

It would be a better solution than having the full genome in each alignment, but it is still somewhat wasteful in the storage required.

If you have sequenced a genome to, say, 30X, it means that you have reads that over each base pair in the genome on average 30 times. If you store local alignments in a format like this, the full genomic sequence will be represented about 30 times, because we have a copy of a base-pair each time it is part of a read. (And it is actually substantially worse than this, since we also store all the flanking sequence).





**FIXME: describe project**



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

**FIXME:** Descripe template code


## Building a command-line tool

There is a third Python file in `src`, `src/main.py`, that will show you have to build a command-line program in Python. Generally, you can run any Python code by calling `python3` with the file that contains the code, e.g.

```sh
> python3 foo.py
```

will run any code in the file `foo.py`. However, there is a little more to writing command-line tools than this. For a tool to be useful, the user needs a mechanism to provide input to program, in some case also a way to provide optional flags, and the user needs to get the results of running the code back.

The way the user informs the program about which flags/options to use and where to find input and where to write output is through command-line arguments, and the actual data that goes into the program and comes out again goes through files (or "streams", which are essentially the same thing).

The file `src/main.py` shows you a very rudementary way of handling this in Python; in later projects we will see more advanced (and better) techniques.

**FIXME: more here**
