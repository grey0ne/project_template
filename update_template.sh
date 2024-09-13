while getopts t:n:d:r: flag
do
    case "${flag}" in
        t) TEMPLATE=${OPTARG};;
        n) PROJECT_NAME=${OPTARG};;
        d) PROJECT_DOMAIN=${OPTARG};;
        r) TARGET_DIR=${OPTARG};;
    esac
done

rm -rf tmp_templ
cp -r $TEMPLATE tmp_templ
for i in $(find tmp_templ);
do
    if test -f "$i"
    then
        sed -i '' "s/<project_name>/$PROJECT_NAME/g" $i
        sed -i '' "s/<project_domain>/$PROJECT_DOMAIN/g" $i
    fi
done
mv tmp_templ/.gitignore.template tmp_templ/.gitignore

rsync -r tmp_templ/ $TARGET_DIR/
cp -n tmp_templ/dev-scripts/env.prod.template $TARGET_DIR/dev-scripts/env.prod
rm $TARGET_DIR/dev-scripts/env.prod.template
cp -n tmp_templ/dev-scripts/env.stage.template $TARGET_DIR/dev-scripts/env.stage
rm $TARGET_DIR/dev-scripts/env.stage.template
rm -rf tmp_templ

