import sched
from pathlib import Path

import scrapy
import time
import json
from scrapy.crawler import CrawlerProcess

from scrapy.utils.project import get_project_settings

BASE_DIR = Path(__file__).parent.parent
POSTS_FOLDER = BASE_DIR / 'data_processing/Posts'
OVERSIZE_FOLDER = BASE_DIR / 'data_processing/oversize'
MAX_CONTENT_SIZE = 4000


def save_oversize_json(data):
    if len(data["content"]) > MAX_CONTENT_SIZE:
        filename = OVERSIZE_FOLDER / f"{int(time.time())}.json"
        with filename.open('w') as f:
            json.dump([data], f)


class MySpider(scrapy.Spider):
    name = 'myspider1'

    def start_requests(self):
        scraped_urls = set()
        for filename in POSTS_FOLDER.glob('*.json'):
            with filename.open() as f:
                scraped_data = json.load(f)
                scraped_urls.update(article['url'] for article in scraped_data)

                # Read URLs from Oversize folder
                for filename in OVERSIZE_FOLDER.glob('*.json'):
                    with filename.open() as f:
                        scraped_data = json.load(f)
                        scraped_urls.update(article['url'] for article in scraped_data)

        yield scrapy.Request('https://www.coindesk.com/', meta={'scraped_urls': scraped_urls})

    def parse(self, response, **kwargs):
        scraped_urls = response.meta['scraped_urls']

        article_blocks = response.css(
            '#fusion-app > div.high-impact-vertstyles__StickyHighImpactLayoutWrapperStyled-cuy9q8-1.hPdtnJ > div > div > main > div > section:nth-child(2) > div > div.live-wire > div > div')

        for block in article_blocks:
            title = block.css(
                'div.live-wirestyles__Body-sc-1xrlfqv-2.cGUTRt > div.live-wirestyles__Title-sc-1xrlfqv-3.fwiqHn::text').get()
            href = block.css('a::attr(href)').get()

            if href not in scraped_urls:
                scraped_urls.add(href)
                try:
                    yield response.follow(url=href, callback=self.parse_article,
                                          meta={'title': title, 'scraped_urls': scraped_urls})
                except ValueError:
                    pass

    def parse_article(self, response):
        title = response.meta['title']
        content = response.css(
            "#fusion-app > div.high-impact-vertstyles__StickyHighImpactLayoutWrapperStyled-cuy9q8-1.hPdtnJ > div > main > article > div.containerstyles__StyledContainer-sc-292snj-0.KqMZq > div > section > div.main-body-grid.false > div.at-content-wrapper > div.contentstyle__StyledWrapper-g5cdrh-0.jsJHBz *::text").extract()

        content_text = ' '.join(content).strip()

        data = {
            "content": content_text,
            "url": response.url,
            "timestamp": int(time.time()),
        }
        if len(data["content"]) > MAX_CONTENT_SIZE:
            save_oversize_json(data)
        else:
            filename = POSTS_FOLDER / f"{int(time.time())}.json"
            with filename.open('w') as f:
                json.dump([data], f)

        yield data


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(MySpider)
    process.start()
    process.stop()


if __name__ == "__main__":
    main()
