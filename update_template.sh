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

rsync -r $TMP_DIR/ $TARGET_DIR/
cp -n $TMP_DIR/deploy/env.prod.template $TARGET_DIR/deploy/env.prod
rm $TARGET_DIR/deploy/env.prod.template
cp -n $TMP_DIR/deploy/env.stage.template $TARGET_DIR/deploy/env.stage
rm $TARGET_DIR/deploy/env.stage.template
cp -n $TMP_DIR/spa/next.config.mjs.template $TARGET_DIR/spa/next.config.mjs
rm $TARGET_DIR/spa/next.config.mjs.template
rm -rf $TMP_DIR

