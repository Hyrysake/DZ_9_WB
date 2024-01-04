import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com']

    def __init__(self):
        super(QuotesSpider, self).__init__()
        self.quotes_data = []
        self.authors_data = {}

    def parse(self, response):
        # Отримання інформації про цитати
        quotes = response.css('div.quote')
        for quote in quotes:
            quote_text = quote.css('span.text::text').get().strip()
            author_name = quote.css('small.author::text').get().strip()
            tags = quote.css('div.tags a.tag::text').getall()

            self.quotes_data.append({
                "tags": tags,
                "author": author_name,
                "quote": quote_text
            })

            # Отримання посилання на автора та перехід на його сторінку
            author_url = quote.css('small.author ~ a::attr(href)').get()
            yield response.follow(author_url, callback=self.parse_author)

        # Отримання посилання на наступну сторінку з цитатами
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            self.save_data()

    def parse_author(self, response):
        # Отримання інформації про автора
        author_name = response.css('h3.author-title::text').get().strip()
        born_info = response.css('span.author-born-date::text').get().strip()
        born_location = response.css('span.author-born-location::text').get().strip()
        description = response.css('div.author-description::text').get().strip()

        self.authors_data[author_name] = {
            "fullname": author_name,
            "born_date": born_info,
            "born_location": born_location,
            "description": description
        }

    def save_data(self):
        # Збереження інформації у файли
        with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
            json.dump(self.quotes_data, quotes_file, ensure_ascii=False, indent=2)

        with open('authors.json', 'w', encoding='utf-8') as authors_file:
            authors_list = list(self.authors_data.values())
            json.dump(authors_list, authors_file, ensure_ascii=False, indent=2)
