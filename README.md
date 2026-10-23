# REAS — Rust Engineering & Architecture Standard

REAS is an opinionated engineering standard for Rust code. It favors explicit domain types, state machines, and **human-navigable ports and adapters**. It also defines rules for technical documentation.

**Current version:** 1.4.0-draft. This is a draft, not a Rust framework, a runtime dependency, or an officially certified standard.

## Read the standard

Start with the [REAS knowledge index](standard/index.md). Open only the rules that apply to your project.

For AI coding agents, use [CLAUDE.md](CLAUDE.md) or [AGENTS.md](AGENTS.md).

- [Core Rust](standard/core-rust.md)
- [Ports and adapters](standard/ports-and-adapters.md)
- [State machines](standard/state-machines.md)
- [Persistence and transactions](standard/persistence.md)
- [Validation, security, and evidence](standard/validation.md)
- [Documentation](standard/documentation.md)
- [Technical terminology](standard/terminology.md)
- [Self-audit and limitations](standard/self-audit.md)
- [STE review procedure](standard/ste-review.md)

## Key decisions

Choose abstractions for clarity first, then check their runtime cost. Do not make compilation speed the goal. Compile locally if the hosted build cannot run Cargo.

Use ports and adapters for public or human-maintained applications.
Keep the concrete adapter easy to locate.
For private projects, use [REAS-ARCH-003](standard/ports-and-adapters.md#reas-arch-003) to select the architecture and record exceptions.

Use ASD-STE100, Issue 9, as the **target** writing standard. Keep project knowledge in an [OKF v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) bundle. **The language review does not establish full STE compliance.**
See the [review scope and open findings](standard/ste-review.md).

## Check the documentation

Install the validation dependency, then run the checks:

```bash
python -m pip install -r requirements-docs.txt
python scripts/check_docs.py
python -m unittest discover -s tests -v
```

The checker validates the REAS frontmatter profile, index reachability, rule declarations, local destinations, and Markdown fragments.
See its [supported syntax and limits](standard/checker.md).
It does not establish full OKF or ASD-STE100 compliance.

The [examples](examples/README.md) are separate Cargo packages.
GitHub Actions runs Cargo checks, tests, Clippy, formatting checks, and nightly diagnostic-code doctests.
The [self-audit](standard/self-audit.md) identifies the code revision verified by each cited run.

## Status and contribution

See the [changelog](CHANGELOG.md) and [contribution guide](CONTRIBUTING.md). REAS is independent of the Rust project, the ASD-STE100 publishers, and the OKF maintainers.

## License

Original documentation uses [CC BY 4.0](LICENSE-DOCS). Example code uses [MIT](LICENSE-CODE). External standards retain their own terms.
