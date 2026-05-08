import os
import re

markdown_path = r"e:\intraget\UI_COMPONENTS_CODE.md"
with open(markdown_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_file = None
current_code = []
in_code = False

for line in lines:
    if line.startswith('## STEP'):
        # Just use a regex to find apps/.. or packages/..
        m = re.search(r'(apps/[^\s()]+|packages/[^\s()]+)', line)
        # Next.js route groups have parens, so we need to match them:
        m = re.search(r'(apps/\S+|packages/\S+)', line)
        if m:
            current_file = m.group(1).rstrip(')')
            # sometimes the line is: apps/web/app/(student)/dashboard/page.tsx
            # If the original line had parens around the WHOLE path, we strip it.
            # E.g. "(apps/web/app/globals.css)"
            if current_file.startswith('('):
                current_file = current_file[1:]
        continue
    
    if line.startswith('```') and not in_code and current_file:
        in_code = True
        current_code = []
        continue
    
    if line.startswith('```') and in_code:
        in_code = False
        if current_file:
            full_path = os.path.join(r"e:\intraget\iib-india", current_file)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as out:
                out.write("".join(current_code))
            print(f"Wrote {full_path}")
            current_file = None
        continue
        
    if in_code:
        current_code.append(line)
