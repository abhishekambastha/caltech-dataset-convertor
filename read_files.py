import os
import glob

for dir_name in glob.glob('data/set*'):
    print('Found Directory: {}'.format(dir_name))
    for sequence in glob.glob('{}/*.seq'.format(dir_name)):
        print('\tSequence File: {}'.format(sequence))

for dir_name in glob.glob('data/annotations/set*'):
    print('Found Annotation Directory: {}'.format(dir_name))
    for vbb in glob.glob('{}/*.vbb'.format(dir_name)):
        print('\tAnnotation File: {}'.format(vbb))

