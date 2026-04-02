import re

with open('frontend/src/style.css', 'r') as f:
    css = f.read()

# Add --bg-code-inline to light mode
css = css.replace(
    '  --bg-message: #ffffff;',
    '  --bg-message: #ffffff;\n  --bg-code-inline: hsl(250, 20%, 94%);'
)

# Add --bg-code-inline to dark mode (in both places)
css = css.replace(
    '  --bg-message: hsl(250, 14%, 18%);',
    '  --bg-message: hsl(250, 14%, 18%);\n  --bg-code-inline: hsl(250, 14%, 26%);'
)

# Update inline code background
css = css.replace(
    'background-color: var(--surface-hover);',
    'background-color: var(--bg-code-inline);'
)

with open('frontend/src/style.css', 'w') as f:
    f.write(css)
