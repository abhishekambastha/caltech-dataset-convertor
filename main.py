import os
from scipy.io import loadmat
from prepare_caltech_dataset import convert_sequence, convert_annotations, read_sequence
import cv2
import glob
import json

def process_seqs():
    """Convert the sequence files and save to similar dir structure"""

    for dir_name in glob.glob('data/set*'):
        parent_dir = os.path.split(dir_name)[-1]
        if not os.path.exists('target/{}'.format(parent_dir)):
            os.mkdir('target/{}'.format(parent_dir))
        for seq_path in glob.glob('{}/*.seq'.format(dir_name)):
            #vid = cv2.VideoCapture(seq_path)
            current_dir = os.path.splitext(os.path.basename(seq_path))[0]
            if not os.path.exists('target/{}/{}'.format(parent_dir, current_dir)):
                os.mkdir('target/{}/{}'.format(parent_dir, current_dir))
            #save it here!
            print('Converting {}/{}.seq'.format(parent_dir, current_dir))
            #convert_sequence(vid, 'target/{}/{}'.format(parent_dir, current_dir))
            read_sequence(seq_path, 'target/{}/{}'.format(parent_dir, current_dir))


def process_annotations():
    """Convert annotations to json file format"""

    for dir_name in glob.glob('data/annotations/set*'):
        parent_dir = os.path.split(dir_name)[-1]
        if not os.path.exists('target/{}'.format(parent_dir)):
            os.mkdir('target/{}'.format(parent_dir))
        for vbb_file in glob.glob('{}/*.vbb'.format(dir_name)):
            current_dir = os.path.splitext(os.path.basename(vbb_file))[0]
            vbb = loadmat(vbb_file)
            print('Converted annotations from {}'.format(vbb_file))
            annotation = convert_annotations(vbb)

            if not os.path.exists('target/{}/{}'.format(parent_dir, current_dir)):
                os.mkdir('target/{}/{}'.format(parent_dir, current_dir))
            with open('target/{}/{}/annotations.json'.format(parent_dir, current_dir), 'w') as f:
                json.dump(annotation, f)

def main():
    if not os.path.exists('target'):
        os.mkdir('target')

    process_seqs()

    process_annotations()


if __name__ == '__main__':
    main()
