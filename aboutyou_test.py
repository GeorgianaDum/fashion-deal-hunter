
import json
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

URL = (
    "https://www.aboutyou.ro/p/jdy/"
    "geaca-de-primavara-toamna-jdyraya-29565109"
)

class JSONInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capturing = False
        self.parts = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            attributes = dict(attrs)
            self.capturing = (
                attributes.get("type", "").lower()
                == "application/json"
            )
            self.parts = []

    def handle_data(self, data):
        if self.capturing:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.capturing:
            self.scripts.append("".join(self.parts))
            self.capturing = False


print("ABOUT YOU - diagnostic JSON")

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

    inspector = JSONInspector()
    inspector.feed(html)

    print("JSON scripts found:", len(inspector.scripts))

    for index, raw in enumerate(inspector.scripts, start=1):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            print(f"Script {index}: invalid JSON")
            continue

        print(f"\nScript {index}")
        print("Root type:", type(data).__name__)

        if isinstance(data, dict):
            print("Top-level keys:", list(data.keys())[:15])

        elif isinstance(data, list):
            print("List length:", len(data))

        print(
            "Contains product ID:",
            "29565109" in raw
        )
        print(
            "Contains product name:",
            "JDYRAYA" in raw.upper()
        )

    print("\nDiagnostic only.")
    print("No prices extracted.")
    print("products.json unchanged.")

except (HTTPError, URLError, TimeoutError) as error:
    print("Access failed:", type(error).__name__)
