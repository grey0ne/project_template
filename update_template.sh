while getopts t:n:r: flag
do
    case "${flag}" in
        t) TEMPLATE=${OPTARG};;
        n) PROJECT_NAME=${OPTARG};;
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
        echo "Transforming $i"
    fi
done
mv tmp_templ/.gitignore.template tmp_templ/.gitignore

rsync -r tmp_templ/ $TARGET_DIR/
rm -rf tmp_templ

