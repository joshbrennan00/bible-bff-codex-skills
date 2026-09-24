# App workflow and recovery

## Architecture and discovery

“Vercel” means the team's existing Content Library Manager website. It is a production UI, not Vercel's deployment dashboard. The UI reads Google Drive sources, publishes a storage object through its backend, registers Story Audio, records duration and audit lineage, and verifies the public URL. The observed storage provider is Google Cloud Storage; the application may use Firebase-related infrastructure. Its database schema and server credentials are not part of this skill.

Ask the team's administrator for the private app URL and Drive root. Discover navigation links in the live UI. Observed routes: `/drive`, `/publish`, `/retool/stories`, `/retool/speakers`, `/history`. These are UI routes, not supported API endpoints. Backend version changes may require adapting the UI instructions after inspection.

## Discovery

In Stories, use **Search Stories** with an exact catalog ID, then **Open Story {ID}**. Wait for the detail dialog and **Audio** heading; a Loading dialog is not evidence. Inspect the actual speaker row and its status. Close with **Close Story editor**. Existing audio for another speaker is not a duplicate. Any audio for the intended speaker needs reconciliation rather than blind replacement, including a broken record.

Get all catalog pages and all Drive pages if doing a full audit. The canonical catalog is the live app, not a static list shipped here. Exclude marketing/viral/intro-only assets from full-story queues, but inspect title-only collections when investigating a missing spoken title. Do not conclude a title was never recorded from filenames alone.

## Publishing

1. Open **Drive Library**, then the observed source root, speaker folder and exact components. Wait for each folder's contents to finish changing. A folder name can contain a literal slash; never split a display path to reconstruct hierarchy. Prefer folder IDs from connector metadata.
2. Preview the exact source file. Validate **Drive ID**, **Checksum**, filename, MIME and size against the approved queue. Metadata must finish loading before comparison.
3. **Select This File** → **Asset type Select an asset type** → **Speaker Audio Story**.
4. **Speaker Select a speaker** → exact current app speaker. Choose the **Testament** combo box. Wait for **Story Select a story**, open it, fill textbox **Filter story**, inspect the available options and select the exact catalog title. Do not guess an option when punctuation/case differs.
5. **Run Preflight**; wait for **Validate and Review Destination**. A disabled Run Preflight often means the check is still running. Do not click Publish from classification.
6. Validate source ID/checksum and both empty statuses. The app generates a canonical path structurally like `<configured-prefix>/speaker_audios/<speaker-slug>/stories/<testament-slug>/<story-slug>/narration.mp3`. The prefix and slugs must come from the app; do not manufacture the public URL. Compare the complete observed destination to the selected classification.
7. **Continue to Confirm**. Inspect **Operation: PUBLISH**, matching destination and production mode. **Publish File** once.
8. Wait for publication result. Expected text: **The file was published successfully and its public URL is available.**, **Anonymous request returned the expected content type.**, and **Record {ID} saved with duration ...**. Capture request ID, record ID, duration, public URL, file ID/checksum and timestamps into the local receipt. The returned storage URL is the app audio URL, not the Drive download URL.
9. Persist the receipt before navigating to another source. Optionally confirm the live Audio row. Do not repeatedly verify the same evidence without a reason.

## Recoveries learned from real operation

| Situation | Action |
|---|---|
| Folder shows old children under new breadcrumbs | Wait for contents to settle; navigate back to the correct parent and inspect. Repeated “Edited” folders are especially vulnerable. Verify final file ID before any write. |
| A local synced folder spells `/` as a space or has trailing whitespace | Keep local path separate from Drive components/IDs. Never reconstruct one from the other. |
| Story selector briefly missing after testament selection | Inspect current state; wait for the selector. Do not restart an upload already in flight. |
| Preflight incomplete | Read its result before proceeding; both empty statuses are mandatory. |
| WAV gets UNSUPPORTED MIME while destination says narration.mp3 | A changed filename is not conversion. Convert selected audio to actual MP3, upload a new source copy, and rerun preflight. |
| Folder says “on app already,” old report says missing | Live Story Audio plus fresh storage preflight outrank both labels. |
| Timeout or error after Publish | Search Publication History using request/source; inspect live audio. If COMPLETED and matching audio exists, reconcile the receipt and do not publish again. If public verification cannot be established, mark that field unverified. Retry only after a confirmed failed operation and fresh empty checks. |
| Browser disconnect | Save pending source, approval, phase and known request ID. Reconnect using supported tools. Inspect history before another publish. |
| Different source bytes since approval | Hold for new approval, even if name and ID are unchanged. |
| Missing title or questionable content | Hold exact recording; provide evidence and editing note. Do not invent or splice narration without permission. |

## Resume

Read only local `work/queue.json`, `work/receipts.json` and `work/CHECKPOINT.md`. Reconcile completed and in-flight operations with the live app. Historical approval remains valid for the same source bytes; historical absence does not. Never bulk-replay a queue without per-item verification.
