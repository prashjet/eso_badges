import os
import numpy as np
from PIL import Image
import pandas as pd
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.font_manager as font_manager
font_dirs = ['/Library/Fonts']
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)
matplotlib.rcParams['font.family'] = 'Helvetica Neue LT Com'
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import warnings
warnings.filterwarnings("ignore")

def read_spreadsheet(filename):
    xl = pd.read_excel(filename)
    N_ppl = len(xl)
    tmp = ['{0} {1}'.format(xl['First Name'][i], xl['Surname'][i])
           for i in range(N_ppl)]
    xl['Full Name'] = tmp
    xl = xl.sort_values(['Surname'])
    xl = xl.set_index(np.arange(N_ppl))
    xl['idx'] = np.arange(N_ppl)
    return xl

def iterate_text(fig,
                 x0, y0, width, height,
                 xtxt, ytxt, text,
                 size_init=10,
                 del_size=0.1,
                 kw_text={}):
    ax = fig.add_axes([x0, y0, width, height])
    ax.axis('off')
    success = False
    size = size_init
    renderer = fig.canvas.get_renderer()
    fig_width = fig.get_window_extent(renderer=renderer).width
    while success==False:
        if size < size_init:
            txt.remove()
        txt = ax.text(xtxt, ytxt, text,
                      size = size ,
                      **kw_text)
        txt_width = txt.get_window_extent(renderer=renderer).width
        success = (txt_width < 0.95*fig_width)
        size -= del_size
    return txt

def get_template_nambebadge(event,
                            orientation='horizontal',
                            with_url=True,
                            alpha=0.5,
                            imgdir='img/',
                            color=None):
    # make figure
    mm2inch = 25.4
    if orientation is 'horizontal':
        bdg_width = 90./mm2inch
        bdg_height = 60./mm2inch
    elif orientation is 'vertical':
        bdg_height = 90./mm2inch
        bdg_width = 60./mm2inch
    else:
        raise ValueError('Orientation must be horizontal or vertical')
    fig = plt.figure(figsize=(bdg_width, bdg_height), dpi=300)

    # add background image
    if with_url is True:
        filename = '{0}{1}_with_url.jpg'.format(imgdir, orientation)
    else:
        filename = '{0}{1}_no_url.jpg'.format(imgdir, orientation)
    eso_logo = Image.open(filename)
    ax_eso = fig.add_axes([0, 0, 1, 1])
    ax_eso.imshow(eso_logo, alpha=alpha)
    ax_eso.axis('off')
    if color is not None:
        rect = Rectangle((0, 0), 1, 1,
                         facecolor=color,
                         alpha=0.5,
                         transform=ax_eso.transAxes)
        ax_eso.add_patch(rect)

    # add text
    if orientation is 'horizontal':
        # event name
        iterate_text(fig,
                     0., 0.84, 1, 0.1,
                     0.945, 0.5, event['Name'],
                     size_init=8,
                     kw_text={'ha':'right', 'va':'center', 'weight':'bold'})
        # event date
        iterate_text(fig,
                     0., 0.785, 1, 0.1,
                     0.945, 0.5, event['Date'],
                     size_init=8,
                     kw_text={'ha':'right', 'va':'center'})
    if orientation is 'vertical':
        # event name
        iterate_text(fig,
                     0., 0.66, 1, 0.1,
                     0.5, 0.5, event['Name'],
                     size_init=14,#8,
                     kw_text={'ha':'center', 'va':'center', 'weight':'bold'})
        # event date
        iterate_text(fig,
                     # 0., 0.623, 1, 0.1,
                     0., 0.6, 1, 0.1,
                     0.5, 0.5, event['Date'],
                     size_init=12,#8,
                     kw_text={'ha':'center', 'va':'center'})

    return fig

