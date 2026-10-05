# Install Ref.

Ref is a Claude skill. There are three ways to install it. Pick the one that matches where you use Claude. Menu labels can vary slightly between app versions, so if yours differ, look for the nearest match.

Downloads live in two places with the same files: unfayr.com/ref and the Releases page of the GitHub repo (github.com/timlaneseo-tech/unfayr-ref/releases). The skill zip is named like `ref-1.0.0.zip`. The sample kit is `ref-sample-kit-1.0.0.zip`.

## Claude Code, from GitHub.

This is the fastest way, and you get updates when we ship them. In a Claude Code session, run:

```
/plugin marketplace add timlaneseo-tech/unfayr-ref
/plugin install ref@unfayr
```

Or from your shell:

```
claude plugin marketplace add timlaneseo-tech/unfayr-ref
claude plugin install ref@unfayr
```

Restart Claude Code, then ask it to start a review. Review files are saved in `./reviews/` in the folder where you run it. To update later, run `/plugin marketplace update unfayr`.

## claude.ai.

1. Download the skill zip.
2. Open **Settings**, then **Capabilities**.
3. Turn on code execution (it may be called "Code execution and file creation"). Ref needs it to keep the review file valid.
4. Under **Skills**, choose to upload a skill and select the zip. Don't unzip it first.
5. Make sure **Ref** is switched on in the skills list.
6. Start a new chat and say: "Start a review for my spring promo email."

## Claude desktop app.

Same as claude.ai. Open **Settings**, then **Capabilities**, turn on code execution, upload the zip under **Skills** and switch Ref on.

## Claude Code, from the zip.

If you'd rather not add a marketplace, unzip the skill so the folder ends up at `~/.claude/skills/ref`, with `SKILL.md` directly inside it. On Windows that is `%USERPROFILE%\.claude\skills\ref`. Use the name of the file you downloaded in place of `ref-1.0.0.zip` below.

macOS and Linux:

```
mkdir -p ~/.claude/skills
unzip -o ref-1.0.0.zip -d ~/.claude/skills
```

Windows (PowerShell):

```
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
Expand-Archive ref-1.0.0.zip -DestinationPath "$env:USERPROFILE\.claude\skills" -Force
```

The zip already contains the `ref` folder. To upgrade, run the same commands with the new zip.

Ref needs Python 3.10 or newer. Claude Code uses the Python on your machine. If `python` isn't found, Ref tries `python3`.

## Optional connectors.

Ref works without any connectors: paste feedback into the chat and Ref does the rest. If you have the Gmail, Slack or Google Drive connectors turned on, you can also say "check my email and Slack for feedback on the spring promo" and Ref will search for it.

What Ref does with connectors:

- It reads only what you point it at: a thread, a channel, a document.
- It shows you what it found before it records anything.
- It never sends. Every message stays a draft for you to send. With Gmail, Ref can create a draft only if you ask.
- If a connector fails, Ref says which one and asks you to paste that feedback instead.

If a Google Drive connector is on, Ref may offer to save a copy of the review file there. It is only an offer.

## Check it works.

Download the sample kit and try it using the steps in the [README](README.md#try-it-in-2-minutes).

Built by Unfayr · unfayr.com
