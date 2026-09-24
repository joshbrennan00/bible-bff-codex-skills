# Bible BFF Codex skills

A reusable, human-reviewed workflow for publishing speaker story audio through the Bible BFF Content Library Manager hosted on Vercel.

This is a skill, not the backend application or an account-access bundle. It does not deploy a Vercel project. Your team must already operate the Content Library Manager described below.

## Start here

1. Download this repository using GitHub's **Code → Download ZIP** and unzip it, or clone it with Git. Open the resulting **bible-bff-codex-skills** folder as a project in Codex.
2. The skill is in `.agents/skills/uploading-speaker-stories-into-vercel/SKILL.md`. Repository skills are discovered when working in this project. If it does not appear, start a new task in the project and explicitly ask Codex to read that file. See [official skill documentation](https://developers.openai.com/codex/skills/). Astra can use it as the model in Codex; no special Astra package is required. Ordinary chat without file and browser tools cannot execute the workflow.
3. Use your own account to sign in to your team's Content Library Manager. Ask the team administrator for its URL and permission to publish. The dashboard must show **Drive ready** and **GCS ready**. The operator does not need a Vercel token, Firebase credentials, or a Google Cloud service-account key. Those integrations belong to the application's server and must remain there.
4. Enable the browser/computer-use capability available in your Codex installation. Let Codex read its tool documentation. The skill can also use a connected Google Drive plugin, authenticated with **your own Google account**, to list files or upload converted copies. You need access to the shared source folder; new conversion copies also require write access. No connector is bundled or automatically installed.
5. For the offline helpers, install **Python 3.10+**. Install **FFmpeg and ffprobe** only if WAV/M4A conversion is needed, using your normal trusted package manager (for example `brew install ffmpeg` on a Mac). Browser helper tests also need Node.js 18+. No Python packages, API keys, or npm dependencies are required.
6. Copy `.env.example` to `.env` if you want to keep the setup details locally. Fill in the app URL and source folder information from your team. These are optional operator notes: scripts do not auto-load `.env`. You can instead supply these details directly to Codex. Never add credentials. Keep all inventories, recordings, and receipts in ignored `work/`.
7. Run the offline tests: `python3 -m unittest discover -s tests -v` and `node tests/test_guards.cjs`. Then ask Codex: **“Use $uploading-speaker-stories-into-vercel. Check my setup and prepare one story for listening review. Do not publish.”** Codex should locate the app, speaker, catalog story and exact source, check current audio, and stop for review.
8. After listening, approve the exact recording. Start with one real approved story and verify its publication result before approving a larger batch. Normal prompt: **“Use uploading speaker stories into Vercel. Review the missing recordings for [speaker], in batches of 16. Skip existing audio and wait for my approval before publishing each batch.”**

## What to provide once

Your team's app URL, the Google Drive source folder link (or the app's Drive Library root), the speaker to process, and any preferred finished-edit folder. The app must already contain the speaker and canonical stories. Existing records are authoritative; old spreadsheets and filenames are only leads.

## What is included

- A complete review → approval → preflight → publication → verification workflow.
- Matching, format conversion, and guarded browser publication helpers.
- Private local queue/receipt schemas and recovery instructions.
- Offline tests and a security/portability review.

No audio, prior approval, historical queue, production ID, backend code, credentials, or account session is included. Each collaborator discovers a fresh queue from the live app. The full guide is [SKILL.md](.agents/skills/uploading-speaker-stories-into-vercel/SKILL.md).

## Maintainers

Before any public commit, review `git diff --cached`, run `python3 scripts/security_check.py`, and inspect all tracked files. The scanner is a guardrail, not a guarantee. Never force-add ignored work files. See [SECURITY_REVIEW.md](SECURITY_REVIEW.md).
