from __future__ import print_function
from scipy.io import loadmat
import cv2
import json
import sys

def convert_annotations(vbb):
    """Get the bounding boxes for MATLAB's vbb file format

    Argument:
       vbb: Matlab file containing the bounding boxes

    Returns:
       dict containing num_frames * num_objects * bbox's
    """

    num_frames = int(vbb['A'][0][0][0][0][0])
    objects_sequence = vbb['A'][0][0][1][0]
    annotations = {}

    for i in xrange(num_frames):
        objects_current_frame = objects_sequence[i]
        if objects_current_frame.shape[1] > 0:
            num_objects = objects_current_frame['pos'][0].shape[0]
            coords_list = []
            for obj in xrange(num_objects):
                coords_curr = {}
                box = objects_current_frame['pos'][0][obj]
                x1 = int(box[0][0])
                y1 = int(box[0][1])
                w = int(box[0][2])
                h = int(box[0][3])

                coords_curr['x1'] = x1
                coords_curr['y1'] = y1
                coords_curr['x2'] = x1 + w
                coords_curr['y2'] = y1 + h

                coords_list.append(coords_curr)
            im_info = {}
            im_info['num_objects'] = num_objects
            im_info['coords_list'] = coords_list

        else:
            im_info = {}
            im_info['num_objects'] = 0
            im_info['coords_list'] = []

        annotations['{:04d}.png'.format(i)] = im_info
        print('Processing annotations {}/{}'.format(i, num_frames), end='\r')
        sys.stdout.flush()

    return annotations



#get the annotation
#vbb = loadmat('./V000.vbb')

#d = convert_annotations(vbb)
#with open('annotations.json', 'w') as outfile:
#    json.dump(d, outfile)

def convert_sequence(vid, target_dir):
    """Convert the video sequence to images, and saves it in target directory

    Arguments:
        video sequence, output diretory
    """
    i = 0
    while True:
        ret, frame = vid.read()
        if not ret:
            print('\n')
            sys.stdout.flush()
            break
        cv2.imwrite('{}/{:04d}.png'.format(target_dir, i), frame)
        print('Number of images extracted:  {} '.format(i), end='\r')
        sys.stdout.flush()
        i += 1
