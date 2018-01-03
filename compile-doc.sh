#!/usr/bin/env bash

# Remove everything except this script
find . -type f -not -name 'compile-doc.sh' -not -path '*/\.*' -print0 | xargs -0 rm --
rm -R -- */
# Checkout whatever is necessary to compile the doc (from master branch)
git checkout master docs geextract 
git reset HEAD
cd docs
make html
cd ..
mv -f docs/_build/html/* .
rm -rf geextract docs
git add -A
git commit -m "Generated doc for gh-pages for `git log master -1 --pretty=short --abbrev-commit`"
git push origin gh-pages
