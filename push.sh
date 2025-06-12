#!/bin/bash

echo "# project-redis" >> README.md
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:Deni4h/project-redis.git
git push -u origin main
