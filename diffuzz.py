import os, sys
import logging
import deepdiff
import click
from termcolor import colored
import hashlib
import pprint

@click.command()
@click.option('--verbose/--quiet', default=False,
        help="Says more stuff, quiet by default")
@click.option('--out', default='-', type=click.File('w'),
        help="Output to a file, default to STDOUT")
@click.option('--ext', multiple=True, required=True,
        help="Search this file extension, ALL for everything (ALL could be a bad idea)")
@click.argument('older', nargs=1, type=click.Path(exists=True))
@click.argument('newer', nargs=1, type=click.Path(exists=True))


def main(verbose, out, older, newer, ext):
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
                            finder[f].append(os.path.join(dirpath, filename))
                            print os.path.join(dirpath, filename)

    constant_files = list(set(finder[older]) & set(finder[newer]))
    dict_hash = {}
    for i in constant_files:
        two_hashes = {}
        for f in finder.keys():
            hasher = hashlib.md5()
            with open(os.path.join(start_directory, f, i), 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
                afile.close()
            two_hashes.update({f: hasher.digest().encode('base64')[:7]})
        if two_hashes.values()[0] == two_hashes.values()[1]:
            print colored("MATCH : %s -- %s" % (two_hashes.values()[0], i), color='green')
        else:
            print colored("NOP : %s/%s -- %s" % (two_hashes.values()[0],two_hashes.values()[1], i), color="red")

