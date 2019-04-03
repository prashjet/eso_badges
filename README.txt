ESO namebadges
====

#### AUTHORS

* Prashin Jethwa <prashinjethwa@gmail.com>

-------------------------------------------------------------------------------

CONTENTS
--------

* description
* requirements
* usage/example

-------------------------------------------------------------------------------

## DESCRIPTION

Code to make namebadges for ESO meetings. Takes spreadsheet of participants as input. Allows for various options (e.g. vertical/horizontal, colours etc), and produces pdf documents ready for double-sided printing.

-------------------------------------------------------------------------------

## REQUIRMENTS

Requires [Pandas](https://pandas.pydata.org/), [Python Imaging Library](https://pillow.readthedocs.io/en/stable/) and standard Python libraries.

-------------------------------------------------------------------------------

## UASAGE/EXAMPLE

Use the

  $ make_badges

function, which accepts the following keyword arguments:

* particpant_file -- location of excel spreadsheet which has columns for Surname, First Name and Affiliation of participants
* event -- a dictionary {'Name':'xxx', 'Date':'yyy'}
* outdir -- directory to store the output, default current directory
* outfile -- name of output file, default badges.pdf
* orientation -- vertical or horizontal, default horizontal
* alpha -- transparency of background from 0 to 1, default 0.5
* with_url -- whether to use background with ESO url and name, default False
* n_blank -- number of blank badges to print, default 0 (this is useful for unexpected arrivals & using up the last sheet of paper)
* delete_tmp -- delete individual badges/pages of badges, default False
* color -- color of background, accepts matplotlib color specification

and creates output:

* 'badges.pdf' (or outfile) in outdir
* if delete_tmp is False, additionally create subdirectories 'pages' which contains individual pages of badges, and 'individual' with images of each individual namebadge

An example excel spreadsheet and output can be found in the 'example' directory. Create this using the script:

  $ python example_script.py

END
