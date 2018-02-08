import sys
import argparse

parser = argparse.ArgumentParser(description='Process some arguments.')
parser.add_argument('-s', help='Set the server ip address.')
parser.add_argument('-p', help='Set the server port.')
parser.add_argument('-z', help='Set the socket size')
parser.add_argument('-t', help='Set the hashtag being searched.')

args = parser.parse_args()

if args.s == None:
    print('Please set server ip address with the -s flag.')
    sys.exit(1)
if args.p == None:
    print('Please set server port with the -p flag.')
    sys.exit(1)
if args.z == None:
    print('Please set socket size with the -z flag.')
    sys.exit(1)
if args.t == None:
    print('Please set hastag with the -t flag.')
    sys.exit(1)

print(args)

print('Finished')