"""Behavioral regression tests for the documented REAS checker profile."""
from pathlib import Path
import tempfile
import unittest

from datetime import date

from scripts.check_docs import freshness_warnings, retired_terms, split_frontmatter, validate

REPO = Path(__file__).resolve().parents[1]

RULE_BODY = (
    '### Intent\n\nWhy.\n\n### Enforcement\n\nRequired.\n\n### Scope\n\nWhere.\n\n'
    '### Rules\n\nDo this.\n\n### Verification\n\n- Review question: how?\n'
)
STANDARD = (
    '---\ntype: Engineering Standard\nupdated: 2026-11-20\n---\n# Title\n\n'
    '## REAS-RUST-001: Rule\n\n' + RULE_BODY + '\n## Quality test\n\nCan it?\n'
)
TERMINOLOGY = (
    '---\ntype: Technical Reference\n---\n# Terms\n\n## Retired terms\n\n'
    '| Term | Use instead |\n| --- | --- |\n| old term | new term |\n'
)


class FixtureTests(unittest.TestCase):
    """Shared temporary-bundle helpers. Holds no tests of its own."""

    def fixture(self, files=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        contents = {
            'standard/index.md': '---\nokf_version: "0.2"\n---\n# Index\n[Rule](rule.md)\n',
            'standard/rule.md': '---\ntype: Rule\n---\n# REAS-RUST-001: Rule\n',
        }
        contents.update(files or {})
        for name, content in contents.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
        return root

    def append(self, root, content, name='standard/rule.md'):
        path = root / name
        path.write_text(path.read_text() + content)


class CheckDocsTests(FixtureTests):
    def test_valid_frontmatter(self):
        metadata, body, error = split_frontmatter('---\ntype: Rule\n---\nText')
        self.assertIsNone(error)
        self.assertEqual(metadata['type'], 'Rule')
        self.assertEqual(body, 'Text')

    def test_missing_frontmatter_is_reported_for_a_concept(self):
        root = self.fixture({'standard/rule.md': '# REAS-RUST-001\n'})
        self.assertTrue(any('Concept requires' in error for error in validate(root)))

    def test_invalid_yaml(self):
        _, _, error = split_frontmatter('---\ntype: [unclosed\n---\nBody')
        self.assertIsNotNone(error)

    def test_duplicate_yaml_keys_are_rejected(self):
        _, _, error = split_frontmatter('---\ntype: Rule\ntype: Other\n---\nBody')
        self.assertIn('Duplicate YAML key', error)

    def test_frontmatter_must_be_a_mapping(self):
        _, _, error = split_frontmatter('---\n- Rule\n---\nBody')
        self.assertEqual(error, 'Frontmatter must be a mapping')

    def test_unclosed_frontmatter(self):
        _, _, error = split_frontmatter('---\ntype: Rule\nBody')
        self.assertEqual(error, 'Unclosed YAML frontmatter')

    def test_code_does_not_declare_links_or_rules(self):
        root = self.fixture()
        self.append(root, '\n```md\n# REAS-RUST-001\n[bad](absent.md)\n```\n'
                    '\n    [bad](absent.md)\n\n`[bad](absent.md)`\n')
        self.assertEqual(validate(root), [])

    def test_real_repository(self):
        self.assertEqual(validate(Path(__file__).resolve().parents[1]), [])

    def test_missing_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(validate(Path(directory)), ['The standard/ OKF bundle is missing'])

    def test_missing_index(self):
        root = self.fixture()
        (root / 'standard/index.md').unlink()
        self.assertEqual(validate(root), ['standard/index.md: Bundle index is missing'])

    def test_wrong_index_version(self):
        root = self.fixture()
        path = root / 'standard/index.md'
        path.write_text(path.read_text().replace('0.2', '0.1'))
        self.assertTrue(any('Bundle index must' in error for error in validate(root)))

    def test_unindexed_concept_is_rejected(self):
        root = self.fixture({'standard/hidden.md': '---\ntype: Rule\n---\nHidden.\n'})
        self.assertTrue(any('not reachable' in error for error in validate(root)))

    def test_indirect_index_navigation_is_valid(self):
        root = self.fixture({'standard/deep/concept.md': '---\ntype: Reference\n---\nText.\n'})
        self.append(root, '\n[More](deep/concept.md)\n')
        self.assertEqual(validate(root), [])

    def test_navigation_cannot_leave_and_reenter_the_bundle(self):
        root = self.fixture({
            'README.md': '[Hidden](standard/hidden.md)\n',
            'standard/hidden.md': '---\ntype: Rule\n---\nHidden.\n',
        })
        self.append(root, '\n[Outside](../README.md)\n')
        self.assertTrue(any('hidden.md: Concept is not reachable' in error for error in validate(root)))

    def test_broken_inline_reference_and_image_paths(self):
        cases = ('[missing](absent.md)', '[missing][target]\n\n[target]: absent.md',
                 '![missing](absent.png)', '[target][]\n\n[target]: absent.md',
                 '[target]\n\n[target]: absent.md')
        for content in cases:
            with self.subTest(content=content):
                root = self.fixture()
                self.append(root, '\n' + content + '\n')
                self.assertTrue(any('Broken local link' in error for error in validate(root)))

    def test_reference_link_title_and_parentheses(self):
        root = self.fixture({'standard/file(one).md': '---\ntype: Reference\n---\nText.\n'})
        self.append(root, '\n[more][ref]\n\n[ref]: <file(one).md> "A title"\n')
        self.assertEqual(validate(root), [])

    def test_same_and_cross_file_fragments(self):
        for destination in ('#absent', 'index.md#absent'):
            with self.subTest(destination=destination):
                root = self.fixture()
                self.append(root, f'\n[bad]({destination})\n')
                self.assertTrue(any('Broken local fragment' in error for error in validate(root)))

    def test_github_style_heading_fragments(self):
        root = self.fixture()
        self.append(root, '\n## A `code` heading!\n\n## A `code` heading!\n'
                    '\n[one](#a-code-heading) [two](#a-code-heading-1)\n')
        self.assertEqual(validate(root), [])

    def test_unicode_and_explicit_html_anchors(self):
        root = self.fixture()
        self.append(root, '\n## Café\n\n<a id="stable"></a>\n'
                    '\n[one](#caf%C3%A9) <a href="#stable">two</a>\n')
        self.assertEqual(validate(root), [])

    def test_broken_html_links_are_rejected(self):
        root = self.fixture()
        self.append(root, '\n<a href="absent.md">bad</a>\n')
        self.assertTrue(any('Broken local link' in error for error in validate(root)))

    def test_absolute_paths_use_the_document_scope(self):
        root = self.fixture({'README.md': '[index](/standard/index.md#index)\n'})
        self.append(root, '\n[self](/rule.md#reas-rust-001-rule)\n')
        self.assertEqual(validate(root), [])

    def test_directory_navigation_uses_an_index(self):
        root = self.fixture({
            'standard/deep/index.md': '# More\n[Concept](concept.md)\n',
            'standard/deep/concept.md': '---\ntype: Reference\n---\nText.\n',
        })
        self.append(root, '\n[More](deep/)\n')
        self.assertEqual(validate(root), [])

    def test_directory_fragment_uses_readme_when_index_is_absent(self):
        root = self.fixture({'example/README.md': '# Example\n'})
        self.append(root, '\n[example](../example/#example)\n')
        self.assertEqual(validate(root), [])

    def test_link_cannot_escape_repository(self):
        root = self.fixture()
        self.append(root, '\n[escape](../../outside.md)\n')
        self.assertTrue(any('Link leaves repository' in error for error in validate(root)))

    def test_invalid_html_uri_reports_an_error_instead_of_crashing(self):
        root = self.fixture()
        self.append(root, '\n<a href="http://[">bad</a>\n')
        self.assertTrue(any('Invalid link URI' in error for error in validate(root)))

    def test_external_urls_are_not_fetched(self):
        root = self.fixture()
        self.append(root, '\n[external](https://invalid.example/missing#absent)\n')
        self.assertEqual(validate(root), [])

    def test_duplicate_rule_outside_bundle_is_rejected(self):
        root = self.fixture({'README.md': '# REAS-RUST-001: Another rule\n'})
        self.assertTrue(any('Duplicate REAS-RUST-001' in error for error in validate(root)))

    def test_setext_rule_declarations_are_checked(self):
        root = self.fixture({'README.md': 'REAS-RUST-001: Duplicate\n========================\n'})
        self.assertTrue(any('Duplicate REAS-RUST-001' in error for error in validate(root)))

    def test_malformed_rule_ids_are_rejected(self):
        for identifier in ('REAS-RUST-02', 'REAS-RUST-0010', 'REAS-rust-002'):
            with self.subTest(identifier=identifier):
                root = self.fixture()
                self.append(root, f'\n## {identifier}: Bad\n')
                self.assertTrue(any('Invalid rule declaration' in error for error in validate(root)))

    def test_log_is_not_a_concept(self):
        root = self.fixture({'standard/log.md': '# Updates\n\n## 2026-10-23\nA change.\n'})
        self.assertEqual(validate(root), [])

    def test_invalid_log_dates_are_rejected(self):
        root = self.fixture({'standard/log.md': '# Updates\n\n## 2026-02-30\nA change.\n'})
        self.assertTrue(any('Log date must' in error for error in validate(root)))

    def test_nested_index_frontmatter_is_rejected(self):
        root = self.fixture({'standard/deep/index.md': '---\nokf_version: "0.2"\n---\n# More\n'})
        self.assertTrue(any('Nested index must not' in error for error in validate(root)))

    def test_event_metadata_accepts_mapping_list_and_utc_offsets(self):
        for field in ('generated: {by: process:ci, at: 2026-10-23T12:00:00Z}',
                      'verified: {by: human:reviewer, at: "2026-10-23T08:00:00-04:00"}',
                      'verified: [{by: tool/1, at: 2026-10-23T12:00:00Z}]'):
            with self.subTest(field=field):
                root = self.fixture({'standard/rule.md': f'---\ntype: Rule\n{field}\n---\n# REAS-RUST-001\n'})
                self.assertEqual(validate(root), [])

    def test_invalid_event_actors_and_timestamps_are_rejected(self):
        cases = ('generated: {by: unknown, at: 2026-10-23T12:00:00Z}',
                 'verified: {by: human:reviewer}',
                 'verified: {by: human:reviewer, at: rubbish}',
                 'verified: {by: human:reviewer, at: 2026-10-23}',
                 'verified: {by: human:reviewer, at: "2026-10-23T12:00:00"}')
        for field in cases:
            with self.subTest(field=field):
                root = self.fixture({'standard/rule.md': f'---\ntype: Rule\n{field}\n---\n# REAS-RUST-001\n'})
                self.assertTrue(any('Invalid ' in error for error in validate(root)))

    def test_source_requires_a_resource(self):
        root = self.fixture({'standard/rule.md': '---\ntype: Rule\nsources: [{title: Missing}]\n---\n# REAS-RUST-001\n'})
        self.assertTrue(any('Sources must include' in error for error in validate(root)))

    def test_unknown_metadata_is_preserved_as_an_extension(self):
        root = self.fixture({'standard/rule.md': '---\ntype: Rule\ncustom: value\n---\n# REAS-RUST-001\n'})
        self.assertEqual(validate(root), [])


class RuleShapeTests(FixtureTests):
    def standard(self, body=STANDARD, extra=None):
        files = {'standard/rule.md': body}
        files.update(extra or {})
        return self.fixture(files)

    def test_well_formed_standard_passes(self):
        self.assertEqual(validate(self.standard(), today=date(2026, 11, 20)), [])

    def test_rule_type_fixtures_are_not_held_to_the_shape(self):
        self.assertEqual(validate(self.fixture()), [])

    def test_missing_section_is_rejected(self):
        body = STANDARD.replace('### Scope\n\nWhere.\n\n', '')
        errors = validate(self.standard(body), today=date(2026, 11, 20))
        self.assertTrue(any('Sections must be' in error for error in errors), errors)

    def test_sections_out_of_order_are_rejected(self):
        body = STANDARD.replace('### Intent\n\nWhy.\n\n### Enforcement\n\nRequired.\n\n',
                                '### Enforcement\n\nRequired.\n\n### Intent\n\nWhy.\n\n')
        errors = validate(self.standard(body), today=date(2026, 11, 20))
        self.assertTrue(any('Sections must be' in error for error in errors), errors)

    def test_allowances_is_optional_but_positioned(self):
        good = STANDARD.replace('### Verification', '### Allowances\n\nExcept here.\n\n### Verification')
        self.assertEqual(validate(self.standard(good), today=date(2026, 11, 20)), [])
        bad = STANDARD.replace('### Rules', '### Allowances\n\nExcept here.\n\n### Rules')
        errors = validate(self.standard(bad), today=date(2026, 11, 20))
        self.assertTrue(any('Sections must be' in error for error in errors), errors)

    def test_enforcement_value_is_closed(self):
        for value, ok in (('Required.', True), ('Advisory.', True), ('Mandatory.', False), ('required', False)):
            with self.subTest(value=value):
                body = STANDARD.replace('Required.', value)
                errors = validate(self.standard(body), today=date(2026, 11, 20))
                self.assertEqual(any('Enforcement must be' in error for error in errors), not ok, errors)

    def test_empty_section_is_rejected(self):
        body = STANDARD.replace('### Rules\n\nDo this.\n\n', '### Rules\n\n')
        errors = validate(self.standard(body), today=date(2026, 11, 20))
        self.assertTrue(any('Rules section is empty' in error for error in errors), errors)

    def test_rule_heading_must_be_level_two(self):
        body = STANDARD.replace('## REAS-RUST-001: Rule', '### REAS-RUST-001: Rule')
        errors = validate(self.standard(body), today=date(2026, 11, 20))
        self.assertTrue(any('must be level 2' in error for error in errors), errors)

    def test_quality_test_is_required_and_non_empty(self):
        missing = STANDARD.replace('\n## Quality test\n\nCan it?\n', '')
        errors = validate(self.standard(missing), today=date(2026, 11, 20))
        self.assertTrue(any("Missing 'Quality test'" in error for error in errors), errors)
        empty = STANDARD.replace('Can it?\n', '')
        errors = validate(self.standard(empty), today=date(2026, 11, 20))
        self.assertTrue(any("'Quality test' section is empty" in error for error in errors), errors)

    def test_every_real_rule_has_the_shape(self):
        # Floor for the gate: the real bundle declares rules in Engineering Standard concepts.
        count = sum(
            path.read_text().count('\n## REAS-')
            for path in (REPO / 'standard').glob('*.md')
            if 'type: Engineering Standard' in path.read_text()
        )
        self.assertGreaterEqual(count, 20)
        self.assertEqual(validate(REPO), [])


class LimitsSectionTests(FixtureTests):
    def standard(self, body):
        return self.fixture({'standard/rule.md': body})

    def test_limits_is_accepted_after_verification(self):
        body = STANDARD.replace('- Review question: how?\n', '- Review question: how?\n\n### Limits\n\nNot this.\n')
        self.assertEqual(validate(self.standard(body), today=date(2026, 11, 20)), [])

    def test_limits_before_verification_is_rejected(self):
        body = STANDARD.replace('### Verification', '### Limits\n\nNot this.\n\n### Verification')
        errors = validate(self.standard(body), today=date(2026, 11, 20))
        self.assertTrue(any('Sections must be' in error for error in errors), errors)

    def test_empty_limits_is_rejected(self):
        body = STANDARD.replace('- Review question: how?\n', '- Review question: how?\n\n### Limits\n\n')
        errors = validate(self.standard(body), today=date(2026, 11, 20))
        self.assertTrue(any('Limits section is empty' in error for error in errors), errors)


class RetiredTermTests(FixtureTests):
    def bundle(self, extra=None):
        files = {'standard/terminology.md': TERMINOLOGY}
        files.update(extra or {})
        root = self.fixture(files)
        self.append(root, '\n[Terms](terminology.md)\n', name='standard/index.md')
        return root

    def test_clean_bundle_passes(self):
        self.assertEqual(validate(self.bundle()), [])

    def test_planted_retired_term_fails(self):
        root = self.bundle()
        self.append(root, '\nWe use the OLD TERM here.\n')
        errors = validate(root)
        self.assertIn("standard/rule.md: Retired term 'old term'; use new term", errors)

    def test_retired_term_in_code_is_not_flagged(self):
        root = self.bundle()
        self.append(root, '\nUse `old term` only in code.\n\n```text\nold term\n```\n')
        self.assertEqual(validate(root), [])

    def test_exempt_documents_may_mention_retired_terms(self):
        root = self.bundle({'CHANGELOG.md': '# Changelog\n\nRenamed old term.\n'})
        self.assertEqual(validate(root), [])

    def test_missing_or_empty_table_is_a_floor_failure(self):
        for text, message in (
            ('---\ntype: Technical Reference\n---\n# Terms\n', 'Retired terms section is missing'),
            ('---\ntype: Technical Reference\n---\n# Terms\n\n## Retired terms\n\n| Term | Use instead |\n| --- | --- |\n', 'Retired terms table is empty'),
        ):
            with self.subTest(message=message):
                root = self.bundle({'standard/terminology.md': text})
                self.assertTrue(any(message in error for error in validate(root)))

    def test_bundle_without_terminology_is_not_scanned(self):
        root = self.fixture()
        self.append(root, '\nold term\n')
        self.assertEqual(validate(root), [])

    def test_real_terminology_retires_at_least_one_term(self):
        rows = retired_terms((REPO / 'standard/terminology.md').read_text())
        self.assertIsNotNone(rows)
        self.assertGreaterEqual(len(rows), 1)

    def test_parser_reads_term_and_replacement(self):
        self.assertEqual(retired_terms(TERMINOLOGY), [('old term', 'new term')])


class FreshnessTests(FixtureTests):
    def concept(self, updated, kind='Engineering Standard'):
        body = STANDARD.replace('type: Engineering Standard\nupdated: 2026-11-20', f'type: {kind}\nupdated: {updated}')
        return self.fixture({'standard/rule.md': body})

    def test_invalid_and_future_dates_are_errors(self):
        today = date(2026, 11, 20)
        self.assertTrue(any('Invalid updated' in e for e in validate(self.concept('yesterday'), today=today)))
        self.assertTrue(any('is in the future' in e for e in validate(self.concept('2027-01-01'), today=today)))

    def test_stale_concept_is_a_warning_not_an_error(self):
        root = self.concept('2025-01-01')
        today = date(2026, 11, 20)
        self.assertEqual(validate(root, today=today), [])
        warnings = freshness_warnings(root, today=today)
        self.assertEqual(len(warnings), 1)
        self.assertIn('the limit for Engineering Standard is 365', warnings[0])

    def test_threshold_depends_on_type(self):
        today = date(2026, 11, 20)
        fresh_enough_for_a_rule = self.concept('2026-08-01')
        self.assertEqual(freshness_warnings(fresh_enough_for_a_rule, today=today), [])
        stale_for_an_audit = self.concept('2026-08-01', kind='Audit Report')
        warnings = freshness_warnings(stale_for_an_audit, today=today)
        self.assertEqual(len(warnings), 1)
        self.assertIn('the limit for Audit Report is 90', warnings[0])

    def test_concept_without_updated_is_not_warned(self):
        self.assertEqual(freshness_warnings(self.fixture(), today=date(2026, 11, 20)), [])

    def test_every_real_concept_has_an_updated_date(self):
        missing = [
            path.relative_to(REPO).as_posix()
            for path in (REPO / 'standard').rglob('*.md')
            if path.name not in {'index.md', 'log.md'}
            and 'updated:' not in path.read_text().split('\n---', 1)[0]
        ]
        self.assertEqual(missing, [])


if __name__ == '__main__':
    unittest.main()
