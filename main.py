import os
from scipy.io import loadmat
from prepare_caltech_dataset import convert_sequence, convert_annotations, read_sequence
import cv2
import glob
import json

def process_seqs():
    """Convert the sequence files and save to similar dir structure"""

    if not os.path.exists('target/images'):
        os.mkdir('target/images')

    for dir_name in glob.glob('data/set*'):
        parent_dir = os.path.split(dir_name)[-1]
        for seq_path in glob.glob('{}/*.seq'.format(dir_name)):
            current_dir = os.path.splitext(os.path.basename(seq_path))[0]
            print('Converting {}/{}.seq'.format(parent_dir, current_dir))
            read_sequence(seq_path, 'target/images', parent_dir + '_' + current_dir)


def process_annotations():
    """Convert annotations to json file format"""

    final_annotation = {}
    if not os.path.exists('target/Annotations'):
        os.mkdir('target/Annotations')

    for dir_name in glob.glob('data/annotations/set*'):
        parent_dir = os.path.split(dir_name)[-1]
        for vbb_file in glob.glob('{}/*.vbb'.format(dir_name)):
            current_dir = os.path.splitext(os.path.basename(vbb_file))[0]
            vbb = loadmat(vbb_file)
            print('Converted annotations from {}'.format(vbb_file))
            annotation = convert_annotations(vbb, '{}_{}'.format(parent_dir, current_dir))
            final_annotation.update(annotation)

    with open('target/Annotations/annotations.json', 'w') as f:
        json.dump(final_annotation, f)


def main():
    if not os.path.exists('target'):
        os.mkdir('target')

    #process_seqs()

    process_annotations()


if __name__ == '__main__':
    main()
