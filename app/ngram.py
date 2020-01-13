#!/usr/bin/env python3
import fileinput
import re
import argparse
from itertools import groupby


def ngrams(words):
    for length in range(1,3):
        for ngram in zip(*(words[i:] for i in range(length))):
            #print(length, ngram)
            yield ngram

def mapper(line):
    words = re.findall(r'[a-zA-z]+', line)
    #print('words:', words)
    for ngram in ngrams(words):
        yield ' '.join(ngram), 1

def do_mapper(files):
    #print('files',files)
    for line in fileinput.input(files):
        for key, value in mapper(line):
            yield key, value

def reducer(key, values):
    count = sum(map(int, values))
    return key, count

def do_reducer(files):
    pairs = map(lambda line: line.strip().split('...', 1)  , fileinput.input(files))
    for key, value in groupby(pairs, lambda x: x[0]):
        values = (v for k, v in value)
        yield reducer(key, values)
    

if  __name__ == '__main__':

    parser = argparse.ArgumentParser(description='N-gram counter')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', '--mapper', action='store_true')
    group.add_argument('-r', '--reducer', action='store_true')
    parser.add_argument('files', type=str, nargs='*')

    args = parser.parse_args()

    if args.mapper:
        for key, value in do_mapper(args.files):
            print('{}...{}'.format(key, value))
    else:
        for key, value in do_reducer(args.files):
            print('{}...{}'.format(key, value))
        
    '''
    s = 'i am a superman'
    print(list(mapper(s)))

    print(list(reducer('a',[1,2,1,5])))
    '''
