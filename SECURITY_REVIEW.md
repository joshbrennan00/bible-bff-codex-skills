# Security and portability review

## Public package boundary

Only reusable instructions, generic source code and synthetic test cases belong here. Historical source inventories, recordings, private IDs, application hostname, bucket names, local account paths, receipts and conversation exports were excluded. No OAuth, Vercel, Firebase or Google Cloud credentials are required or included. The environment example contains only optional non-secret operator settings.

This repository begins with a new history. Do not copy the parent workspace's Git history. The included scanner checks tracked content and reachable commit blobs for selected credential patterns and private paths; manual review is also required. Pattern scanning cannot prove that every possible secret is absent.

## Portability boundary

A fresh operator can discover the workflow from the README, skill, schema reference, UI recovery guide and helper scripts. Runtime inputs are the team-provided app URL, source root, account access and speaker selection. These private configuration values intentionally must be provided separately. Existing production infrastructure is required; this package does not recreate it or grant access.

Offline tests exercise ambiguous matching, longest-title matching, conversion duration, overwrite refusal and publication rejection when approval/source/destination checks fail. They use synthetic data only. Browser publication must still be smoke-tested through the new operator's account with one approved real recording. No claim is made that another person's authentication or production access has been tested.

## Preserved and changed behavior

The working audit normalizer, exact/contained-title matching and fuzzy thresholds are retained in a parameterized helper. Historical title-to-ID overrides and blanket promotion of fuzzy matches were removed: those encode old human decisions and are unsafe to transfer. The page-building scripts produced private audit reports rather than performing publication, so they are not bundled; the queue schema carries their reusable grouping principles.

The working browser workflow was held in conversation-local functions. Its source/checksum, empty-destination, PUBLISH and result checks are packaged as a parameterized browser helper. Approval binding and exact destination checks make those invariants explicit. Source navigation remains agent-guided because same-name nested folders can expose stale children. The conversion parameters remain libmp3lame at 192 kbps; overwrite refusal and duration checks were added for portability.

## Maintainer release checklist

- Run both test commands in the README and the skill frontmatter validator when available.
- Review every tracked file and the complete first commit diff.
- Run `python3 scripts/security_check.py` before and after the first commit.
- Ensure `.env`, media, receipts and private working files remain ignored.
- Publish only this repository, never the surrounding workspace.

## Validation performed for the initial package

Python matching/conversion tests and Node publication guard tests passed using synthetic fixtures. Local documentation links and required skill metadata were validated. The bundled optional quick_validate.py could not run because PyYAML was unavailable; the skill has only simple name/description frontmatter, checked directly. No production uploads were performed as a package test. A fresh-account walkthrough was reviewed against the README: missing app URL/access is an explicit setup input, and all operational state is rebuilt locally.
