docker-compose -f docker-compose.staging.yml up -d --build
docker-compose -f docker-compose.staging.yml exec web python3 manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python3 manage.py collectstatic