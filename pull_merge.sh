#!/bin/zsh

# UPDATE THIS WITH YOUR BRANCH NAME
BRANCH_NAME="noah"

git checkout main
git pull upstream main
git push origin main
git checkout $BRANCH_NAME
git merge main