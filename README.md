This repository contains some _blogging utilities_ made by me for my [blog](https://pncnmnp.github.io/blogs/blog.html).
The parser here **can convert any Markdown file to HTML** with the syntax mentioned [here](https://www.markdownguide.org/cheat-sheet/#basic-syntax) ( Note: Currently the parser does not support any extended features ).
As I use _vanilla HTML_ and _CSS_ for my site, this specification works well and has automated my task to a great extent.

## How to run
To run use:
`python3.6 to_html.py`

You will be asked to enter the `filepath` of your Markdown file and `title` of your HTML document.
You can use `spelling_corrector.py` to scan your MD files, though I am still working to make it efficient.

## Manual Changes
The `./templates/head.txt` and `./templates/tail.txt` contains the head and tail of the HTML file. Basically, the markdown parsed file is being sandwiched between these two files. **You will have to manually make changes to both these files**.

P.S. To see the parsing of this README file, open `./templates/extra/readme.html`.