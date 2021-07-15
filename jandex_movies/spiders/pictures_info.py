import scrapy
from scrapy.http import Response
from PIL import Image
from io import BytesIO

class Url:
    def __new__(cls, url) -> str:
        if 'http' not in url:
            url = f"https:{url}"
        return url

class PicturesSpider(scrapy.Spider):
    name = "pictures"

    def start_requests(self):
        url = "https://www.kinopoisk.ru"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for src in response.css('img::attr(src)').getall():
            if 'data:image' in src:
                continue
            yield scrapy.Request(url=response.urljoin(src), callback=self.get_img_details)

    def get_img_details(self, response: Response) -> dict:
        headers = response.headers
        name = response.url.split('/')[-2]
        try:
            type_: str = headers.get('content-type').decode('utf8')
        except:
            type_ = None
        try:
            size = round(int(headers.get('content-length').decode('utf8'))/1024, 2)
        except:
            size = None
        try:
            width, height = Image.open(BytesIO(response.body)).size
        except:
            width, height = None, None
        yield {
            'name': name,
            'dimentions': f"{width}x{height}" if width else None,
            'size': size,
            'url': response.url,
            'isWebp': 'webp' in type_ if type_ else None,
        }

if __name__ == '__main__':
    pass