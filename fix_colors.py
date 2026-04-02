import re

with open('frontend/src/style.css', 'r') as f:
    css = f.read()

# Update light mode
css = css.replace(
    '  --bg-message: #ffffff;',
    '  --bg-message: #ffffff;\n  --bg-code-inline: hsl(250, 20%, 94%);'
)

# Update dark mode
css = re.sub(
    r'  --bg-message: hsl\(250, 12%, 20%\);',
    r'  --bg-message: hsl(250, 14%, 22%);\n  --bg-code-inline: hsl(250, 14%, 28%);',
    css
)

# Also update ai-input to use the same distinct background
css = css.replace(
    '  background: var(--surface);\n  outline: none;\n  box-shadow: var(--shadow-md);',
    '  background: var(--bg-message);\n  outline: none;\n  box-shadow: var(--shadow-md);'
)

with open('frontend/src/style.css', 'w') as f:
    f.write(css)
