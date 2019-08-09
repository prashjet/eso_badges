from namebadge import make_badges

event = {'Name':'Luminaries of Astronomy', 'Date':'9/8/19'}
outdir = 'example_output'

particpant_file  = 'example/participants.xlsx'
make_badges(particpant_file=particpant_file,
            event=event,
            outdir=outdir,
            orientation='vertical',
            alpha=1.,
            with_url=False,
            delete_tmp=True,
            n_blank=7,
            color=None,
            outfile='badges.pdf')

# event = {'Name':'Preparing for 4MOST', 'Date':'6-8/5/19'}
# outdir = '../4most/'
#
# particpant_file  = '../4most/socloc.xlsx'
# make_badges(particpant_file=particpant_file,
#             event=event,
#             outdir=outdir,
#             orientation='vertical',
#             alpha=1.,
#             with_url=False,
#             delete_tmp=True,
#             n_blank=8,
#             color='yellow',
#             outfile='socloc_badges.pdf')

# END
