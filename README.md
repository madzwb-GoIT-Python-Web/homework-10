# homework-10
homework-10

Please specify all PASSWORD and SECRET options.
To use Mongo to Postgres data migration please specify all MONGO_* options.
Scenarios:
        python manage.py scrap2json
        python manage.py json2pg
    or:
        python manage.py scrap2json
        python manage.py json2mg
        python manage.py mg2pg
PS:
    not all cli options are working(-d --data). Its is in TODO list.


DJANGO_SECRET_KEY   = 
# DJANGO_SECRET_KEY_FILE  = secrets/django.key

ADMIN_USERNAME  = admin
ADMIN_PASSWORD  = 
ADMIN_EMAIL     = admin@locahost
# ADMIN_PASSWORD_FILE = secrets/admin.key

POSTGRES_NAME           = quotes
POSTGRES_USER           = postgres
POSTGRES_PASSWORD       = 
POSTGRES_HOST           = 127.0.0.1
POSTGRES_PORT           = 5432
# POSTGRES_PASSWORD_FILE  = secrets/postgres.key

MONGODB_USER            = madzwb
MONGODB_NAME            = homework-8_1
MONGODB_PASSWORD        = 
MONGODB_DOMAIN          = cluster.y1pqhvz.mongodb.net
# MONGODB_PASSWORD_FILE   = secrets/mongodb.key


# MAIL_PASSWORD_FILE = secrets/mail.key
MAIL_FROM_NAME  = "Quotes"
MAIL_USERNAME   = "madzwb@meta.ua"
MAIL_PASSWORD   = 
MAIL_FROM       = "madzwb@meta.ua"
MAIL_PORT       = 465
MAIL_SERVER     = "smtp.meta.ua"
MAIL_STARTTLS   = False
MAIL_SSL_TLS    = True
USE_CREDENTIALS = True
VALIDATE_CERTS  = True


pip install toml && python -c 'import toml; c = toml.load("pyproject.toml"); print("\n".join(c["project"]["dependencies"]))' | pip download -r /dev/stdin  --dest=dest 