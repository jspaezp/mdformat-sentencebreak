# mdformat-sentencebreak

An [mdformat](https://github.com/executablebooks/mdformat) plugin that adds line wrapping based on sentence completion marks.

## Behavior

This input ....

```text
> Long sentences are broken at punctuation marks,
> unless the generated sentence would be extremely small
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.

> And it will not break sentences if
> they are inside something else ... emphasis for example
**Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.**

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.
**Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.**
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.

> Sentences are kept separate if they end in punctuation

Some.
Very.
Small.
Series.
of.
Sentences.

> Sentences are combined if they do not end in punctuation.

a
very
sloppy
sentence

```

Will get this ....

```
Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna.

**Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.**

Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna.
**Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.**
Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna.

Some.
Very.
Small.
Series.
of.
Sentences.

a very sloppy sentence
```

## Installation

> pip install mdformat-sentencebreak 
