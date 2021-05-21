echo "starting server and proccessor"
(nodemon --exec flask run & nodemon --exec python3 process.py)
echo  "exiting"
