"""Diagnostic read-only for a single public ABOUT YOU product page.

Does not scrape a catalog, bypass protections, or modify products.json.
"""
import json
import re
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlparse

URL = 'https://www.aboutyou.ro/p/jdy/geaca-de-primavara-toamna-jdyraya-29565109'

class ProductDataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_json_ld = False
        self.parts = []
        self.json_ld = []

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            attributes = dict(attrs)
            self.in_json_ld = attributes.get('type', '').lower() == 'application/ld+json'
            self.parts = []

    def handle_data(self, data):
        if self.in_json_ld:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_json_ld:
            self.json_ld.append(''.join(self.parts))
            self.in_json_ld = False


def find_products(obj):
    if isinstance(obj, dict):
        types = obj.get('@type', [])
        if isinstance(types, str):
            types = [types]
        if 'Product' in types:
            yield obj
        for value in obj.values():
            yield from find_products(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from find_products(value)


def main():
    assert urlparse(URL).hostname == 'www.aboutyou.ro'
    request = urllib.request.Request(URL, headers={
        'User-Agent': 'FashionDealHunterDiagnostic/1.0 (single-page read-only test)',
        'Accept': 'text/html,application/xhtml+xml',
    })
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            status = response.status
            final_url = response.geturl()
            content_type = response.headers.get('Content-Type', '')
            raw = response.read(2_000_000)
    except urllib.error.HTTPError as exc:
        print(f'HTTP status: {exc.code}. Site may restrict automated access.')
        return
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f'Network request failed: {type(exc).__name__}: {exc}')
        return

    print(f'HTTP status: {status}')
    print(f'Final domain: {urlparse(final_url).hostname}')
    print(f'Content type: {content_type}')
    if 'html' not in content_type.lower():
        print('Not HTML; no product extraction attempted.')
        return
    parser = ProductDataParser()
    parser.feed(raw.decode('utf-8', errors='replace'))
    print(f'JSON-LD blocks: {len(parser.json_ld)}')
    count = 0
    for block in parser.json_ld:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        for product in find_products(data):
            count += 1
            print('Product structured data found:')
            for key in ('name', 'sku', 'color'):
                if product.get(key):
                    print(f'  {key}: {str(product[key])[:200]}')
            offers = product.get('offers')
            if offers:
                print('  Offers field exists (requires validation before use).')
    print(f'Product JSON-LD objects: {count}')
    if not count:
        print('No usable Product JSON-LD detected. No prices inferred.')
    print('Diagnostic only. products.json unchanged.')

if __name__ == '__main__':
    main()
