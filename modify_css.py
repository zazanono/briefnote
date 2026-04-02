import re

with open('frontend/src/style.css', 'r') as f:
    css = f.read()

# 1. Update :root
root_old = """\
:root {
  --bg-sidebar: hsl(250, 18%, 96%);
  --bg-editor: hsl(250, 20%, 97%);
  --bg-ai: hsl(250, 18%, 96%);
  --bg-page: hsl(255, 15%, 99%);
  --border: oklch(0.88 0.02 280);
  
  --text-main: #111827;
  --text-muted: hsl(250, 10%, 45%);
  --text-light: hsl(250, 15%, 65%);
  
  --surface: hsl(255, 15%, 99%);
  --surface-hover: hsl(250, 30%, 95%);
  --surface-active: hsl(250, 40%, 94%);
  
  --accent: hsl(255, 50%, 68%);
  --accent-hover: hsl(255, 45%, 60%);
  --accent-text: #ffffff;
  --danger: #ef4444;

  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  
  --shadow-sm: 0 1px 2px oklch(0.65 0.06 280 / 0.05);
  --shadow-md: 0 4px 12px oklch(0.65 0.06 280 / 0.08);
}"""

root_new = """\
:root {
  color-scheme: light;
  --bg-sidebar: hsl(250, 18%, 96%);
  --bg-editor: hsl(250, 20%, 97%);
  --bg-ai: hsl(250, 18%, 96%);
  --bg-page: hsl(255, 15%, 99%);
  --border: oklch(0.88 0.02 280);
  
  --text-main: #111827;
  --text-editor: #334155;
  --text-muted: hsl(250, 10%, 45%);
  --text-light: hsl(250, 15%, 65%);
  --text-placeholder: #e2e8f0;
  
  --surface: hsl(255, 15%, 99%);
  --surface-hover: hsl(250, 30%, 95%);
  --surface-active: hsl(250, 40%, 94%);
  --surface-accent: hsl(255, 40%, 96%);
  --surface-accent-hover: hsl(255, 40%, 94%);
  
  --badge-bg: #f1f5f9;
  
  --accent: hsl(255, 50%, 68%);
  --accent-hover: hsl(255, 45%, 60%);
  --accent-text: #ffffff;
  
  --danger: #ef4444;
  --danger-hover: #dc2626;
  --danger-bg: #fef2f2;
  --danger-border: #fca5a5;

  --success: #10b981;
  --warning: #f59e0b;

  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  
  --shadow-sm: 0 1px 2px oklch(0.65 0.06 280 / 0.05);
  --shadow-md: 0 4px 12px oklch(0.65 0.06 280 / 0.08);
  --shadow-page: 0 -4px 12px oklch(0.65 0.06 280 / 0.04), 0 -1px 3px oklch(0.65 0.06 280 / 0.03);
}

[data-theme="dark"] {
  color-scheme: dark;
  --bg-sidebar: hsl(250, 12%, 13%);
  --bg-editor: hsl(250, 12%, 11%);
  --bg-ai: hsl(250, 12%, 13%);
  --bg-page: hsl(250, 12%, 16%);
  --border: hsl(250, 10%, 22%);
  
  --text-main: hsl(250, 10%, 92%);
  --text-editor: hsl(250, 10%, 88%);
  --text-muted: hsl(250, 10%, 65%);
  --text-light: hsl(250, 10%, 45%);
  --text-placeholder: hsl(250, 10%, 30%);
  
  --surface: hsl(250, 12%, 15%);
  --surface-hover: hsl(250, 12%, 19%);
  --surface-active: hsl(250, 12%, 23%);
  --surface-accent: hsl(250, 15%, 18%);
  --surface-accent-hover: hsl(250, 15%, 22%);
  
  --badge-bg: hsl(250, 12%, 23%);
  
  --accent: hsl(255, 60%, 72%);
  --accent-hover: hsl(255, 60%, 77%);
  --accent-text: #111827;
  
  --danger: #ef4444;
  --danger-hover: #f87171;
  --danger-bg: hsl(0, 50%, 18%);
  --danger-border: hsl(0, 50%, 35%);

  --success: #10b981;
  --warning: #f59e0b;

  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.5);
  --shadow-page: 0 -4px 12px rgba(0, 0, 0, 0.3), 0 -1px 3px rgba(0, 0, 0, 0.2);
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --bg-sidebar: hsl(250, 12%, 13%);
    --bg-editor: hsl(250, 12%, 11%);
    --bg-ai: hsl(250, 12%, 13%);
    --bg-page: hsl(250, 12%, 16%);
    --border: hsl(250, 10%, 22%);
    
    --text-main: hsl(250, 10%, 92%);
    --text-editor: hsl(250, 10%, 88%);
    --text-muted: hsl(250, 10%, 65%);
    --text-light: hsl(250, 10%, 45%);
    --text-placeholder: hsl(250, 10%, 30%);
    
    --surface: hsl(250, 12%, 15%);
    --surface-hover: hsl(250, 12%, 19%);
    --surface-active: hsl(250, 12%, 23%);
    --surface-accent: hsl(250, 15%, 18%);
    --surface-accent-hover: hsl(250, 15%, 22%);
    
    --badge-bg: hsl(250, 12%, 23%);
    
    --accent: hsl(255, 60%, 72%);
    --accent-hover: hsl(255, 60%, 77%);
    --accent-text: #111827;
    
    --danger: #ef4444;
    --danger-hover: #f87171;
    --danger-bg: hsl(0, 50%, 18%);
    --danger-border: hsl(0, 50%, 35%);

    --success: #10b981;
    --warning: #f59e0b;

    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.4);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.5);
    --shadow-page: 0 -4px 12px rgba(0, 0, 0, 0.3), 0 -1px 3px rgba(0, 0, 0, 0.2);
  }
}"""
css = css.replace(root_old, root_new)

# 2. Replace hardcoded colors
css = css.replace('background: hsl(255, 40%, 96%);', 'background: var(--surface-accent);')
css = css.replace('background: hsl(255, 40%, 94%);', 'background: var(--surface-accent-hover);')
css = css.replace('background: #dc2626; /* darker red */', 'background: var(--danger-hover);')
css = css.replace('color: #e2e8f0;', 'color: var(--text-placeholder);')
css = css.replace('background: #10b981;', 'background: var(--success);')
css = css.replace('background: #f59e0b;', 'background: var(--warning);')
css = css.replace('color: #334155;', 'color: var(--text-editor);')
css = css.replace('background: #f1f5f9;', 'background: var(--badge-bg);')
css = css.replace('background: #fef2f2; border-color: #fca5a5;', 'background: var(--danger-bg); border-color: var(--danger-border);')
css = css.replace('box-shadow: 0 -4px 12px oklch(0.65 0.06 280 / 0.04), 0 -1px 3px oklch(0.65 0.06 280 / 0.03);', 'box-shadow: var(--shadow-page);')

# 3. Add sidebar footer styles
sidebar_footer_css = """
.sidebar-footer {
  padding: 12px 20px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
}

.theme-toggle {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 6px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.theme-toggle:hover {
  background: var(--surface-hover);
  color: var(--text-main);
}
"""
css += sidebar_footer_css

with open('frontend/src/style.css', 'w') as f:
    f.write(css)
