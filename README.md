# Nexus

A CLI notes manager written in Python.

## Core

* Notes are plain `.md` files.
* The filesystem is the source of truth.
* Notes can be edited with any editor; `$EDITOR` is used by Nexus.
* Nexus only acts when explicitly invoked.
* Currently implemented commands: `nexus init` and `nexus new`.

## Nexus Space

A Nexus space contains:

```text
.nexus/
000-inbox/
001-899/
900-unmanaged/
901-unknown/
996-audio/
997-images/
998-archive/
999-template/
main.md
```

* `000-inbox` — default location for new notes.
* `001–899` — user-created folders.
* `900-unmanaged` — notes automatically archived after remaining in the inbox for 31 days.
* `901-unknown` — notes Nexus cannot safely recognize or manage.
* `996-audio` — reserved for audio.
* `997-images` — image attachments.
* `998-archive` — user archive.
* `999-template` — templates.
* `000` and `900–999` are reserved for Nexus.

## Notes

`nexus new` creates notes in `000-inbox/`.

Created notes contain exactly:

```yaml
created: ...
type: nexus-note
```

The filesystem determines the note's name and location; metadata does not duplicate them.

After creation, Nexus only reads existing metadata and does not automatically rewrite notes.

Notes without a `created` remain in the inbox indefinitely.

## Inbox

The inbox is `000-inbox`.

A note left there for **31 days** after its creation date is automatically moved to `900-unmanaged`.

A note is considered managed once it has been moved out of the inbox.

## Main

`main.md` lives in the root of the Nexus space.

It provides a tree-like overview of the inbox and user-created folders (`001–899`).

## Configuration

Each Nexus space contains:

```text
.nexus/config.toml
```

It stores space-level configuration such as the creation date and Nexus-managed directory names.

## Archive

`900-unmanaged` is Nexus's automatic archive for unmanaged inbox notes.

`998-archive` is the user's manual archive and is used by a future `nexus archive` command.
