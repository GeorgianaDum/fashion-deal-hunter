
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError

URL = (
    "https://www.aboutyou.ro/p/jdy/"
    "geaca-de-primavara-toamna-jdyraya-29565109"
)

class PageInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = []
        self.scripts = {}
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "title":
            self.in_title = True

        if tag == "meta":
            key = attrs.get("property") or attrs.get("name")
            value = attrs.get("content", "")
            if key and (
                key.startswith("og:")
                or key.startswith("product:")
                or key in ("description", "twitter:title")
            ):
                self.meta.append((key, value[:200]))

        if tag == "script":
            kind = attrs.get("type", "unspecified")
            self.scripts[kind] = self.scripts.get(kind, 0) + 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


print("ABOUT YOU - diagnostic HTML")

try:
    request = Request(
        URL,
        headers={
            "User-Agent": "FashionDealHunterDiagnostic/1.0"
        }
    )

    with urlopen(request, timeout=20) as response:
        html = response.read(2_000_000).decode(
            "utf-8", errors="replace"
        )
        print("HTTP status:", response.status)
        print("Final domain:", urlparse(response.url).hostname)
        print("HTML characters:", len(html))

    inspector = PageInspector()
    inspector.feed(html)

    print("Page title:", inspector.title.strip()[:200])

    print("\nPublic metadata:")
    for key, value in inspector.meta[:20]:
        print(f"  {key}: {value}")

    print("\nScript types:")
    for kind, count in inspector.scripts.items():
        print(f"  {kind}: {count}")

    print("\nProduct-related indicators:")
    for term in (
        "JDYRAYA", "29565109", "price",
        "availability", "application/ld+json"
    ):
        print(f"  {term}: {term.lower() in html.lower()}")

    print("\nDiagnostic only. No prices extracted.")
    print("products.json unchanged.")

except (HTTPError, URLError, TimeoutError) as error:
    print("Page access failed:", type(error).__name__)
    print("No product data collected.")
