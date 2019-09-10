# Qualitative Coding

Qualitative coding for comptuer scientists. 

Qualitative coding is a form of feature extraction in which text (or images,
video, etc.) is tagged with features of interest. Sometimes the codebook is
defined ahead of time, other times it emerges through multiple rounds of coding.
For more on how and why to use qualitative coding, see Emerson, Fretz, and
Shaw's *Writing Ethnographic Fieldnotes* or Shaffer's *Quantitative
Ethnography*.

Most of the tools available for qualitative coding and subsequent analysis were
designed for non-programmers. They are GUI-based, proprietary, and don't expose 
the data in well-structured ways. Concepts from computer science, such as trees,
sorting, and filtering, could also be applied to qualitative coding analysis if
the interface supported it. 

Qualitative Coding, or `qc`, was designed to address these issues. I have used
`qc` as a primary coding tool in a [SIGCSE
paper](http://chrisproctor.net/publications/proctor_2019_defining_cs.html) on
how K-12 schools define and design computer science courses. The impetus for
packaging and releasing a stable version was my own dissertation work. 

## Limitations

- Due to its nature as a command-line program, `qc` is only well-suited to coding textual data. 
- `qc` uses line numbers as a fundamental unit. Therefore, it requires text files in your corpus to be 
  hard-wrapped at 80 characters. The `init` task will handle this for you. 
- Currently, the only interface for actually doing the coding is a split-screen
  in vim, with the corpus text on one side and comma-separated codes adjacent. This works well 
  for me, but might not work well for you. I have other ideas in the pipeline,
  but they won't be around soon.

# Installation

    pip install qualitative-coding

# Setup 

- All the source files you want to code should be in a directory (possibly
  nested). 
- Choose a working directory. Run `qc init`. This will create `settings.yaml`.
- In `settings.yaml`, update `corpus_dir` with the directory holding your source
  files. This may be relative to `settings.yaml` or absolute. Similarly, specify
  directories for `codes_dir` `logs_dir`, `memos_dir`, and the YAML file where you want
  to store your codebook. Unless you're particular, the default settings are fine. 
- Run `qc init --prepare_corpus --prepare_codes --coder yourname`. This will
  hard-wrap all the text in your corpus at 80 characters and create blank coding
  files. 

# Usage

## Workflow

`qc` is designed to give you a powerful terminal-based interface. The general
workflow is to use `code` to apply qualitative codes to your text files. As you
go, you will start to have ideas about the meanings and organization of your
codes. Use `memo` to capture these. 

Once you finish a round of coding, it's time to reorganize your codes. Use
`codebook` to refresh the codebook based on new coding. Use `stats` to see the
distribution of your codes. If you want to move codes into a tree, make these
changes directly in the codebook's YAML. If you realize you have redundant
codes, use `rename`. 

The `--coder` argument supports keeping track of multiple coders on a project,
and there are options to filter on coder where relevant. Analytical tools, such
as correlations (on multiple units of analysis) and inter-rater reliability are
coming. 

## Tutorial

Create a new directory somewhere. We will create a virtual environment, intstall
`qc`, and download some sample text from Wikipedia. 

    $ python3 -m venv env
    $ source env/bin/activate
    $ pip install qualitative-coding
    $ qc init
    $ qc init
    $ curl -o corpus/what_is_coding.txt "https://en.wikipedia.org/w/index.php?title=Coding_%28social_sciences%29&action=raw"
    $ qc init --prepare-corpus --prepare-codes --coder chris

Now we're ready to start coding. This next command will open a split-window vim session. 
Add comma-separated codes to the blank file on the right. I usually page-up (control+u) 
and page-down (control+d) each file to keep their line numbers synchronized. Once you've 
added some codes, we can analyze and refine them.

    $ qc code chris -f
    $ qc codebook
    $ qc list
    - a_priori
    - analysis
    - coding_process
    - computers
    - errors
    - grounded_coding
    - themes

Now that we have coded our corpus (consisting of a single document), we should
think about whether these codes have any structure. All data in `qc` is stored
in flat files, so you can easily modify it by hand. Re-organize some of your
codes in `codebook.yaml`. When you finish, run `codebook` again. It will go
through your corpus and add any missing codes. 

    $ qc list
    - analysis
    - coding_process
        - a_priori
        - grounded_coding
    - computers
    - errors
    - themes

I decided to group a priori coding and grounded coding together under coding
process. Let's see some statistics on the codes:

    $ qc stats
    Code                  Count
    ------------------  -------
    analysis                  2
    coding_process            7
    .  a_priori               2
    .  grounded_coding        2
    computers                 2
    errors                    1
    themes                    2

`stats` has lots of useful filtering and formatting options. For example, `qc
stats --files wiki --depth 1 --min 10 --format latex` would only consider files
having "wiki" in the filename. Within these files, it would show only
top-level categories of codes having at least ten instances, and would output a
table suitable for inclusion in a LaTeX document. Use `--help` on any command to
see available options.

Next, we might want to see examples of what we have coded. 

    $ qc code analysis
    Showing results for codes:  analysis
    
    what_is_coding.txt (2)
    ================================================================================
    
    [0:3]
    In the [[social science|social sciences]], '''coding''' is an analytical process | analysis
    in which data, in both [[quantitative research|quantitative]] form (such as      | 
    [[questionnaire]]s results) or [[qualitative research|qualitative]] form (such   | 
    
    [52:57]
    process of selecting core thematic categories present in several documents to    | 
    discover common patterns and relations.<ref>Grbich, Carol. (2013). "Qualitative  | 
    Data Analysis" (2nd ed.). The Flinders University of South Australia: SAGE       | analysis
    Publications Ltd.</ref>                                                          | 
                                                                                     | 

Again, there are lots of options for filtering and viewing your coding. At some
point, you will probably want to revise your codes. You can easily rename a
code, or collapse codes together, with the `remane` command. This updates your 
codebook as well as in all your code files.

    $ qc rename grounded_coding grounded

At this point, you are starting to realize some of the deeper themes running
through your corpus. Capturing these in an "integrative memo" is an important
part of qualitative coding. `memo` will open a preformatted document for you in vim. 

    $ qc memo chris --message "Thoughts on coding process"

Congratulations! You have finished the first round of coding. Before you move
on, this would be an excellent time to check your files into version control.
I hope you find `qc` to be powerful and efficient; it's worked for me!

-Chris Proctor

## Commands

Use `--help` for a full list of available options for each command.

### init
Initializes a new coding project, as described above.

    $ qc init

### check
Checks that all required files and directories are in place. 

    $ qc check

### code
Opens a split-screen vim window with a corpus file and the corresponding code
file. The name of the coder is a required positional argument. 
Use `--pattern` to glob-match the corpus file you want to code. If
multiple are matched, you will be prompted to choose. The `--first-without-codes` option is
particularly useful for coding the next uncoded text.

    $ qc code chris -f

### codebook (cb)
Scans through all the code files and adds new codes to the codebook. 

    $ qc codebook

### list (ls)
Lists all the codes currently in use. By default, lists them as a tree. The `--expanded` option 
will instead flatten the list of codes, and list each as something like `subjects:math:algebra`.

    $ qc list --expanded

### rename
Goes through all the code files and replaces one code with another. Removes the old code from the codebook.

    $ qc rename funy funny

### find
Displays all occurences of the provided code(s). With the `--recursive` option, also includes child
codes in the codebook's tree of codes. Note that a code may appear multiple times in the codebook; in this case, 
the `--recursive` option will search for all children of all instances. When you want to grab text for a quotation,
use the `--textonly` option. The `--files` option lets you filter which corpus files to search.

    $ qc find math science art --recursive

### stats
Displays frequency of usage for each code. Note that counts include all usages of children.
List code names to show only certain codes. Filter code results with 
`--depth`, `--max`, and `--min`. Use the `--expanded` option to show the full name of each code, rather than the 
tree representation. Arguments to `--format` may be any supported by [tabulate](https://bitbucket.org/astanin/python-tabulate).
The `--files` option lets you filter which corpus files to use in computing stats.

    $ qc stats curriculum math algebra --depth 1
