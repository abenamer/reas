#!/usr/bin/env python3
"""Check the REAS documentation profile. This is not an STE language checker.

Parse CommonMark links, images, headings, and HTML href/src/id attributes.
Resolve heading fragments with GitHub-style slugs. Do not fetch external URLs.
Check rule declarations in ATX or Setext headings throughout the repository.
In Engineering Standard concepts, check the rule shape (Intent, Enforcement,
Scope, Rules, optional Allowances, Verification) and the Quality test section.
Check that no document outside the exempt list uses a retired term from the
terminology table. Report concepts whose `updated` date is older than the
freshness threshold for their type as warnings, not errors.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
import yaml

RULE = re.compile(r"^(REAS-[A-Z]+-\d{3})(?=$|[\s:])")
RULE_TYPE = "Engineering Standard"
RULE_SECTIONS = ("Intent", "Enforcement", "Scope", "Rules", "Verification")
OPTIONAL_RULE_SECTION = "Allowances"
TRAILING_OPTIONAL_SECTION = "Limits"
ENFORCEMENT_VALUES = ("Required.", "Advisory.")
QUALITY_TEST = "Quality test"
TERMINOLOGY = "standard/terminology.md"
RETIRED_TERMS_HEADING = "## Retired terms"
# Documents that quote retired terms on purpose: the table that retires them,
# the identifier history, the changelog, and the language-review record.
RETIRED_TERM_EXEMPT = frozenset({
    TERMINOLOGY, "standard/rule-identifiers.md", "CHANGELOG.md", "standard/ste-review.md",
})
# Freshness threshold in days by concept type (REAS-DOC-002). Other types use
# FRESHNESS_DEFAULT_DAYS. A stale concept is a warning, not an error.
FRESHNESS_DAYS = {"Audit Report": 90, "Review Procedure": 180, "Technical Reference": 180}
FRESHNESS_DEFAULT_DAYS = 365
ACTOR = re.compile(r"^(?:human:[^\s]+|process:[^\s]+|[^\s/]+/[^\s/]+)$")
MARKDOWN = MarkdownIt("commonmark")


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of silently using the last value."""


def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise yaml.constructor.ConstructorError(
                None, None, f"Duplicate YAML key: {key}", key_node.start_mark
            )
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, text, None
    match = re.search(r"\n---[ \t]*(?:\n|$)", text[4:])
    if match is None:
        return None, text, "Unclosed YAML frontmatter"
    raw = text[4:][:match.start()]
    body = text[4:][match.end():]
    try:
        metadata = yaml.load(raw, Loader=UniqueKeyLoader)
    except (yaml.YAMLError, TypeError) as exc:
        return None, text, f"Invalid YAML: {exc}"
    if not isinstance(metadata, dict):
        return None, text, "Frontmatter must be a mapping"
    return metadata, body, None


class HTMLReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value is None:
                continue
            if name in {"href", "src"}:
                self.links.append(value)
            if name == "id" or (tag == "a" and name == "name"):
                self.anchors.add(value)

    handle_startendtag = handle_starttag


@dataclass
class Section:
    level: int
    text: str
    body: str


@dataclass
class Document:
    body: str
    headings: list[tuple[int, str]]
    links: list[str]
    anchors: set[str]
    sections: list[Section]
    plain: str


