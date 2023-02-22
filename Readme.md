
# SOCIAL-HUB

[![Social Hub API](https://github.com/Nkasi-e/social-api/actions/workflows/build-deploy.yml/badge.svg)](https://github.com/Nkasi-e/social-api/actions/workflows/build-deploy.yml) <a href='https://coveralls.io/github/Nkasi-e/social-api?branch=readme'><img src='https://coveralls.io/repos/github/Nkasi-e/social-api/badge.svg?branch=readme' alt='Coverage Status' /></a>

## _An API that allows users to create contents_

### _This API was build using the python fastapi framework_

## Features

- [x] Anybody can create an account and become a user.
- [x] Authenticated users can login to their individual account.
- [x] Authenticated users can create posts.
- [x] Authenticated users can read personal posts.
- [x] Authenticated users can view everybody's posts.
- [x] Authenticated users can view a specific post.
- [x] Authenticated users can delete personal post.
- [x] Authenticated users can update personal post.
- [x] Authenticated users can can like any post of their choice.
- [x] Authenticated users can can unlike any post of their choice.
- [x] Can get a specific user by Id.
- [x] Users have the ability to search for keywords and get back response if it matches any keyword in the post content available on the database
- [x] Users have the ability to set pagination, default pagination is set to 10
<!-- - Note: The unchecked box means those particular feature are not ready yet but still under production or building.
- More features may still be added to the `Diary API` as an update, until it is fully ready. -->

## API Documentation

API documentation:

## Models <br>

### Users

| field      | data_type | constraints       | validation                                                                                                |
| ---------- | --------- | ----------------- | --------------------------------------------------------------------------------------------------------- |
| id         | Object    | required          | None                                                                                                      |
| email      | string    | required          | unique, email must conform to email (example: johndoe@gmail.com)                                          |
| password   | string    | required          | pasword must contain at least one uppercase, one lowercase, one number, and must be at least 8 characters |
| created_at | timestamp | automatically set |

### Posts

| field      | data_type | constraints                          | validation |
| ---------- | --------- | ------------------------------------ | ---------- |
| id         | integer   | required                             | None       |
| title      | string    | required                             | None       |
| content    | string    | required                             | None       |
| publised   | boolean   | optional, default value set to false | None       |
| created_at | timestamp | required, automatically set          |            |

### Likes

| field   | data_type | constraints | validation |
| ------- | --------- | ----------- | ---------- |
| user_id | integer   | required    | None       |
| post_id | integer   | required    | None       |

### Home Page

- Route: /
- Method: GET
- Header
  - Authorization: None
- Responses: Success

```json
{
  "message": "Welcome to Social Hub"
}
```

### Signup User <br>

- Route: /users
- Method: POST
- Header
  - Authorization: None
- Body:

```json
{
  "email": "johndoe@example.com",
  "password": "Password123"
}
```

- Responses: Success

```json
{
  "id": 1,
  "email": "johndoe@example.com",
  "created_at": "2023-02-05T15:29:24.712Z"
}
```

### Login User

- Route: /login
- Method: POST
- Body:

```json
{
  "username": "johndoe@example.com",
  "password": "Password123"
}
```

- Responses: Success

```json
{
  "access_token": "accesstokenexample&8ofiwhb.fburu276r4ufhwu4.o82uy3rjlfwebj",
  "token_type": "Bearer"
}
```

### Create Post

- Route: /posts
- Method: POST
- Header
  - Authorization: Bearer {token}
- Body:

```json
{
  "title": "string",
  "content": "string",
  "published": true
}
```

- Responses: Success

```json
{
  "title": "string",
  "content": "string",
  "published": true,
  "id": 0,
  "created_at": "2023-02-05T19:02:41.204Z",
  "owner_id": 0,
  "owner": {
    "id": 0,
    "email": "user@example.com",
    "created_at": "2023-02-05T19:02:41.204Z"
  }
}
```

### Get Post

- Route: /posts
- Method: GET
- Header
  - Authorization: Bearer {token}
- Body:

```json
[
  {
    "Post": {
      "title": "string",
      "content": "string",
      "published": true,
      "id": 4,
      "created_at": "2023-02-05T19:10:08.030Z",
      "owner_id": 4,
      "owner": {
        "id": 4,
        "email": "user@example.com",
        "created_at": "2023-02-05T19:10:08.030Z"
      }
    },
    "likes": 0
  }
  {
    "Post": {
      "title": "string",
      "content": "string",
      "published": true,
      "id": 1,
      "created_at": "2023-02-05T19:10:08.030Z",
      "owner_id": 2,
      "owner": {
        "id": 2,
        "email": "johndoe@example.com",
        "created_at": "2023-02-05T19:10:08.030Z"
      }
    },
    "likes": 4
  }
  {
    "Post": {
      "title": "string",
      "content": "string",
      "published": true,
      "id": 3,
      "created_at": "2023-02-05T19:10:08.030Z",
      "owner_id": 2,
      "owner": {
        "id": 2,
        "email": "user@example.com",
        "created_at": "2023-02-05T19:10:08.030Z"
      }
    },
    "likes": 2
  }
]
```

## Getting Started

### Prerequisites

In order to  run this project locally, you would need to have the following installed on your local machine.

- Python ^3.10,
- PostgreSQL
- Docker - optional

### Installation

- Clone this repository

```
git clone [https://github.com/Nkasi-e/social-api.git]
```

- update env with .env.example.txt
- Download all dependecies using ```pip install -r requirements.txt``` or ```pipenv install``` that's if you have pipenv installed already on your machine
- run uvicorn app.main:app --reload <hr>

