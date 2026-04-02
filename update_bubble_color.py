import re

with open('frontend/src/style.css', 'r') as f:
    css = f.read()

# Add --bg-message to light mode
css = css.replace(
    '  --bg-ai: hsl(250, 18%, 96%);',
    '  --bg-ai: hsl(250, 18%, 96%);\n  --bg-message: #ffffff;'
)

# Add --bg-message to dark mode (in both places)
css = css.replace(
    '  --bg-ai: hsl(250, 12%, 13%);',
    '  --bg-ai: hsl(250, 12%, 13%);\n  --bg-message: hsl(250, 14%, 18%);'
)

# Update .ai-message background
css = css.replace(
    '  background: var(--surface);',
    '  background: var(--bg-message);'
)

with open('frontend/src/style.css', 'w') as f:
    f.write(css)
