#!/usr/bin/env python
import argparse
import sqlitedict


DATABASE_PATH = 'articles.sqlite'


def check_article(article):
    if article.endswith('.pdf'):
        article = article[:-4]

    with sqlitedict.SqliteDict(DATABASE_PATH) as dataset:
        is_read = dataset.get(article, False)

    return is_read


def add_article(article):
    if article.endswith('.pdf'):
        article = article[:-4]

    with sqlitedict.SqliteDict(DATABASE_PATH, autocommit=True) as dataset:
        dataset.setdefault(article, True)

    return True


def create_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('check',
                        type=str,
                        nargs='*',
                        help='check if article has already been read')

    parser.add_argument('-a',
                        '--add',
                        type=str,
                        help='mark an article as read')

    return parser


def check_args(user_args):
    if user_args['check']:
        article = user_args['check'][0]
        is_read = check_article(article)
        print(is_read)
    elif user_args['add']:
        article = user_args['add']
        is_added = add_article(article)

        if is_added:
            print('Article {} marked as read'.format(article))


def main():
    parser = create_argument_parser()
    user_args = vars(parser.parse_args())

    check_args(user_args)


if __name__ == '__main__':
    main()
