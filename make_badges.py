from namebadge import make_badges

"""create namebadges from an excel spreadsheet ready for doublesided printing

Keyword arguments:
particpant_file -- location of excel spreadsheet which has columns for Surname,
    First Name and Affiliation of participants
event -- a dictionary {'Name':'xxx', 'Date':'yyy'}
outdir -- directory to store the output, default current directory
outfile -- name of output file, default badges.pdf
orientation -- vertical or horizontal, default horizontal
n_blank -- number of blank badges to print, default 0
alpha -- transparency of background from 0 to 1, default 0.5
with_url -- whether to use background with ESO url and name, default False
delete_tmp -- delete individual badges/pages of badges, default False

Output:
Creates 'badges.pdf' (or outfile) in outdir formatted for double-sided printing.
If delete_tmp is False, additionally create subdirectories:
- 'pages' which contains individual pages of badges
- 'individual' with images of each individual namebadge
"""

particpant_file  = 'example/participants.xlsx'
event = {'Name':'Luminaries of Astronomy', 'Date':'11/10/18'}
outdir = 'example/'
make_badges(particpant_file=particpant_file,
            event=event,
            outdir=outdir,
            orientation='vertical',
            alpha=0.5,
            with_url=False,
            n_blank=5,
            color='yellow',
            delete_tmp=True)
