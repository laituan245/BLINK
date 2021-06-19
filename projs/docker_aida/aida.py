import sys
import os
import logging
import ujson as json
from collections import defaultdict
import subprocess

PWD = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)


def aida_en(path, path_nom, path_pro, outpath, freebase=False, candidates=False):
    pass


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 6:
        print('USAGE: <lang> <path to nam tab> <path to nom tab> <path to pro tab> <output dir>')
        exit()

    # Extract arguments and create the output directory
    lang, pnam, pnom, ppro, outdir = argv[1], argv[2], argv[3], argv[4], argv[5]
    os.makedirs(outdir, exist_ok=True)

    if lang == 'en':
        aida_en(pnam, pnom, ppro, '%s/en.linking.tab' % outdir, candidates=True)
        aida_en(pnam, pnom, ppro, '%s/en.linking.freebase.tab' % outdir, freebase=True, candidates=True)
