from curses import meta
from os import getcwd
from os.path import join, dirname

import time
import pickle
from utils import augmentation


PATH_REPO = join(dirname(getcwd()), 'text-augmentation')
PATH_DATA = join(PATH_REPO, 'data')
PATH_OUTPUT = join(PATH_REPO, 'output')


import json
import argparse
import logging
logging.basicConfig(level=logging.INFO)



if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='augment text data')
	
    parser.add_argument('--PATH_DATA', metavar='t', type=str, help='Path of the directory where your datafile is stored', default=PATH_DATA)
    parser.add_argument('--name_data', metavar='t', type=str, help='name of your datafile .json', default='dict_requests')
    parser.add_argument('--PATH_OUTPUT', metavar='t', type=str, help='Path of the directory where you want to store your augmented data', default=PATH_OUTPUT)
    args = parser.parse_args()


    logging.info('Loading data...')
    a_file = open(join(args.PATH_DATA, f'{args.name_data}.json'), "r")
    data_dict = json.loads(a_file.read())

    logging.info('Augmenting data...')
    start = time.time()
    dict_augmented = augmentation.augmentation_tests(data_dict)	
    end = time.time()

    logging.info(f"Your original data had {len(data_dict)} samples and your new data has {len(dict_augmented)} samples. The process lasted {end-start} seconds")

    logging.info(f'Saving datafile: data_augmented.json in {PATH_OUTPUT} directory')
    a_file = open(join(args.PATH_OUTPUT, 'data_augmented.json'), "w")
    json.dump(dict_augmented, a_file)
    a_file.close()

    ####