def add_names(fig,
              person,
              orientation='horizontal',
              outdir='.',
              outfile=None):

    txtlist = []
    if orientation is 'horizontal':
        # name
        txt = iterate_text(fig,
                0., 0.405, 1, 0.2,
                0.5, 0.5, person['Full Name'],
                size_init=16,
                kw_text={'ha':'center', 'va':'center', 'weight':'bold'})
        txtlist += [txt]
        # affilitation
        if person['Affiliation'] is not np.nan:
            txt = iterate_text(fig,
                    0., 0.26, 1, 0.2,
                    0.5, 0.5, person['Affiliation'],
                    size_init=12,
                    kw_text={'ha':'center', 'va':'center'})
            txtlist += [txt]
    if orientation is 'vertical':
        # first name
        txt = iterate_text(fig,
                0., 0.345, 1, 0.2,
                0.5, 0.5, person['First Name'].upper(),
                size_init=18,#14.,
                kw_text={'ha':'center', 'va':'center', 'weight':'bold'})
        txtlist += [txt]
        # surname
        txt = iterate_text(fig,
                0., 0.27, 1, 0.2,
                0.5, 0.5, person['Surname'],
                size_init=14,#13.8,
                kw_text={'ha':'center', 'va':'center', 'weight':'bold'})
        txtlist += [txt]
        # affilitation
        if person['Affiliation'] is not np.nan:
            txt = iterate_text(fig,
                    0., 0.187, 1, 0.2,
                    0.5, 0.5, person['Affiliation'],
                    size_init=14,#10,
                    kw_text={'ha':'center', 'va':'center'})
            txtlist += [txt]

    # save badge
    if outfile is None:
        outfile = 'namebadge_{0:03d}.png'.format(person['idx'])
    fig.savefig('{0}/{1}'.format(outdir, outfile))

    # remove all name text ready for next badge
    for txt in txtlist:
        txt.remove()

    return 0

def check_text_postion():

    # to check text position
    # make versions to compare with examples found on ESO website
    # http://www.eso.org/intra/org/pad/vi/

    test_event = pd.Series({'Name':'Name of the Event',
                            'Date':'Date of the Event'})
    test_horiz_person = pd.Series({'Full Name':'Name of the person',
                                   'Affiliation':'Affiliation (optional)'})
    test_vert_person = pd.Series({'First Name':'FIRST NAME',
                                  'Surname':'Last Name',
                                  'Affiliation':'Affiliation (optional)'})

    # horizontal check
    fig = get_template_nambebadge(test_event,
                                  orientation='horizontal',
                                  imgdir='img/withtxt/')
    add_names(fig,
              test_horiz_person,
              orientation='horizontal',
              outdir='img/withtxt/',
              outfile='horizontal_check.png')

    # vertical check
    fig = get_template_nambebadge(test_event,
                                  orientation='vertical',
                                  imgdir='img/withtxt/')
    add_names(fig,
              test_vert_person,
              orientation='vertical',
              outdir='img/withtxt/',
              outfile='vertical_check.png')

    return 0

def collate_on_page(N_ppl,
                    outdir,
                    tmpdir,
                    orientation='horizontal',
                    outroot='badges',
                    n_rows=3,
                    n_cols=3):

    n_per_page = n_rows * n_cols
    n_pages = int(np.ceil(N_ppl/n_per_page))
    mm2inch = 25.4
    page_width = 8.27
    page_height = 11.69
    border_width = 12./mm2inch
    border_height = 15./mm2inch
    bdg_width = 60./mm2inch
    bdg_height = 90./mm2inch
    pagesize = (page_width, page_height)
    # get canvas units i.e. page minus border
    cnv_width = page_width - 2*border_width
    cnv_height = page_height - 2*border_height

    if orientation is 'horizontal':
        rot = 90.
        rot_bk = 90 + 180.
    else:
        rot = 0.
        rot_bk = 0.

    def cnv_to_fig_units(cnv_units):
        cx0, cy0, cw, ch = cnv_units
        x0 = (cx0 * cnv_width + border_width)/page_width
        y0 = (cy0 * cnv_height + border_height)/page_height
        w = cw * cnv_width / page_width
        h = ch * cnv_height / page_height
        return x0, y0, w, h

    for i_page in range(n_pages):
        print('...', i_page+1, 'out of', n_pages)

        fig = plt.figure(figsize=pagesize, dpi=300)
        fig_bk = plt.figure(figsize=pagesize, dpi=300)

        for i_badge in range(n_per_page):

            idx = n_per_page * i_page + i_badge
            bfile = '{0}namebadge_{1:03d}.png'.format(tmpdir, idx)
            try:
                badge = Image.open(bfile)
            except:
                break
            x0 = (i_badge % n_cols)
            y0 = np.int(np.floor(1.*i_badge/n_rows))
            x0 /= 1.*n_cols
            y0 /= 1.*n_rows
            cnv = [x0, y0, 1./n_cols, 1./n_rows]
            ax = fig.add_axes(cnv_to_fig_units(cnv))
            img = badge.rotate(rot, expand=1)
            ax.imshow(img, aspect='auto')
            ax.axis('off')
            cnv = [1.-1./n_cols-x0, y0, 1./n_cols, 1./n_rows]
            ax_bk = fig_bk.add_axes(cnv_to_fig_units(cnv))
            img = badge.rotate(rot_bk, expand=1)
            ax_bk.imshow(img, aspect='auto')
            ax_bk.axis('off')

        outfile = '{0}/pages/{1}_{2:03d}_a.pdf'.format(outdir, outroot, i_page)
        fig.savefig(outfile)
        outfile = '{0}/pages/{1}_{2:03d}_b.pdf'.format(outdir, outroot, i_page)
        fig_bk.savefig(outfile)

    plt.close()

    return 0

