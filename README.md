# REAS — Rust Engineering & Architecture Standard

REAS is an opinionated engineering standard for Rust code. It favors explicit domain types, state machines, and **human-readable ports and adapters**. It also defines rules for technical documentation.

**Current version:** 1.2.0-draft. This is a draft, not a Rust framework, a runtime dependency, or an officially certified standard.

## Read the standard

Start with the [REAS knowledge index](standard/index.md). Open only the rules that apply to your project.

For AI coding agents, use [CLAUDE.md](CLAUDE.md) or [AGENTS.md](AGENTS.md).

- [Core Rust](standard/core-rust.md)
- [Ports and adapters](standard/ports-and-adapters.md)
- [State machines](standard/state-machines.md)
- [Database persistence](standard/persistence.md)
- [Documentation](standard/documentation.md)
- [Technical terminology](standard/terminology.md)
- [Self-audit and limitations](standard/self-audit.md)
- [STE review procedure](standard/ste-review.md)

## Key decisions

Use zero-cost abstractions when they clarify behavior. Do not make compilation speed the goal. Compile locally if the development environment cannot run the build.

Favor ports and adapters for public or human-maintained systems. Keep the concrete implementation easy to locate. For private projects, ask a few questions before you select the architecture.

Use ASD-STE100, Issue 9, as the **target** writing standard. Keep project knowledge in an [OKF v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) bundle. **Full STE compliance has not been verified.**

## Check the documentation

Install the validation dependency, then run the checks:

```bash
python -m pip install -r requirements-docs.txt
python scripts/check_docs.py
python -m unittest discover -s tests -v
```

The checker reads local files. It does not verify external URLs or the full ASD-STE100 vocabulary. See [the self-audit](standard/self-audit.md).

The [examples](examples/README.md) are separate small Cargo packages. Test them with Cargo when Rust is installed.

## Status and contribution

See the [changelog](CHANGELOG.md) and [contribution guide](CONTRIBUTING.md). REAS is independent of the Rust project, the ASD-STE100 publishers, and the OKF maintainers.

## License

Original documentation uses [CC BY 4.0](LICENSE-DOCS). Example code uses [MIT](LICENSE-CODE). External standards retain their own terms.
