# A sample flask app with below requirements

Write a small HTTP service that implements a RESTful API that stores a message and returns the SHA256 hash of that message to the user. The service must also be able to retrieve the message using the hash. Feel free to use the language you are most comfortable with!



You will need to implement the following endpoints:



 ## /messages

Accepts a JSON message as a POST. The message should adhere to the following format:

```

{

  “message”: “this is a sample message!”

}

```

The contents of the message should be a string.



The response should contain the SHA256 of the string content of the original message as a hexadecimal string. It should resemble the following:

```

{

   “digest” : “bdfcba37390f1dc3d871011777098dab32c8dd9542b56291268ed950c8b58ba7”

}

```




## /messages/<hash>

Accepts the SHA256 of a message as a GET parameter and returns the content of the original message as a string. A request to a non-existent SHA256 hash should return a 404 along with an error message.



A successful response should resemble the following:



```

{

  “message”: “this is a sample message!”

}

```



An unsuccessful response should respond with the following JSON:

```

{

  “error”: “unable to find message”,

“message_sha256”: “abc123”

}

```



## /messages/<hash>

The /messages endpoint also accepts the SHA256 hash of a message with a DELETE method which will delete the message if it exists.



The API should return 200 OK if the message was deleted or if the message did not exist. It should return the appropriate error code if the API encounters a problem while attempting to delete the message.




## /metrics

Handle a GET request that retrieves runtime metrics from your service. The format and content is up to you, but you should include any measurements you would want to see when monitoring this service in production.

## Example

Let’s say you expose port 8080:

```shell

$ curl -X POST -H "Content-Type: application/json" -d '{"message": "foo"}'

http://localhost:8080/messages

{

   "digest": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"

}

```



You can calculate that your result is correct on the command line:

```shell

$ echo -n "foo" | shasum -a 256 2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae -

```



You can now query your service for the original message:

```shell

$ curl http://localhost:8080/messages/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f9

8a5e886266e7ae

{

   "message": "foo"

}

$ curl -i http://localhost:8080/messages/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

aaaaaaaaaaaaaa HTTP/1.0 404 NOT FOUND Content-Type: application/json Content-Length: 36

Server: Werkzeug/0.11.5 Python/3.5.1 Date: Wed, 31 Aug 2016 14:21:11 GMT

{

   "error": "unable to find message",

   “message_sha256”: “aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

aaaaaaaaaaaaaa”

}
