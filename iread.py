#!/usr/bin/env python
import argparse


def create_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('check',
                        type=str,
                        help='check if article has already been read')

    parser.add_argument('-a',
                        '--add',
                        type=str,
                        help='mark an article as read')

    return parser


def main():
    parser = create_argument_parser()

    user_args = parser.parse_args()
    print(user_args)


if __name__ == '__main__':
    main()
