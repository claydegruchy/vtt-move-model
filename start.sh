echo "starting server and proccessor"
export FLASK_APP=server.py
(nodemon --exec python3 process.py -nr & nodemon --exec flask run)
echo  "exiting"