def parse_document(body: str) -> Document:
    tokens = MARKDOWN.parse(body)
    headings = []
    links = []
    anchors = set()
    used_slugs = set()
    html = HTMLReferences()
    sections: list[Section] = []
    section_bodies: list[list[str]] = []
    plain: list[str] = []

    def read_inline(children):
        for child in children or []:
            if child.type == "link_open":
                links.append(child.attrGet("href") or "")
            elif child.type == "image":
                links.append(child.attrGet("src") or "")
            elif child.type == "html_inline":
                html.feed(child.content)
            read_inline(child.children)

    def inline_text(children, with_code: bool) -> str:
        kinds = {"text", "code_inline"} if with_code else {"text"}
        parts = []
        for child in children or []:
            if child.type in kinds:
                parts.append(child.content)
            parts.append(inline_text(child.children, with_code))
        return "".join(parts)

    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            inline = tokens[index + 1]
            text = "".join(
                child.content for child in inline.children or []
                if child.type in {"text", "code_inline", "image"}
            )
            headings.append((int(token.tag[1:]), text))
            sections.append(Section(int(token.tag[1:]), text, ""))
            section_bodies.append([])
            plain.append(inline_text(inline.children, with_code=False))
            base = "".join(
                char for char in text.lower()
                if char in "-_ " or unicodedata.category(char)[0] not in "PSZC"
            ).replace(" ", "-")
            slug = base
            suffix = 0
            while slug in used_slugs:
                suffix += 1
                slug = f"{base}-{suffix}"
            used_slugs.add(slug)
            anchors.add(slug)
        elif token.type == "html_block":
            html.feed(token.content)
        if token.type == "inline":
            read_inline(token.children)
            if tokens[index - 1].type != "heading_open":
                plain.append(inline_text(token.children, with_code=False))
                if section_bodies:
                    section_bodies[-1].append(inline_text(token.children, with_code=True))
    links.extend(html.links)
    anchors.update(html.anchors)
    for section, parts in zip(sections, section_bodies):
        section.body = "\n".join(parts)
    return Document(body, headings, links, anchors, sections, re.sub(r"\s+", " ", " ".join(plain)))


def rule_shape_errors(document: Document) -> list[str]:
    """Check each rule in an Engineering Standard concept for the REAS rule shape."""
    errors = []
    sections = document.sections
    for index, section in enumerate(sections):
        match = RULE.match(section.text)
        if match is None:
            continue
        rule = match.group(1)
        if section.level != 2:
            errors.append(f"{rule}: Rule heading must be level 2")
            continue
        children = []
        for later in sections[index + 1:]:
            if later.level <= 2:
                break
            if later.level == 3:
                children.append(later)
        names = [child.text for child in children]
        expected = list(RULE_SECTIONS[:4])
        if OPTIONAL_RULE_SECTION in names:
            expected.append(OPTIONAL_RULE_SECTION)
        expected.append(RULE_SECTIONS[4])
        if TRAILING_OPTIONAL_SECTION in names:
            expected.append(TRAILING_OPTIONAL_SECTION)
        if names != expected:
            errors.append(
                f"{rule}: Sections must be Intent, Enforcement, Scope, Rules, "
                f"[Allowances], Verification, [Limits]; found {', '.join(names) or 'none'}"
            )
            continue
        for child in children:
            if not child.body.strip():
                errors.append(f"{rule}: {child.text} section is empty")
            elif child.text == "Enforcement" and child.body.strip() not in ENFORCEMENT_VALUES:
                errors.append(f"{rule}: Enforcement must be 'Required.' or 'Advisory.'")
    quality = [s for s in sections if s.level == 2 and s.text == QUALITY_TEST]
    if not quality:
        errors.append(f"Missing '{QUALITY_TEST}' section")
    elif not quality[0].body.strip():
        errors.append(f"'{QUALITY_TEST}' section is empty")
    return errors


def retired_terms(text: str) -> list[tuple[str, str]] | None:
    """Read the Retired terms table from the terminology concept.

    Return None when the section is absent, else the (term, replacement) rows.
    """
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == RETIRED_TERMS_HEADING)
    except StopIteration:
        return None
    rows = []
    table_lines = []
    for line in lines[start + 1:]:
        if line.startswith("#"):
            break
        if line.lstrip().startswith("|"):
            table_lines.append(line)
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0]:
            rows.append((cells[0], cells[1]))
    return rows


