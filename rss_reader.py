from typing import List, Optional, Sequence
import requests
from bs4 import BeautifulSoup


def rss_parser(
        xml: str,
        limit: Optional[int] = None,
):
    """
    RSS parser.

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. if None, returns all news.

    Returns:
        List of strings.
        Which then can be printed to stdout or written to file as a separate lines.

    Examples:
        #>>> xml = '<rss><channel><title>Some RSS Channel</title><link>https://some.rss.com</link><description>Some RSS Channel</description></channel></rss>'
        #>>> rss_parser(xml)
        ["Feed: Some RSS Channel",
        "Link: https://some.rss.com"]
        #>>> print("\\n".join(rss_parser(xmls)))
        Feed: Some RSS Channel
        Link: https://some.rss.com
    """
    # RSS response from server
    rss_raw_text = requests.get(xml).text

    # Main content
    main_soup = BeautifulSoup(rss_raw_text, features="xml")

    # HEADER PART
    # Header only - items deleted
    head_soup = BeautifulSoup(rss_raw_text, features="xml")
    for i in range(0, len(head_soup.find_all('item'))):
        i_tag = head_soup.find('item')
        i_tag.decompose()

    # Building header attributes output
    ch_title = (f"Feed: {head_soup.find('title').text}\n") if head_soup.find('title') is not None else (f"\r")
    ch_link = (f"Link: {head_soup.find('link').text}\n") if head_soup.find('link') is not None else (f"\r")
    ch_lastBuildDate = (f"Last Build Date: {head_soup.find('lastBuildDate').text}\n") if head_soup.find(
        'lastBuildDate') is not None else (f"\r")
    ch_pubDate = (f"Publication Date: {head_soup.find('pubDate').text}\n") if head_soup.find(
        'pubDate') is not None else (f"\r")
    ch_language = (f"Language: {head_soup.find('language').text}\n") if head_soup.find('language') is not None else (
        f"\r")
    ch_managinEditor = (f"Managing Editor: {head_soup.find('managinEditor').text}\n") if head_soup.find(
        'managinEditor') is not None else (f"\r")
    ch_description = (f"Description: {head_soup.find('description').text}\n") if head_soup.find(
        'description') is not None else (f"\r")

    # Extracting all the categories of the header dependently on the number of categories
    ch_category = (f"Categories: ")
    if len(head_soup.find_all('category')) > 1:
        header_categories = head_soup.find_all('category')
        for header_category in header_categories:
            ch_category += (f"{header_category.text}, ")
    elif len(head_soup.find_all('category')) == 1:
        ch_category = (f"{head_soup.find('category').text}")
    else:
        ch_category = (f"\r")

    # Writing header attributes to output string of every item
    feed_header_output = (f"{ch_title}"
                          f"{ch_link}"
                          f"{ch_lastBuildDate}"
                          f"{ch_pubDate}"
                          f"{ch_language}"
                          f"{ch_category}"
                          f"{ch_managinEditor}"
                          f"{ch_description}"
                          )

    # ITEMS PART
    items = main_soup.find_all('item')
    items_output = (f"{''}")
    limit_count = 0
    if limit == None:
        limit = len(items)

    # Building items attributes output
    for i in items:
        if limit_count < limit:
            it_title = (f"Title: {i.find('title').text}\n") if i.find('title') is not None else (f"\r")
            it_author = (f"Author: {i.find('author').text}\n") if i.find('author') is not None else (f"\r")
            it_pubDate = (f"Publication Date: {i.find('pubDate').text}\n") if i.find(
                'pubDate') is not None else (f"\r")
            it_link = (f"Link: {i.find('link').text}\n") if i.find('link') is not None else (f"\r")
            it_description = (f"{i.find('description').text}\n") if i.find(
                'description') is not None else (f"\r")

            # Extracting all the categories of every item dependently on the number of categories
            it_category = (f"Categories: ")
            if len(i.find_all('category')) > 1:
                item_categories = i.find_all('category')
                for category in item_categories:
                    it_category += (f"{category.text}, ")
            elif len(i.find_all('category')) == 1:
                it_category += (f"{i.find('category').text}")
            else:
                it_category = (f"\r")

            # Writing item attributes to output string of every item
            item_out = (f"{it_title}"
                        f"{it_author}"
                        f"{it_pubDate}"
                        f"{it_link}"
                        f"{it_category}\n\n"
                        f"{it_description}"
                        f"\n\n")

            # Appeding item output string to all items output string
            items_output += (f"{item_out}")
            limit_count += 1

    return (f"{feed_header_output}\n"
            f"{items_output}")
