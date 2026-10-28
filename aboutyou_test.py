
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser

URL = (
    "https://www.mangooutlet.com/ro/ro/p/femei/"
    "paltoane/geaca-parka-cu-buzunare-si-guler-inalt/"
    "77947938/35/00"
)

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.metadata = []
        self.json_ld = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            key = attrs.get("property") or attrs.get("name")
            if key and (
                key.startswith("og:")
                or key.startswith("product:")
                or key == "description"
            ):
                self.metadata.append(
                    (key, attrs.get("content", "")[:160])
                )
        if tag == "script":
            if attrs.get("type") == "application/ld+json":
                self.json_ld += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


print("MANGO OUTLET - diagnostic produs")

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
        print("Final URL:", response.url)

    inspector = Inspector()
    inspector.feed(html)

    print("HTML characters:", len(html))
    print("Page title:", inspector.title.strip()[:200])
    print("JSON-LD blocks:", inspector.json_ld)

    print("\nPublic metadata:")
    for key, value in inspector.metadata[:15]:
        print(key, ":", value)

    print("\nProduct indicators:")
    for term in (
        "77947938", "geacă parka",
        "price", "availability", "RON"
    ):
        print(term, ":", term.lower() in html.lower())

    print("\nDiagnostic only.")
    print("No prices extracted.")
    print("products.json unchanged.")

except (HTTPError, URLError, TimeoutError) as error:
    print("Access failed:", type(error).__name__)