def parse_updated(value) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def freshness_warnings(root: Path, today: date | None = None) -> list[str]:
    """Report concepts whose `updated` date is older than the threshold for their type."""
    today = today or date.today()
    root = root.resolve()
    bundle = root / "standard"
    warnings = []
    if not bundle.is_dir():
        return warnings
    for path in sorted(bundle.rglob("*.md")):
        if path.name in {"index.md", "log.md"}:
            continue
        try:
            meta, _, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        except (UnicodeError, OSError):
            continue
        if not isinstance(meta, dict) or "updated" not in meta:
            continue
        updated = parse_updated(meta["updated"])
        if updated is None or updated > today:
            continue
        limit = FRESHNESS_DAYS.get(meta.get("type"), FRESHNESS_DEFAULT_DAYS)
        age = (today - updated).days
        if age > limit:
            rel = path.relative_to(root).as_posix()
            warnings.append(f"{rel}: updated {updated} is {age} days old; the limit for {meta.get('type')} is {limit}")
    return warnings


def valid_timestamp(value) -> bool:
    if isinstance(value, str):
        if "T" not in value:
            return False
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return False
    return isinstance(value, datetime) and value.utcoffset() is not None


def metadata_errors(meta: dict) -> list[str]:
    errors = []
    events = []
    if "generated" in meta:
        events.append(("generated", meta["generated"]))
    verified = meta.get("verified", [])
    if isinstance(verified, dict):
        verified = [verified]
    if not isinstance(verified, list):
        errors.append("verified must be a mapping or a list")
    else:
        events.extend(("verified", event) for event in verified)
    for field, event in events:
        if not isinstance(event, dict):
            errors.append(f"{field} must be a mapping")
            continue
        actor = event.get("by")
        if not isinstance(actor, str) or not ACTOR.fullmatch(actor):
            errors.append(f"Invalid {field}.by")
        if not valid_timestamp(event.get("at")):
            errors.append(f"Invalid {field}.at: use a datetime with a UTC offset")
    sources = meta.get("sources", [])
    if not isinstance(sources, list) or any(
        not isinstance(source, dict)
        or not isinstance(source.get("resource"), str)
        or not source["resource"].strip()
        for source in sources
    ):
        errors.append("Sources must include a resource")
    return errors


