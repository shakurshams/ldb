sudo docker-compose -f docker-compose.yml up --build --detach
sudo docker exec ldb_web_1 celery -A data_app.config worker --loglevel=INFO -Q enrich,db
# sudo docker exec -d ldb_web_1 celery -A data_app.config worker --loglevel=INFO -Q enrich,db