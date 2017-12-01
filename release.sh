#!/bin/bash

#get highest tag number
VERSION=`git describe --abbrev=0 --tags`

[[ -z $VERSION ]] && VERSION="0.0.1"

#replace . with space so can split into an array
VERSION_BITS=(${VERSION//./ })

#get number parts and increase last one by 1
VNUM1=${VERSION_BITS[0]}
VNUM2=${VERSION_BITS[1]}
VNUM3=${VERSION_BITS[2]}
VNUM3=$((VNUM3+1))

#create new tag
NEW_TAG="$VNUM1.$VNUM2.$VNUM3"

echo "Updating $VERSION to $NEW_TAG"
echo "__version__ = '$NEW_TAG'" > loony/version.py
git commit -am "Updating to Version $NEW_TAG"
#get current hash and see if it already has a tag
GIT_COMMIT=`git rev-parse HEAD`
NEEDS_TAG=`git describe --contains $GIT_COMMIT 2>/dev/null`

#only tag if no tag already (would be better if the git describe command above could have a silent option)
if [ -z "$NEEDS_TAG" ]; then
    echo "Tagged with $NEW_TAG (Ignoring fatal:cannot describe - this means commit is untagged) "
    git tag $NEW_TAG
    pyinstaller loony/main.py --onefile --clean -p ./loony -n loony_${NEW_TAG}_macos --hidden-import=Queue
    rm dist/loony
    ln -s dist/loony_${NEW_TAG}_macos dist/loony
    git add dist/loony_${NEW_TAG}_macos
    git commit -am "Adding new binary: loony_${NEW_TAG}_macos"
    git push --tags
    git push
else
    echo "Already a tag on this commit"
fi
