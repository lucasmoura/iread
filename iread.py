#!/usr/bin/env python
import argparse
import glob
import os
import sqlite3


DATABASE_PATH = '/home/lucas/.iread/articles'


def format_article_name(article):
    if article.endswith('.pdf'):
        article = article[:-4]

    return article


def perform_check(dataset, article):
    if os.path.isfile(article):
        is_read = check_article(dataset, article)
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


def check_article(dataset, article):
    article = format_article_name(article)

    cursor = dataset.cursor()
    cursor.execute(
            '''
            SELECT name
            FROM articles
            WHERE name = ?
            ''', (article,)
    )

    is_read = True

    if len(cursor.fetchall()) == 0:
        is_read = False

    return is_read


def remove_article(dataset, article):
    article = format_article_name(article)

    is_read = check_article(dataset, article)
    if not is_read:
        return False

    cursor = dataset.cursor()
    cursor.execute(
        '''DELETE
           FROM articles
           WHERE name = ? ''', (article,))
    dataset.commit()

    return True


def add_article(dataset, article):
    article = format_article_name(article)

    cursor = dataset.cursor()
    cursor.execute(
            '''
            INSERT INTO articles(name)
            VALUES(:name)
            ''', {'name': article}
    )
    dataset.commit()

    return True


def create_dataset():
    dataset = sqlite3.connect(DATABASE_PATH)
    cursor = dataset.cursor()

    cursor.execute(
        '''
        CREATE TABLE articles(id INTEGER PRIMARY_KEY, name TEXT)
        '''
    )

    dataset.commit()
    return dataset


def check_dataset():
    if not os.path.exists(DATABASE_PATH):
        dataset = create_dataset()
    else:
        dataset = sqlite3.connect(DATABASE_PATH)

    return dataset


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

    parser.add_argument('-d',
                        '--delete',
                        type=str,
                        help=('Remove article from dataset. The article will \
                               no longer be marked as read'))

    return parser


def check_args(user_args, dataset):
    if user_args['check']:
        article = user_args['check'][0]
        perform_check(dataset, article)
    elif user_args['add']:
        article = user_args['add']
        is_added = add_article(dataset, article)

        if is_added:
            print('Article {} marked as read'.format(article))
    elif user_args['delete']:
        article = user_args['delete']
        is_removed = remove_article(dataset, article)

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

    dataset = check_dataset()
    check_args(user_args, dataset)
    dataset.close()


if __name__ == '__main__':
    main()
