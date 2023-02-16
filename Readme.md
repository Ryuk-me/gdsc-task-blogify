## GDSC Blogify Task


## How to run 

```sh

# To run with Docker

clone this repository

move to root directory of the project

and use commands 

$ docker compose build
$ docker compose up

Swagger UI : http://localhost:8009/docs

# To run without Docker

clone the repo

install all the dependencies using command

$ pip install -r .\app\requirements.txt

# also install mongo db and redis (wsl will be required on windows to install redis)

$ uvicorn app.main:app --host 0.0.0.0 --port 8009


```


> Features Impleneted

1. - [X] USER SINGUP
1. - [X] USER AUTHENTICATION USING JWT
1. - [X] Users should be able to create blog posts by providing a title and content.
1. - [X] Users should be able to read, update, and delete their own blog posts.
2. - [X] Users should be able to view a list of all blog posts, including the title, author, and creation date. 

> Bonus Features

1. - [X] Add support for uploading images to blog posts.
2. - [X] Implement pagination for the list of all blog posts. The API should return a specified number of posts per page. Added `limit` to achieve pagination by limiting number of blogs per page
2. - [X] Add support for searching blog posts by title or content.
3. - [X] Implement rate limiting for the authentication and blog post routes to prevent abuse. `[IMPLEMENTED] {16-02-2023}`

```sh

Routes with rate limit

/api/v1/auth/user  time=1 seconds=5
/api/v1/blog/       times=2 seconds=5
/api/v1/blog/all       time=1 seconds=5

To test rate limit

/limit    time=1 seconds=5
```



