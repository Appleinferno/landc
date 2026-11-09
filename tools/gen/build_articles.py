"""Build Lot Clearing Tips blog articles from content_articles.ARTICLES."""
import sys
from gen_article import render_article, article_word_count
from content_articles import ARTICLES

def main():
    wanted = set(sys.argv[1:])
    for p in ARTICLES:
        if wanted and p["slug"] not in wanted:
            continue
        out, html = render_article(p)
        print(f"{p['slug']}: ~{article_word_count(html)} words")

if __name__ == "__main__":
    main()
