# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of scripts that operate on the macOS pasteboard (clipboard). The scripts are designed to be triggered from launchers such as Quicksilver or Alfred, and perform various transformations on clipboard content.

## Core Architecture

- **Script Files**: Root-level `pb-*` files (58 total) are the main clipboard transformation scripts
  - **Ruby scripts** (~43): Use `helper.rb` library, follow pattern below
  - **Shell scripts** (~14): Standalone bash/sh scripts using pbpaste/pbcopy directly
  - **Python scripts** (2): `pb-quote-wrap`, `pb-json-dumps` - examples of ongoing refactoring
- **Library Code**: `lib/` contains shared modules:
  - `helper.rb`: Core Ruby clipboard operations (`clipboard`, `notify`, `pbpaste`/`pbcopy`)
  - `humanize.rb`: Text humanization utilities with ActiveSupport integration
  - `notify`: Bash script fallback notification system using osascript
  - `copy-finder-path.scpt`: AppleScript for Finder integration
- **Installation**: `install.rb` and `Rakefile` handle copying scripts to `bin/` directory and making them executable
- **Testing**: RSpec tests in `spec/` directory with Guard for auto-running

## Development Commands

### Installation and Setup

```bash
# Install all scripts to bin/ directory
rake install
# or just:
rake  # (default task)

# Install dependencies
bundle install
```

### Testing

```bash
# Run all tests
bundle exec rspec

# Run specific test
bundle exec rspec spec/pb-humanize_spec.rb
bundle exec rspec spec/lib_notify_spec.rb

# Auto-run tests with Guard (watches pb-* and spec files)
bundle exec guard
```

**Test coverage includes:**
- `pb-humanize_spec.rb`: HumanizingString class
- `pb-sort_spec.rb`: Sorting functionality
- `lib_notify_spec.rb`: Comprehensive notification system tests (special characters, escaping, edge cases)

### Script Structure

Scripts come in three varieties based on ongoing refactoring:

**Ruby scripts** (most common):
```ruby
#!/usr/bin/env ruby
require "helper"
clipboard {|content| content.some_transformation }
```
We want to Boy Scout Rule our way to re-writing all of these to Python.

**Shell scripts** (simple transformations):
```bash
#!/bin/bash
pbpaste | some_command | pbcopy
```
These can be kept when they're simple. Once they get ugly, they should be re-written to Python.

**Python scripts** (refactoring target):
```python
#!/usr/bin/env python3
import subprocess
content = subprocess.run(['pbpaste'], capture_output=True, text=True).stdout
# ... transformation ...
subprocess.run(['pbcopy'], input=result, text=True)
```
Keep them neat and clean.

## Key Implementation Details

- Scripts use macOS `pbpaste`/`pbcopy` commands for clipboard access
- Notification system: GrowlNotify → `lib/notify` bash script → osascript (with proper AppleScript escaping) (pause to shed a tear for the loss of growlnotify - nothing else compares to you!)
- Installation process can replace secrets from `~/.dotfiles_secrets` YAML file for API keys/tokens FIXME: .dotfiles_secrets is ancient history. Re-write to use `security` and secrets stored in the keychain.
- Ruby dependencies are managed via Bundler (`Gemfile`) (but see above; we want to move away from ruby)

## Dependencies

- Ruby with Bundler
- Optional: GrowlNotify for notifications
- Optional: Quicksilver or Alfred for script launching

## Project Refactoring Goals

1. Migrate towards fewer external dependencies and simpler setup
2. Migrate away from Ruby, towards Python for complex scripts, and bash for simple scripts

**Current progress:**
- Python scripts: `pb-quote-wrap`, `pb-json-dumps`
- Shell scripts: ~14 scripts already converted
- Ruby scripts: ~43 remaining (uses ActiveSupport, humanize, titlecase gems)

TODO:
- update .gitignore (think about it, then do what I mean)
