Instructions:
1. Install docker
2. Run the ```run.sh``` file which should install the flask app, mongo db and redis server
3. The container listens to port 5000 for requests
4. Run the command below to make the request. Modify the file path before:
```
curl --location --request POST '0.0.0.0:5000/upload' \ --form 'csv_data=@"data-2020.txt"'
```
5. You can monitor the log: ```data_app.log```
