with open('frontend/src/style.css', 'r') as f:
    css = f.read()

# Make sure --bg-message is in Light mode
if '--bg-message: #ffffff;' not in css:
    css = css.replace(
        '  --surface: hsl(255, 15%, 99%);',
        '  --surface: hsl(255, 15%, 99%);\n  --bg-message: #ffffff;\n  --bg-code-inline: hsl(250, 20%, 94%);'
    )

# Make sure --bg-message is in Dark mode
if '--bg-message: hsl(250, 14%, 22%);' not in css:
    css = css.replace(
        '  --surface: hsl(250, 12%, 15%);',
        '  --surface: hsl(250, 12%, 15%);\n  --bg-message: hsl(250, 14%, 22%);\n  --bg-code-inline: hsl(250, 14%, 28%);'
    )

# Update AI message background
css = css.replace(
    '  background: var(--surface);\n  border: 1px solid var(--border);',
    '  background: var(--bg-message);\n  border: 1px solid var(--border);'
)

# Update ai-input wrapper
css = css.replace(
    '  background: var(--surface);\n  outline: none;\n  box-shadow: var(--shadow-md);',
    '  background: var(--bg-message);\n  outline: none;\n  box-shadow: var(--shadow-md);'
)

# Update inline code block
css = css.replace(
    '  background-color: var(--surface-hover);\n  border-radius: 4px;\n  font-family: \'Courier New\', Courier, monospace;',
    '  background-color: var(--bg-code-inline);\n  border-radius: 4px;\n  font-family: \'Courier New\', Courier, monospace;'
)

with open('frontend/src/style.css', 'w') as f:
    f.write(css)
