#!/usr/bin/env python3
import json
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://verokone.hs.fi/rest/query"
DEFAULT_QUERY = {
    "county": "",
    "gender": "",
    "taxyear": "2024",
    "age": "",
    "orderby": "gross_income",
    "brand": "is",
    "offset": "0",
    "limit": "100",
}


def read_names(file_path: Path) -> list[str]:
    """Read names from file, ignoring empty lines and stripping whitespace."""
    if not file_path.exists():
        raise FileNotFoundError(f"Names file not found: {file_path}")
    return [line.strip() for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ensure_cache_dir(cache_dir: Path) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)


def safe_cache_name(name: str) -> str:
    sanitized = name.replace("/", "_").replace("\\", "_").strip()
    return sanitized or "unnamed"


def build_query_url(name: str) -> str:
    params = DEFAULT_QUERY.copy()
    params["name"] = name
    return f"{BASE_URL}?{urlencode(params)}"


def fetch_remote_tax_info(name: str) -> Any:
    url = build_query_url(name)
    req = Request(
        url,
        headers={
            "User-Agent": "verokone-cli/0.1",
            "Accept": "application/json",
        },
    )
    with urlopen(req) as response:  # type: ignore[arg-type]
        data = response.read().decode("utf-8")
    return json.loads(data)


def load_tax_info(name: str, cache_dir: Path) -> Any:
    ensure_cache_dir(cache_dir)
    cache_file = cache_dir / f"{safe_cache_name(name)}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))

    try:
        tax_info = fetch_remote_tax_info(name)
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"Failed to fetch data for '{name}': {exc}") from exc

    cache_file.write_text(json.dumps(tax_info, ensure_ascii=False, indent=2), encoding="utf-8")
    return tax_info


def format_tax_summary(name: str, tax_info: Any) -> str:
    if isinstance(tax_info, dict):
        results = tax_info.get("results")
        if isinstance(results, list):
            if not results:
                return f"{name}: no data"
            formattedResults = "\n  " + "\n  ".join([f"{r['name']}({r['birthYear']},{r['lastCounty']})={r['taxYears']['2024']['totalIncome']:.0f}EUR" for r in results])
            return f"{name} {tax_info['count']}: {formattedResults}"
        return f"{name}: {json.dumps(tax_info, ensure_ascii=False)}"
    return f"{name}: {tax_info}"


def main() -> None:
    names_file = Path("names.txt")
    cache_dir = Path("cache")
    for name in read_names(names_file):
        try:
            tax_info = load_tax_info(name, cache_dir)
        except Exception as exc:  # pragma: no cover - best effort logging
            print(str(exc), file=sys.stderr)
            continue
        print(format_tax_summary(name, tax_info))


if __name__ == "__main__":
    main()
