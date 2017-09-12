#!/usr/bin/env python
import argparse
import glob
import os
import sqlitedict


DATABASE_PATH = 'articles.sqlite'


def format_article_name(article):
    if article.endswith('.pdf'):
        article = article[:-4]

    return article


def perform_check(article):
    if os.path.isfile(article):
        is_read = check_article(article)
        print(is_read)
    elif os.path.isdir(article):
        return check_dir(article)


def check_dir(article_dir):
    pdf_files = glob.glob(article_dir + '*.pdf')
    output_str = "Articles in directory:\n\n"
    for article in pdf_files:
        is_read = check_article(article.split('/')[1])
        output_str += '{}...........{}\n'.format(article, is_read)

    print(output_str)


def check_article(article):
    article = format_article_name(article)

    with sqlitedict.SqliteDict(DATABASE_PATH) as dataset:
        is_read = dataset.get(article, False)

    return is_read


def remove_article(article):
    article = format_article_name(article)

    is_read = check_article(article)
    if not is_read:
        return False

    with sqlitedict.SqliteDict(DATABASE_PATH) as dataset:
        dataset[article] = False

    return True


def add_article(article):
    article = format_article_name(article)

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

    parser.add_argument('-u',
                        '--unmark',
                        type=str,
                        help=('Remove article from dataset. The article will \
                               no longer be marked as read'))

    return parser


def check_args(user_args):
    if user_args['check']:
        article = user_args['check'][0]
        perform_check(article)
    elif user_args['add']:
        article = user_args['add']
        is_added = add_article(article)

        if is_added:
            print('Article {} marked as read'.format(article))
    elif user_args['unmark']:
        article = user_args['unmark']
        is_removed = remove_article(article)

        if not is_removed:
            print('Article {} was never marked as read'.format(article))
        else:
            print('Article {} successfully unmarked!'.format(article))


def main():
    parser = create_argument_parser()
    user_args = vars(parser.parse_args())

    user_vars = [bool(value) for key, value in user_args.items()]

    if True not in user_vars:
        parser.print_help()
        return

    check_args(user_args)


if __name__ == '__main__':
    main()