def make_badges(particpant_file=None,
                event={},
                orientation='horizontal',
                alpha=0.5,
                with_url=True,
                outdir='.',
                tmpdir='individual',
                n_blank=0,
                color=None,
                delete_tmp=False,
                outfile='badges.pdf'):
    """create namebadges from an excel spreadsheet ready for doublesided printing

    Keyword arguments:
    particpant_file -- location of excel spreadsheet which has columns for Surname,
        First Name and Affiliation of participants
    event -- a dictionary {'Name':'xxx', 'Date':'yyy'}
    outdir -- directory to store the output, default current directory
    outfile -- name of output file, default badges.pdf
    orientation -- vertical or horizontal, default horizontal
    alpha -- transparency of background from 0 to 1, default 0.5
    with_url -- whether to use background with ESO url and name, default False
    n_blank -- number of blank badges to print, default 0
        (this is useful for unexpected arrivals & using up the last sheet of paper)
    delete_tmp -- delete individual badges/pages of badges, default False
    color -- color of background, accepts any matplotlib color specification

    Output:
    Creates 'badges.pdf' (or outfile) in outdir formatted for double-sided printing.
    If delete_tmp is False, additionally create subdirectories:
    - 'pages' which contains individual pages of badges
    - 'individual' with images of each individual namebadge
    """

    people = read_spreadsheet(particpant_file)
    n_ppl = len(people)

    # make out directory
    if os.path.isdir(outdir) is False:
        os.mkdir(outdir)

    # make tmp directory
    tmpdir = '{0}{1}/'.format(outdir, tmpdir)
    if os.path.isdir(tmpdir) is False:
        os.mkdir(tmpdir)

    # make tmp directory
    pagedir = '{0}pages/'.format(outdir)
    if os.path.isdir(pagedir) is False:
        os.mkdir(pagedir)

    fig = get_template_nambebadge(event,
                                  orientation=orientation,
                                  with_url=with_url,
                                  alpha=alpha,
                                  color=color)
    print('Making namebadge...')
    for index, person in people.iterrows():
        print('...', index+1, 'out of', n_ppl)
        add_names(fig,
                  person,
                  orientation=orientation,
                  outdir=tmpdir)
    if n_blank>0:
        print('Making blank badges')
    for i in range(index+1, index+n_blank+1):
        blnkfile = '{0}namebadge_{1:03d}.png'.format(tmpdir, i)
        fig.savefig(blnkfile)

    print('Collating namebadges on page...')
    collate_on_page(n_ppl + n_blank,
                    outdir,
                    tmpdir,
                    orientation=orientation)
    plt.close()

    print('Merging pages together')
    cmd = "/System/Library/Automator/Combine\ PDF\ "\
        "Pages.action/Contents/Resources/join.py -o {0}{1} {2}*pdf"
    cmd = cmd.format(outdir, outfile, pagedir)
    os.system(cmd)

    print('Cleaning')
    if delete_tmp:
        os.system("rm -r {0}".format(tmpdir))
        os.system("rm -r {0}".format(pagedir))

    print('Done!')

    return 0

# end
