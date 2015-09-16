import os
import re
import cPickle
from scipy import misc
from PIL import Image
import fnmatch
import numpy as np


data_path = os.getcwd() + '\\data-sets\\sd_nineteen\\HSF_0'

DATA = ([[]], [[]])

im_size = (28, 28)


def helper(data, dirname, fnames):

    id_num_pat = re.compile("\d{4}")
    match = id_num_pat.search(dirname)
    if match:
        id_num = match.group(0)

        U_id = 'U' + id_num
        L_id = 'L' + id_num

        U_matches = fnmatch.filter(fnames, '*' + U_id + '*')
        U_matches = fnmatch.filter(U_matches, '*.bmp')

        L_matches = fnmatch.filter(fnames, '*' + L_id + '*')
        L_matches = fnmatch.filter(L_matches, '*.bmp')

        # initialize the output data
        u_alph = []
        l_alph = []

        for u, l in zip(U_matches, L_matches):

            # get actual letter as a string to store in output data
            ltr_id_pat_u = re.compile('_[A-Z]_')
            ltr_id_pat_l = re.compile('_[a-z]_')
            ltr_match_u = ltr_id_pat_u.search(u)
            ltr_match_l = ltr_id_pat_l.search(l)

            # extract raw letter ex: '_a_'
            ltr_raw_u = ltr_match_u.group(0)
            ltr_raw_l = ltr_match_l.group(0)

            # extract actual letter ex: from '_a_' -> 'a'
            ltr_u = ltr_raw_u[1]
            ltr_l = ltr_raw_l[1]

            # define name of image file
            fname_u = os.path.join(data_path, dirname, u)
            fname_l = os.path.join(data_path, dirname, l)

            # convert image to numpy array
            im_u = misc.imread(fname_u, flatten=True)
            im_l = misc.imread(fname_l, flatten=True)

            # remove excess whitespace around letters
            idx_u = np.where(im_u - 255.)
            idx_l = np.where(im_l - 255.)

            box_u = map(min, idx_u)[::-1] + map(max, idx_u)[::-1]
            box_l = map(min, idx_l)[::-1] + map(max, idx_l)[::-1]

            s1_u = box_u[3] - box_u[1]
            s2_u = box_u[2] - box_u[0]

            s1_l = box_l[3] - box_l[1]
            s2_l = box_l[2] - box_l[0]

            if s2_u > s1_u:
                width_u = s2_u
            else:
                width_u = s1_u

            if s2_l > s1_l:
                width_l = s2_l
            else:
                width_l = s1_l

            # trim the images to exclude white space
            im_u = im_u[box_u[1]:(box_u[1] + width_u),
                        box_u[0]:(box_u[0] + width_u)]
            im_l = im_l[box_l[1]:(box_l[1] + width_l),
                        box_l[0]:(box_l[0] + width_l)]

            # make the image smaller using nearest interpolation
            im_u = misc.imresize(im_u, (28, 28), interp='nearest')
            im_l = misc.imresize(im_l, (28, 28), interp='nearest')

            # scale the image down so each pixel is btwn 0. and 1.
            im_u = np.divide(im_u, 255.)
            im_l = np.divide(im_l, 255.)

            u_alph.append((im_u, ltr_u))
            l_alph.append((im_l, ltr_l))

        (u, l) = data
        u.append(u_alph)
        l.append(l_alph)
        data = (u, l)

os.path.walk(data_path, helper, DATA)

output = open('alphabets2.pkl', 'wb')

cPickle.dump(DATA, output)

output.close()
