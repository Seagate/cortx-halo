import os
import sys
import pathlib
import pytest
import argparse

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname
                                 (pathlib.Path(__file__)), '..'))

    default_path = os.path.join(os.path.dirname(pathlib.Path(__file__)), '..')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='path',
                        help='Any combination of directories,\
                        file names or node ids', default=default_path)
    parser.add_argument('-m', dest='marker',
                        help='Marker string for test group')
    args = parser.parse_args()

    args_list = ['-v']
    if args.marker:
        args_list.append('-m ' + args.marker)
    args_list.append(args.path)

    pytest.main(args_list)