def validate(root: Path, today: date | None = None) -> list[str]:
    today = today or date.today()
    root = root.resolve()
    bundle = root / "standard"
    if not bundle.is_dir():
        return ["The standard/ OKF bundle is missing"]
    errors = []
    documents = {}
    concepts = set()
    seen = {}
    graph = {}
    terminology_text = None
    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", "target", ".venv"} for part in path.relative_to(root).parts):
            continue
        rel = path.relative_to(root).as_posix()
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as exc:
            errors.append(f"{rel}: Cannot read: {exc}")
            continue
        meta, body, err = split_frontmatter(content)
        if err:
            errors.append(f"{rel}: {err}")
        document = parse_document(body)
        documents[path] = document
        graph[path] = set()
        if path.is_relative_to(bundle):
            if path.name == "index.md":
                if path.parent == bundle:
                    if meta is None or set(meta) != {"okf_version"} or str(meta.get("okf_version")) != "0.2":
                        errors.append(f"{rel}: Bundle index must contain only okf_version: '0.2'")
                elif meta is not None:
                    errors.append(f"{rel}: Nested index must not contain frontmatter")
            elif path.name == "log.md":
                if meta is not None:
                    errors.append(f"{rel}: Log must not contain frontmatter")
                for level, heading in document.headings:
                    if level == 2:
                        try:
                            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", heading):
                                raise ValueError
                            date.fromisoformat(heading)
                        except ValueError:
                            errors.append(f"{rel}: Log date must use YYYY-MM-DD: {heading}")
            else:
                concepts.add(path)
                if not isinstance(meta, dict) or not isinstance(meta.get("type"), str) or not meta["type"].strip():
                    errors.append(f"{rel}: Concept requires a non-empty type")
                if meta:
                    errors.extend(f"{rel}: {error}" for error in metadata_errors(meta))
                    if "updated" in meta:
                        updated = parse_updated(meta["updated"])
                        if updated is None:
                            errors.append(f"{rel}: Invalid updated: use YYYY-MM-DD")
                        elif updated > today:
                            errors.append(f"{rel}: updated {updated} is in the future")
                    if meta.get("type") == RULE_TYPE:
                        errors.extend(f"{rel}: {error}" for error in rule_shape_errors(document))
                if not body.strip():
                    errors.append(f"{rel}: Empty concept")
                if rel == TERMINOLOGY:
                    terminology_text = body
        for _, heading in document.headings:
            if not heading.startswith("REAS-"):
                continue
            match = RULE.match(heading)
            if match is None:
                errors.append(f"{rel}: Invalid rule declaration: {heading}")
                continue
            rule = match.group(1)
            if rule in seen:
                errors.append(f"{rel}: Duplicate {rule} also in {seen[rule]}")
            seen[rule] = rel
    for path, document in documents.items():
        rel = path.relative_to(root).as_posix()
        for uri in document.links:
            try:
                parsed = urlsplit(uri)
            except ValueError:
                errors.append(f"{rel}: Invalid link URI: {uri}")
                continue
            if parsed.scheme or parsed.netloc:
                continue
            target = unquote(parsed.path)
            if not target:
                actual = path
            elif target.startswith("/"):
                base = bundle if path.is_relative_to(bundle) else root
                actual = (base / target.lstrip("/")).resolve()
            else:
                actual = (path.parent / target).resolve()
            if not actual.is_relative_to(root):
                errors.append(f"{rel}: Link leaves repository: {uri}")
                continue
            if not actual.exists():
                errors.append(f"{rel}: Broken local link: {uri}")
                continue
            if actual.is_dir():
                actual = next(
                    (candidate for name in ("index.md", "README.md")
                     if (candidate := actual / name) in documents), actual
                )
            if actual in documents:
                graph[path].add(actual)
            if parsed.fragment:
                fragment = unquote(parsed.fragment)
                if actual not in documents or fragment not in documents[actual].anchors:
                    errors.append(f"{rel}: Broken local fragment: {uri}")
    index = bundle / "index.md"
    if not index.is_file():
        errors.append("standard/index.md: Bundle index is missing")
    else:
        reachable = set()
        pending = [index]
        while pending:
            path = pending.pop()
            if path in reachable or not path.is_relative_to(bundle):
                continue
            reachable.add(path)
            pending.extend(graph.get(path, set()) - reachable)
        for path in sorted(concepts - reachable):
            errors.append(f"{path.relative_to(root)}: Concept is not reachable from standard/index.md")
    if terminology_text is not None:
        retired = retired_terms(terminology_text)
        if retired is None:
            errors.append(f"{TERMINOLOGY}: Retired terms section is missing")
        elif not retired:
            errors.append(f"{TERMINOLOGY}: Retired terms table is empty")
        else:
            for path, document in documents.items():
                rel = path.relative_to(root).as_posix()
                if rel in RETIRED_TERM_EXEMPT:
                    continue
                plain = document.plain.lower()
                for term, replacement in retired:
                    if term.lower() in plain:
                        errors.append(f"{rel}: Retired term '{term}'; use {replacement}")
    if not seen:
        errors.append("No REAS rule IDs found")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--strict-freshness", action="store_true",
                        help="treat a stale concept as an error instead of a warning")
    args = parser.parse_args()
    errors = validate(args.root)
    warnings = freshness_warnings(args.root)
    for warning in warnings:
        print("WARN:", warning)
    if args.strict_freshness:
        errors.extend(warnings)
    for error in errors:
        print("ERROR:", error)
    if errors:
        print(f"FAIL: {len(errors)} errors")
        return 1
    print("PASS: REAS frontmatter profile, index reachability, rule declarations and shape, "
          "quality tests, retired terms, local links and fragments")
    print("NOT CHECKED: full OKF conformance, STE language, external URLs, technical accuracy, historical ID reuse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
