---
name: uploading-speaker-stories-into-vercel
description: Review, match, deduplicate, and publish approved Bible BFF speaker story audio through the existing Vercel-hosted Content Library Manager, then verify publication and present the next review batch. Use for narrator audio backlogs, not Vercel deployments or story-video production.
---

# Uploading speaker stories into Vercel

Read [workflow](references/workflow.md) for app steps and failure recovery and [data](references/data.md) before creating a queue. No previous conversation or private export is required.

## Inputs and access

Obtain the team's Content Library Manager URL, source Drive folder, and speaker. If the user asks for the next highest speaker, compute counts of unique missing speaker–story pairs from fresh sources; do not reuse historic rankings. Use the user's own authenticated browser and optional Drive connection. Check the app's Drive/GCS readiness. Never request backend secrets; the existing server handles storage and database writes. If tools or app access are missing, finish offline preparation and identify that concrete dependency.

## Workflow

1. Discover the live speaker identity, canonical story IDs/titles/testament and existing audio. Reconcile spelling aliases against the actual app speaker, not a guessed slug.
2. Inventory the approved Drive tree using paginated listings or the app Drive Library. Preserve source file ID, exact filename, folder IDs/path components, MIME, size, checksum and source URL. Resolve shortcuts or hold them. Do not classify a listing error as an empty folder.
3. Match full stories to catalog entries. The helper `scripts/match.py` produces proposals only. Confirm ambiguous spellings, title collisions, multi-story files, viral clips, raw/test recordings and partial titles. Keep multiple edits grouped; identical filenames do not mean identical audio. Compare hashes; if different, show alternatives unless the user already selected one.
4. Check current Story Audio for the speaker. Skip existing audio. Prefer finished edits. Treat “needs a title”, corrections, partial takes and unclear versions as holds. A “REDO” label is a review flag, not automatic rejection or approval. Edited files inside a “needs edit” parent can be valid; folder labels alone are not proof.
5. Present up to 16 recordings (or requested size) with titles, version labels and easy listening. Use supported media preview or local absolute-path audio embeds for already available files. Otherwise give the exact Drive source link. Do not download remote audio merely to evade display restrictions. Check that the spoken opening is the intended title; filename inspection is not listening verification. The user may perform the listening check.
6. Record approval bound to speaker, story, exact file ID and checksum. Persist it locally. Continue approved work without asking again. A new batch, ambiguous A/B choice, changed source bytes or correction requires new review. Do not interpret “everything looks good” as selection of two competing takes.
7. If the app rejects WAV/M4A, use `scripts/convert_audio.py` to create an MP3 from the selected recording without editing content. Add a new copy to the verified original Drive folder through the user's Drive connector or browser. Preserve the original; verify the new ID, metadata, duration and checksum. Record both IDs and conversion lineage. New conversion is not permission to substitute another performance.
8. Publish one recording at a time through fresh preflight, confirming the selected file/checksum, speaker/testament/story and server-generated destination. Both **GCS status: Available** and **Story audio record: Available** mean empty in this app's preflight. Require **All preflight checks passed**, production mode, and **PUBLISH**, never overwrite. Any existing destination is a stop/skip for that item even if previously approved.
9. Record the request ID before another upload. Require success, expected public content type, and saved Story Audio record with positive duration. If result is uncertain, inspect Publication History and live Story Audio before retrying. Never repeat Publish merely because a timeout occurred.
10. Save receipts/checkpoint after each item, report published/skipped/held, then automatically present the next unapproved batch. When requested and supported, record account-wide usage at start/end; report percentage-point difference and acknowledge other tasks can contribute. If unavailable, say unavailable, not zero.

## Tools and scripts

Use supported connector/browser tools, reading their current documentation first. `scripts/browser_publish.cjs` preserves the session's UI publication guard logic, parameterized for a selected tab and item. It is a helper to load into the supported browser runtime, not a standalone browser driver. Run prepare, inspect, publish, settle as separate steps. Re-observe after state changes; folder navigation remains agent-guided because repeated folder labels can select stale content. Never run hidden app APIs, extract cookies, or use raw database writes as a workaround.

## Approval boundaries and output

User batch approval authorizes publication of those exact recordings. Do not request redundant confirmation. Stop for unresolved versions, new content edits or overwrites; normal browser/platform permission rules still apply. Do not grant backend privileges or alter public-read settings manually. No messages to editors or team members without explicit instruction.

Final output: count verified, skipped duplicates and unresolved holds; distinguish app/server verification from actual consumer-app playback. Provide next listening batch when available, keeping it unapproved. Never claim completion from an attempted click.
