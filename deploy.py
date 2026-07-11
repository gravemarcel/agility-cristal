#!/usr/bin/env python3
"""Deploy Agility Cristal site to GitHub Pages"""
import os, json, urllib.request, subprocess, sys

# Read token from git credentials
with open(os.path.expanduser('~/.git-credentials')) as f:
    cred = f.read().strip()
    token = cred.split(':')[-1].split('@')[0]

website_dir = '/home/marcel/agility-cristal-website'
repo_name = 'agility-cristal'
username = 'marcelgrave'

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json",
    "User-Agent": "Hermes"
}

# Check/create repo
req = urllib.request.Request(
    f"https://api.github.com/repos/{username}/{repo_name}",
    headers=headers
)
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        print(f"✓ Repositório existe: {data['html_url']}")
except urllib.error.HTTPError as e:
    if e.code == 404:
        data = json.dumps({"name": repo_name, "description": "Agility Cristal - Cross Training em Porto Alegre", "private": False}).encode()
        req = urllib.request.Request("https://api.github.com/user/repos", data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            print(f"✓ Repositório criado: {result['html_url']}")
    else:
        print(f"✗ Erro: {e.code} - {e.read().decode()[:200]}")
        sys.exit(1)

# Git commands
cmds = [
    f"cd {website_dir} && git init",
    f"cd {website_dir} && git add .",
    f"cd {website_dir} && git commit -m 'Site Agility Cristal - v1.0'",
    f"cd {website_dir} && git branch -M main",
    f"cd {website_dir} && git remote add origin https://{username}:{token}@github.com/{username}/{repo_name}.git",
    f"cd {website_dir} && git push -u origin main 2>&1",
]

for cmd in cmds:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = result.stdout.strip()[:200]
    err = result.stderr.strip()[:200]
    if result.returncode == 0 or (result.returncode != 0 and 'already exists' in out+err):
        print(f"✓ {cmd.split('&&')[-1].strip()[:60]}...")
        if out: print(f"  {out}")
    else:
        print(f"✗ {cmd.split('&&')[-1].strip()[:60]}...")
        print(f"  {err}")
        # Continue anyway

# Enable GitHub Pages
print("\n--- Ativando GitHub Pages ---")
pages_data = json.dumps({
    "source": {"branch": "main", "path": "/"},
    "build_type": "legacy"
}).encode()
req = urllib.request.Request(
    f"https://api.github.com/repos/{username}/{repo_name}/pages",
    data=pages_data,
    headers=headers,
    method="POST"
)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
        print(f"✓ GitHub Pages ativado!")
except urllib.error.HTTPError as e:
    body = json.loads(e.read())
    print(f"Pages: {body.get('message', '')}")
    if e.code == 409:
        # Already exists, try PUT
        req = urllib.request.Request(
            f"https://api.github.com/repos/{username}/{repo_name}/pages",
            data=pages_data,
            headers=headers,
            method="PUT"
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                print("✓ GitHub Pages atualizado!")
        except:
            pass

print(f"\n📡 SITE ONLINE EM BREVE:")
print(f"   https://{username}.github.io/{repo_name}/")
print(f"   https://github.com/{username}/{repo_name}")
