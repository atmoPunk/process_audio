from pydub import AudioSegment
import argparse
import re
import os
from datetime import timedelta

parse_interval = re.compile(r'((?P<minutes>\d+?):)?((?P<seconds>\d+))?')


def parse_int(x):
    return int(x) if x else 0


def get_intervals(string):
    inter = string[1:-1].split()
    start = parse_interval.match(inter[0]).groupdict()
    start = {k: parse_int(v) for k, v in start.items()}
    start = timedelta(minutes=start['minutes'], seconds=start['seconds'])
    end = parse_interval.match(inter[1]).groupdict()
    end = {k: parse_int(v) for k, v in end.items()}
    end = timedelta(minutes=end['minutes'], seconds=end['seconds'])
    return (start, end)


def reverse(args):
    audio = AudioSegment.from_file(args.input)
    rvrs = audio.reverse()
    with open(args.output, 'wb') as f:
        rvrs.export(f)


def concatenate(args):
    result = AudioSegment.from_file(args.head)
    for audio in args.tail:
        result += AudioSegment.from_file(audio)
    with open(args.output, 'wb') as f:
        result.export(f)


def split(args):
    inp = AudioSegment.from_file(args.input)
    out_name, out_ext = os.path.splitext(args.output)
    intervals = [get_intervals(interval) for interval in args.intervals]
    counter = 0
    for start, end in intervals:
        inp_slice = inp[start.total_seconds() * 1e+3:end.total_seconds() * 1e+3]
        with open(out_name + str(counter) + out_ext, 'wb') as f:
            inp_slice.export(f)
            counter += 1


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

reverse_help = 'Reverse an audiofile.'
reverse_parser = subparsers.add_parser('reverse', help=reverse_help, description=reverse_help)
reverse_parser.add_argument('input', type=str, help='an audiofile to reverse')
reverse_parser.add_argument('output', type=str, help='file in which result will be stored')
reverse_parser.set_defaults(func=reverse)

concatenate_help = 'Concatenate a set of audiofiles.'
concatenate_parser = subparsers.add_parser('concatenate', help=concatenate_help,  description=concatenate_help)
concatenate_parser.add_argument('head', type=str, help='first audiofile')
concatenate_parser.add_argument('tail', type=str, nargs='+', help='rest of the files')
concatenate_parser.add_argument('output', type=str, help='file in which result will be stored')
concatenate_parser.set_defaults(func=concatenate)

split_help = 'Split an audiofile.'
split_parser = subparsers.add_parser('split', help=split_help, description=split_help)
split_parser.add_argument('input', type=str, help='an audiofile to split')
split_parser.add_argument('intervals', type=str, nargs='+', help='intervals in which audiofile will be split, format = "[beginning end]"')
split_parser.add_argument('output', type=str, help='name of output files. if contains extension (.ext) then output will be nameX.ext, else just nameX')
split_parser.set_defaults(func=split)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
