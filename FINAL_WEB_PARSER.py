import os
import newspaper
import csv

def get_news_articles(source_urls):
    articles = []

    for source_url in source_urls:
        try:
            source = newspaper.build(source_url, memoize_articles=False)
        except Exception as e:
            print(f"Error accessing {source_url}: {str(e)}")
            continue

        for article in source.articles:
            try:
                article.download()
                article.parse()
            except Exception as e:
                print(f"Error downloading/parsing article from {source_url}: {str(e)}")
                continue
            
            if hasattr(article, 'text') and hasattr(article, 'title'):
                articles.append({
                    'Title': article.title,
                    'Description': article.text,
                })

    return articles

def save_to_csv(articles, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(articles)

def main():
    source_urls = input("Enter the URLs of the news sources (comma-separated, e.g., 'https://www.example1.com,https://www.example2.com'): ").split(',')
    folder_path = '/Desktop/Code/TY CCNLP Project'
    csv_file_path = os.path.join(folder_path, "trial_news.csv")

    articles = get_news_articles(source_urls)

    if articles:
        for i, article in enumerate(articles, start=1):
            print(f"\nArticle {i}:")
            print(f"Title: {article['Title']}")
            print(f"Description: {article['Description']}")

        save_to_csv(articles, csv_file_path)
        print(f"\n{len(articles)} articles saved to '{csv_file_path}'")
    else:
        print(f"No articles found from the provided sources")

if __name__ == "__main__":
    main()
