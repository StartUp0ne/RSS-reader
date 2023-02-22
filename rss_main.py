import logging
import argparse
import sys
import os.path
import feedparser


source_url = r"https://blog.360totalsecurity.com/en/feed/"
result_dir = 'news'


def parse_rss(url: str):
    """
    Reads rss feed and extracts title, description, content tags \n
    :param url: RSS feed URL
    :return: List of dictionaries with keys: title, description, content
    """
    articles = feedparser.parse(url).entries
    news = []
    for article in articles:
        keys = article.keys()
        title = None
        content = None
        description = None
        if "title" in keys:
            title = article.title
        if 'description' in keys:
            description = article.description[0]
        if 'content' in keys:
            content = article.content[0]["value"]
        news.append({'title': title, 'description': description, 'content': content})
    return news


def write_rss_in_file(articles: list, folder: str):
    """
    Creates files and writes articles to them \n
    :param articles: List of dictionaries with keys: title, description, content
    :param folder: Path to the folder where the articles will be recorded
    :return: None
    """
    for article in articles:
        title, description, content = article.values()

        if not title:
            with open(f"{folder}/other_news.txt", 'a') as file_stream:
                print("Article", file=file_stream)
                if description:
                    print(description, file=file_stream)
                if content:
                    print(content, file=file_stream)
            continue

        filename = f"{folder}/{valid_filename(title)}"
        if title and not os.path.exists(filename):
            with open(filename, 'w', encoding="utf-8") as file_stream:
                if description:
                    print(description, file=file_stream)
                if content:
                    print(content, file=file_stream)


def valid_filename(filename: str):
    """
    Removes invalid characters from the string \n
    :param filename: file name without extension
    :return: correct file name
    """
    invalid_char = "<>:\"\\/|?*"
    if set(invalid_char).intersection(filename):
        for ch in invalid_char:
            filename = filename.replace(ch, '')

    return f"{filename}.txt"


def task_for_schedule():
    logging.info(f"Schedule started working, reads rss by url: {source_url}")
    write_rss_in_file(parse_rss(source_url), result_dir)
    logging.info(f"Process finished. Result files saved to the directory:  {result_dir}")


def main(options):
    logging.info("Start reading rss feeds...")
    write_rss_in_file(parse_rss(options.source), options.directory)
    logging.info(f"Process finished. Result files saved to the directory: {options.directory}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="RSS reader",
        description="This program reads rss feeds and writes the found articles "
                    "into separate files, the file name is the name of the article")
    parser.add_argument("-s", "--source", action="store",
                        help="RSS feed URL", default=source_url)
    parser.add_argument("-d", "--directory", action="store", default=result_dir,
                        help="Path to the folder where the articles will be recorded")
    parser.add_argument("--dry", action="store_true", default=False,
                        help="Flag of dry run. If True, use log level - DEBUG")
    parser.add_argument("-l", "--log", action="store",
                        help="File name of log file", )
    args = parser.parse_args()

    logging.basicConfig(filename=args.log, level=logging.INFO if not args.dry else logging.DEBUG,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')

    logging.info(f"RSS reader started with options: {args.__dict__}")

    try:
        main(args)
    except Exception as e:
        logging.exception(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
