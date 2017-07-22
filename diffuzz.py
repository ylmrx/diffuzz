import os, sys
import logging
import deepdiff
import click
from termcolor import colored
import hashlib
import pprint

def hash_file(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
        afile.close()
    return hasher.digest().encode('base64')[:7]

def diff_files(filepath1, filepath2):
    with open(filepath1, 'r') as fp1:
        buf1 = fp1.read()
        fp1.close
    with open(filepath2, 'r') as fp2:
        buf2 = fp2.read()
        fp2.close
    pprint.pprint(deepdiff.DeepDiff(buf1, buf2))



def many_files(start_directory, f, ext):
    many = []
    os.chdir(start_directory)
    os.chdir(f)
    logging.debug("Working in %s", os.getcwd())
    for (dirpath, dirnames, filenames) in os.walk('.'):
        for filename in filenames:
            if 'ALL' in ext:
                finder[f].append(os.path.join(dirpath, filename))
            else:
                for e in ext:
                    if filename.endswith(e):
                        end_path = os.path.join(dirpath, filename)
                        many.append(end_path)
                        logging.debug("found file %s" % end_path)
    return many

@click.command()
@click.option('--verbose/--quiet', default=False,
        help="Says more stuff, quiet by default")
@click.option('--out', default='-', type=click.File('w'),
        help="Output to a file, default to STDOUT")
@click.option('--ext', multiple=True, required=True,
        help="Search this file extension, ALL for everything (ALL could be a bad idea)")
@click.option('--diff', default=False, is_flag=True,
        help="Display the diff when the file was modified")
@click.argument('older', nargs=1, type=click.Path(exists=True))
@click.argument('newer', nargs=1, type=click.Path(exists=True))

def main(verbose, out, older, newer, diff, ext):
    """
    An advanced diff.
    """
    if verbose:
        logging.basicConfig(
                format=colored("verbose::%(message)s", 'yellow'), level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    start_directory = os.getcwd()
    finder = {older:[], newer:[]}
    logging.debug(start_directory)
    for f in finder.keys():
        finder[f] = many_files(start_directory, f, ext)

    constant_files = list(set(finder[older]) & set(finder[newer]))
    dict_hash = {}
    for i in constant_files:
        two_hashes = {}
        for f in finder.keys():
            two_hashes.update({f: hash_file(os.path.join(start_directory, f, i))})
        if two_hashes.values()[0] == two_hashes.values()[1]:
            print colored("MATCH : %s -- %s" % (two_hashes.values()[0], i), 'green')
        else:
            print colored("NOP : %s/%s -- %s" % (two_hashes.values()[0], two_hashes.values()[1], i), 'red')
            if diff:
                diff_files(os.path.join(start_directory, finder.keys()[0], i),
                        os.path.join(start_directory, finder.keys()[1], i))

