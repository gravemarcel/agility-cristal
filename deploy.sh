#!/bin/bash
TOKEN="$1"

# Create GitHub repo
curl -s -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"name":"agility-cristal","description":"Agility Cristal - Cross Training em Porto Alegre","homepage":"https://marcelgrave.github.io/agility-cristal","private":false}' \
  https://api.github.com/user/repos

# Init git
cd /home/marcel/agility-cristal-website
git init
git add .
git commit -m "Site Agility Cristal - v1.0"
git branch -M main

# Push
git remote add origin https://marcelgrave:$TOKEN@github.com/marcelgrave/agility-cristal.git
git push -u origin main

echo ""
echo "=== FEITO! ==="
