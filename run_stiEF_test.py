import sys
from argparse import ArgumentParser

from stiEF_tests import run


parser = ArgumentParser()
# parser.add_argument("--config_path", dest='accumulate', action='store_const', help='hellle')

if __name__ == "__main__":
    # print("ARGS", sys.argv)
    run(sys.argv)
