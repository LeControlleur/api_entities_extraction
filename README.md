# ENTITIES EXTRACTION




## Description of directory structure

- `files` : This directory contains the tests topic files and the database file. You can create here others files that will be used by the tool
- `test` : Dorectory of the differents test files
- `utils` : Thius directory contains the main python files used for the extraction and the statistics processing
- `app.py` : API server file
- `dechiffrement.py` : File used for decrypt the topic
- `.env` : Environment variables
- `dockerfile` : Docker file for the creation if the container
- `log_book.md` : Log book explaing the differents steps for the creation of this API




## Environment settings

You can install the required packages listed in `requirements.txt`

```
pip install -r requirements.txt
```

## Test the application

All the test files are in the directory `test`. You can launch the test discovery and launch the found tests using the following command
```
python3 -m pytest
```

## Start the server

Open the root folder in the terminal. Then, you can directly start the server by 
```
python3 app.py
```

After that, the server should be running.You can request the API using your preferred client. The server is available on the port 5000 of the local IP address.

So the API URL is : 127.0.0.1:5000

The request should use JSON format with the following template : 
```
    {
        "content" : "_your text_"
    }
```

## Dockerize the solution

Ther is a dockerfile at the root of the folder. It contains the commands for creating a container based on Nginx and python images and copy the files into this container.
The following command will build a container :
```
docker build -t perfectmemory .
```

The name of the container is **perfectmemory**.

You have to wait that the container creation is finished and all is OK.

After that, you can just run the following command for launch the API and bind the container to the port 80 of your machine.

```
docker run -it -p 80:5000 perfectmemory
```
