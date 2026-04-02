with open('frontend/src/style.css', 'r') as f:
    css = f.read()

# Revert everywhere
css = css.replace(
    '  background: var(--bg-message);\n  border: 1px solid var(--border);',
    '  background: var(--surface);\n  border: 1px solid var(--border);'
)

# Apply specifically to .ai-message
old_msg = """.ai-message {
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  color: var(--text-main);
  background: var(--surface);
  border: 1px solid var(--border);"""

new_msg = """.ai-message {
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  color: var(--text-main);
  background: var(--bg-message);
  border: 1px solid var(--border);"""

css = css.replace(old_msg, new_msg)

with open('frontend/src/style.css', 'w') as f:
    f.write(css)
