import re

with open('frontend/src/style.css', 'r') as f:
    css = f.read()

# Add --bg-message to light mode
css = re.sub(
    r'(  --bg-ai: hsl\(250, 18%, 96%\);)',
    r'\1\n  --bg-message: #ffffff;',
    css
)

# Add --bg-message to dark mode (in both places)
css = re.sub(
    r'(  --bg-ai: hsl\(250, 12%, 13%\);)',
    r'\1\n  --bg-message: hsl(250, 14%, 18%);',
    css
)

# Precisely update .ai-message
old_ai_msg = """.ai-message {
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  color: var(--text-main);
  background: var(--surface);
  border: 1px solid var(--border);"""

new_ai_msg = """.ai-message {
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  color: var(--text-main);
  background: var(--bg-message);
  border: 1px solid var(--border);"""

css = css.replace(old_ai_msg, new_ai_msg)

with open('frontend/src/style.css', 'w') as f:
    f.write(css)
