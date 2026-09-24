# Local data and helper usage

Store operational data under ignored `work/`. None belongs in public commits.

## Queue item

Fields: `speaker` (live display name), `speaker_id` (if visible), `speaker_slug` (observed from app), `story_id` (string), `story` (canonical title), `testament` (display value), `source_id`, `source_name`, `source_url` (retrieved), `source_parent_id`, `parts` (array of exact Drive names), `mime_type`, `size`, `md5`, `local_audio` (optional absolute path), `approval` (`pending` or `approved`), `approved_source_id`, `approved_md5`, `status`.

Keep alternate candidates in an array and record the selected index. No source IDs or mappings from someone else's account are bundled. Story aliases must be confirmed against the current catalog; a human speaker nickname may differ from the stored speaker name. IDs and slugs are not interchangeable.

Statuses: discovered → needs_review → approved → preflight → publishing → published; alternate outcomes skipped_existing, held_edit, failed, uncertain. Persist publishing state before the click; uncertain never returns automatically to approved.

## Receipt

Record speaker/story IDs, original approved source ID/hash, actual published source ID/hash, conversion details if any, destination, returned public URL, request ID, audio record ID, duration_seconds, timestamp, preflight_destination_empty, server_public_url_verified, and evidence/limitations. Store IDs as strings to preserve large integers. Do not include cookies or authorization headers.

## Matching

`python3 .agents/skills/uploading-speaker-stories-into-vercel/scripts/match.py work/catalog.json work/files.json --out work/proposals.json`

Catalog input is a JSON array of `{story_id, title, aliases: []}`. Files input is a JSON array of `{id, title, ...metadata}`. Optional `--noise work/noise.json` is a JSON array of verified speaker/editor names to ignore. The normalizer and exact/longest-title/fuzzy scoring are adapted from the working audit script. No hardcoded production IDs or historical “reviewed” overrides are carried over. Every output remains a proposal and cannot authorize publication.

## Conversion

`python3 .agents/skills/uploading-speaker-stories-into-vercel/scripts/convert_audio.py work/selected.wav work/converted.mp3`

Requires ffmpeg and ffprobe on PATH. Uses the working conversion parameters: libmp3lame at 192 kbps. Refuses overwrite and checks duration within 0.25 seconds. It does not trim, normalize, add a title or select a different performance. Upload the new copy using the connected Drive upload tool (read its current schema) or authorized browser upload. Use the verified parent folder ID. Retrieve the new metadata; never guess a file ID. Keep both originals and converted IDs in the private receipt. After verifying that the conversion preserves the approved recording and duration, bind the browser item approval fields to the converted file ID/checksum and retain the original approval plus conversion evidence separately. Do not rebind approval for any content edit or alternate performance.

## Browser helper

`scripts/browser_publish.cjs` exports `makePublisher(tab)` and pure guards. It uses the supported tab.playwright interface from the browser tool, not npm Playwright. Ask Codex to load its source into the browser runtime after reading that runtime's current documentation. If importing local modules is unsupported, use the same functions inline through the supported tool. Do not use Node or a standalone driver to bypass browser controls. The operator navigates source folders and classifies through visible controls first, then supplies an approved item and exact observed `destination`. Use `check(snapshot,item)`, `publish(item)`, then `settle(item)`; persist the returned receipt outside the browser through permitted workspace tools.

Never hardcode browser/tab IDs, an app hostname, bucket name or a workstation path in shared scripts. Environment notes in `.env` are intentionally not automatically sourced; this avoids executing arbitrary shell contents.
