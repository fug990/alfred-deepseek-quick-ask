# Changelog

All notable changes to this project are documented here.

## 1.3.5 — 2026-08-19

- Increased the default maximum output length from 1024 to 4096 tokens.
- Added an explicit notice when DeepSeek reports that an answer was truncated by the output limit.

## 1.3.4 — 2026-08-19

- Replaced the oversized system dialog with a compact, resizable native panel.
- Removed the close button: press `Esc` or click outside the panel to dismiss it.
- The panel appears on the display containing the mouse pointer, rather than always using the primary display.

## 1.3.3 — 2026-08-19

- Replaced Alfred Large Type answer display with a compact native macOS panel.
- Long answers can now be scrolled, searched, selected, and copied normally, without opening TextEdit.
- Removed the oversized dialog header and close button; press `Esc` or click outside to close, and the panel follows the cursor's display.

## 1.3.1 — 2026-08-19

- Fixed `dsthink` for upgrades from earlier versions that do not yet have a `DEEPSEEK_THINKING` variable.

## 1.3.0 — 2026-08-19

- Explicitly disables DeepSeek V4 thinking mode by default.
- Never displays `reasoning_content`; only the model's final answer is shown.
- Added `dsthink` to switch thinking mode on or off.

## 1.2.0 — 2026-08-14

- Added `dsmodel` model picker, with `flash` and `pro` shortcuts.
- Supports `deepseek-v4-flash` and `deepseek-v4-pro`.
- Clears local conversation history when changing models.
- Uses `deepseek-v4-flash` as the default model.
- Added a system-prompt safeguard against inaccurate model identity claims.

## 1.1.0 — 2026-08-13

- Added `dsf` for contextual follow-up questions.
- Added `dsclear` to clear the local conversation.

## 1.0.0 — 2026-08-11

- First public-ready release with one-shot DeepSeek questions via `ds`.
