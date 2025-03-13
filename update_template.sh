#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

while getopts t:n:d:r: flag
do
    case "${flag}" in
        t) TEMPLATE=${OPTARG};;
        n) PROJECT_NAME=${OPTARG};;
        d) PROJECT_DOMAIN=${OPTARG};;
        r) TARGET_DIR=${OPTARG};;
    esac
done

TMP_DIR=$SCRIPT_DIR/tmp_templ
TMP_ENV_DIR=$TMP_DIR/environment
TARGET_ENV_DIR=$TARGET_DIR/environment
TEMPLATE_DIR=$SCRIPT_DIR/$TEMPLATE

echo "Updating $TARGET_DIR with template $TEMPLATE_DIR"
rm -rf $TMP_DIR
cp -r $TEMPLATE_DIR $TMP_DIR
for i in $(find $TMP_DIR);
do
    if test -f "$i"
    then
        sed -i '' "s/<project_name>/$PROJECT_NAME/g" $i
        sed -i '' "s/<project_domain>/$PROJECT_DOMAIN/g" $i
    fi
done
mv $TMP_DIR/.gitignore.template $TMP_DIR/.gitignore # Copy gitingore from template so is doesn't affect template repo

copy_or_remove() {
    local file_path=$1
    if [ ! -f "$TARGET_DIR/$file_path" ]; then
        cp -R "$TMP_DIR/$file_path" "$TARGET_DIR/$file_path"
    else
        rm -rf "$TMP_DIR/$file_path"
    fi
}

copy_or_remove "backend/pyproject.toml"
copy_or_remove "backend/application/project_settings.py"
copy_or_remove "backend/application/urls.py"
copy_or_remove "backend/application/api.py"
copy_or_remove "backend/users"
copy_or_remove "spa/app"

rsync -r $TMP_DIR/ $TARGET_DIR/
cp -n $TMP_ENV_DIR/env.prod.template $TARGET_ENV_DIR/env.prod
rm $TARGET_ENV_DIR/env.prod.template
cp -n $TMP_ENV_DIR/env.stage.template $TARGET_ENV_DIR/env.stage
rm $TARGET_ENV_DIR/env.stage.template
rm -rf $TMP_DIR

touch $TARGET_DIR/.env

cd $TARGET_DIR

if [ ! -d "$TARGET_DIR/.git" ]; then
    git init
fi
if [ ! -d "$TARGET_DIR/deploy" ]; then
    git submodule add git@github.com:grey0ne/django-deploy.git deploy
fi
if [ ! -d "$TARGET_DIR/backend/dataorm" ]; then
    git submodule add git@github.com:grey0ne/dataorm.git backend/dataorm
fi
if [ ! -d "$TARGET_DIR/spa/next_utils" ]; then
    git submodule add git@github.com:grey0ne/next_utils.git spa/next_utils
fi

git submodule update --init --recursive