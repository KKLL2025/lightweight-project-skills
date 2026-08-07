# Security Policy

## Supported versions

| Version | Support |
|---|---|
| `0.4.x` preview | Security reports accepted |
| Earlier previews | Not supported |

Preview support means reports are reviewed and fixes may be issued. It is not a production or safety certification.

## Report a vulnerability privately

Use [GitHub private vulnerability reporting](https://github.com/KKLL2025/lightweight-project-skills/security/advisories/new). Do not open a public issue for a vulnerability, leaked credential, private path, or unsafe migration case.

Please include:

- the affected skill, script, version, and operating system;
- a minimal reproduction or proof of concept;
- the expected and observed behavior;
- the potential impact, especially possible data loss or path escape;
- any safe mitigation you already tested.

The maintainers will acknowledge the report when it is reviewed, investigate in proportion to its impact, and coordinate public disclosure after a fix or mitigation is available. Response times are best-effort while the project remains a public preview.

## Scope

Security-sensitive areas include filesystem traversal, symlink handling, destructive migration guidance, untrusted repository content, secret exposure, and release artifact integrity. General usage questions belong in [SUPPORT.md](SUPPORT.md).
