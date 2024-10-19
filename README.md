Update project from template
```bash
./update_template.sh -t django_nextjs_template -n <project_name> -r <result_dir> -d <project_domain>
```
Or from the project itself
```bash
./dc updatetemplate
```

Init Digital ocean for project
```bash
./dc initinfra
```
Sadly DO API doesn't have a way to give PG user grants on database so you have to use admin user and copy admin password from DO admin
