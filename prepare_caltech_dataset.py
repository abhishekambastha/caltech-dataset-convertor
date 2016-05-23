from __future__ import print_function
from scipy.io import loadmat
import cv2
import json
import sys
from pprint import pprint
import struct

def convert_annotations(vbb, prefix):
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

        annotations['{}_{:04d}.jpg'.format(prefix, i)] = im_info
        print('Processing annotations {}/{}'.format(i, num_frames), end='\r')
        sys.stdout.flush()

    return annotations


def read_header(ifile):

    feed = ifile.read(4)
    norpix = ifile.read(24)
    version = struct.unpack('@i', ifile.read(4))
    length = struct.unpack('@i', ifile.read(4))
    assert(length != 1024)
    descr = ifile.read(512)
    params = [struct.unpack('@i', ifile.read(4))[0] for i in range(0,9)]
    fps = struct.unpack('@d', ifile.read(8))
    # skipping the rest
    ifile.read(432)
    image_ext = {100:'raw', 102:'jpg',201:'jpg',1:'png',2:'png'}
    return {'w':params[0],'h':params[1],
                'bdepth':params[2],
                'ext':image_ext[params[5]],
                'format':params[5],
                'size':params[4],
                'true_size':params[8],
                'num_frames':params[6]}

def read_sequence(path, target_dir, prefix):

    ifile = open(path, 'rb')
    params = read_header(ifile)
    bytes = open(path, 'rb').read()

    # this is freaking magic, but it works
    extra = 8
    s = 1024
    seek = [0]*(params['num_frames']+1)
    seek[0] = 1024

    images = []

    for i in range(0, params['num_frames']):
        try:
            tmp = struct.unpack_from('@I', bytes[s:s+4])[0]

            s = seek[i] + tmp + extra
            if i == 0:
                val = struct.unpack_from('@B', bytes[s:s+1])[0]
                if val != 0:
                    s -= 4
                else:
                    extra += 8
                    s += 8
            seek[i+1] = s
            nbytes = struct.unpack_from('@i', bytes[s:s+4])[0]
            I = bytes[s+4:s+nbytes]

            open('{}/{}_{:04d}.jpg'.format(target_dir, prefix, i), 'wb+').write(I)
        except:
            continue

    return images

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

def test_conversion(test_path):
    annotations = None
    with open(test_path + '/annotations.json', 'r') as f:
        annotations = json.load(f)


    lis = annotations['0279.png']
    print(lis['coords_list'])
    print(type(lis['coords_list']))
    print(lis['coords_list'], len(lis['coords_list']))
    print(annotations['0279.png']['coords_list'][0]['x1'])
#    for img_path in glob.glob(test_path + '/*.png'):
#        img = cv2.imread(img_path)

if __name__ == '__main__':
    test_path = './target/set00/V000'
    test_conversion(test_path)
