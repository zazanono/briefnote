import re

with open('frontend/src/style.css', 'r') as f:
    css = f.read()

# Remove the bad bg-message and bg-code-inline additions
css = re.sub(r'\n  --bg-message: #ffffff;', '', css)
css = re.sub(r'\n  --bg-code-inline: hsl\(250, 20%, 94%\);', '', css)
css = re.sub(r'\n  --bg-message: hsl\(250, 14%, 18%\);', '', css)
css = re.sub(r'\n  --bg-code-inline: hsl\(250, 14%, 26%\);', '', css)

# Revert ai-message background
css = css.replace(
    '  background: var(--bg-message);',
    '  background: var(--surface);'
)

css = css.replace(
    '  background-color: var(--bg-code-inline);',
    '  background-color: var(--surface-hover);'
)

# Re-add the dropdown menu css!
dropdown_css = """
.theme-menu-container {
  position: relative;
}

.theme-menu {
  position: absolute;
  bottom: calc(100% + 8px);
  right: 0;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  padding: 4px;
  min-width: 160px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  z-index: 50;
}

.theme-menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 8px 12px;
  border: none;
  background: transparent;
  color: var(--text-main);
  font-size: 13px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  text-align: left;
  transition: background 0.15s;
}

.theme-menu-item:hover {
  background: var(--surface-hover);
}

.theme-menu-item.active {
  background: var(--surface-active);
  font-weight: 500;
}

.theme-menu-item svg {
  color: var(--text-muted);
}
"""

if ".theme-menu-container" not in css:
    css += dropdown_css

with open('frontend/src/style.css', 'w') as f:
    f.write(css)
