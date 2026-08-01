# Conversion notes: pb-gravatar-url

## Still open

- **Consider a shared Python helper module** (analogous to `helper.rb`) for clipboard read/write/notify, so each converted script doesn't duplicate that plumbing. This would also make testing easier (mock the helper instead of subprocess).
