# Blog API
An API for simple blog built with Django, Django Rest Framework and Postgres database.
User authentication is provided by Djoser.

API Endpoints allow to sign up and sing in, view all posts and comments, browse comments for specific post, like posts and comments.


## Run server with Docker

- Clone this repo
- In terminal hit `docker-compose run blogserver`
- Close running process with `Ctrl + C`
- Go to the server container with `docker exec -it blogserver bash`
- Migrate database with `python manage.py migrate`
- Run server with `docker-compose up`

## ER Diagram for the database

![blog-api.png](https://github.com/ArturRejment/blog-api/blob/main/static/images/blog-api.png)

## Returning objects

### User object
```json
{
    "user": {
        "id": 2,
        "username": "marco123",
        "first_name": "Marco",
        "last_name": "Polo",
        "bio": "",
        "imageURL": "http://127.0.0.1:7000/static/images/default.png",
        "following": false
    }
}
```

### Post object
```json
{
    "post": {
        "id": 1,
        "author": {
            "id": 1,
            "username": "marco123",
            "first_name": "Marco",
            "last_name": "Polo",
            "bio": "",
            "imageURL": "http://127.0.0.1:7000/static/images/default.png",
            "following": false
        },
        "title": "Space",
        "content": "Space is the boundless three-dimensional extent in which objects and events have relative position and direction.[1] In classical physics, physical space is often conceived in three linear dimensions, although modern physicists usually consider it, with time, to be part of a boundless four-dimensional continuum known as spacetime.",
        "imageURL": "http://127.0.0.1:7000/static/images/post_pics/spaghetti_bJniGRs.png",
        "tagList": [
            "Bootstrap",
            "Python"
        ],
        "favorited": false,
        "favoritesCount": 0
    }
}
```

### Multiple Posts objects
```json
{
    "posts": [
        {
            "id": 2,
            "author": {
                "id": 2,
                "username": "artur",
                "first_name": "artur",
                "last_name": "rejment",
                "bio": "",
                "imageURL": "http://127.0.0.1:7000/static/images/default.png",
                "following": false
            },
            "title": "Rekrutacja",
            "content": "The world is so big, it is beautiful",
            "imageURL": "http://127.0.0.1:7000/static/images/default.png",
            "tagList": [
                "Django",
                "React"
            ],
            "favorited": false,
            "favoritesCount": 0
        },
        {
            "id": 1,
            "author": {
                "id": 1,
                "username": "marco123",
                "first_name": "Marco",
                "last_name": "Polo",
                "bio": "",
                "imageURL": "http://127.0.0.1:7000/static/images/default.png",
                "following": false
            },
            "title": "Space",
            "content": "Space is the boundless three-dimensional extent in which objects and events have relative position and direction.[1] In classical physics, physical space is often conceived in three linear dimensions, although modern physicists usually consider it, with time, to be part of a boundless four-dimensional continuum known as spacetime.",
            "imageURL": "http://127.0.0.1:7000/static/images/post_pics/spaghetti_bJniGRs.png",
            "tagList": [],
            "favorited": false,
            "favoritesCount": 0
        }
    ],
    "postsCount": 2
}
```

### Comment object

```json
{
    "comment": {
        "id": 3,
        "post": 3,
        "author": {
            "id": 2,
            "username": "marco123",
            "first_name": "Marco",
            "last_name": "Polo",
            "bio": "",
            "imageURL": "http://127.0.0.1:7000/static/images/default.png",
            "following": false
        },
        "content": "Great article",
        "favorited": false,
        "favorites_count": 0
    }
}
```

### Multiple Comments object

```json
{
    "comments": [
        {
            "id": 1,
            "post": 2,
            "author": {
                "id": 2,
                "username": "marco123",
                "first_name": "Marco",
                "last_name": "Polo",
                "bio": "",
                "imageURL": "http://127.0.0.1:7000/static/images/default.png",
                "following": false
            },
            "content": "Great article",
            "favorited": false,
            "favorites_count": 0
        },
        {
            "id": 2,
            "post": 2,
            "author": {
                "id": 2,
                "username": "marco123",
                "first_name": "Marco",
                "last_name": "Polo",
                "bio": "",
                "imageURL": "http://127.0.0.1:7000/static/images/default.png",
                "following": false
            },
            "content": "Great article",
            "favorited": false,
            "favorites_count": 0
        }
    ],
    "commentsCount": 2
}
```

### Tags list
```json
{
    "tags": [
        {
            "tag": "Django"
        },
        {
            "tag": "React"
        },
        {
            "tag": "Bootstrap"
        },
        {
            "tag": "Python"
        }
    ]
}
```

## Endpoints

- `post`
  - `GET` Returns all [posts](#multiple-posts-objects) on the service
    - Allowed url params: `author`, `tag`
    - Example: `post?author=marco&tag=Django` returns all posts whom author is marco and they are about Django
  - `POST` Creates new [post](#post-object)

- `post/<id>`
  - `GET` Returns [post](#post-object) specified by id
  - `PUT` Allows to update post specified by id
  - `DELETE` Allows to delete post specified by id

- `post/<id>/comments`
  - `GET` Returns comments for post specified by id specified
  - `POST` Create comment for post specified by id

- `post/<id>/favorite` (Authentication required)
  - `POST` Adds [post](#post-object) specified by id to favorites
  - `DELETE` Deletes [post](#post-object) specified by id from favorites

- `user/<username>`
  - `GET` Returns [user](#user-object) object specified by username

- `comment/<id>/favorite`
  - `DELETE` Returns [comment](#comment-object) object, deletes comment from favorite
  - `POST` Returns [comment](#comment-object) object, adds comment to favorite

- `tags`
  - `GET` Returns [tags list](#tags-list) that contains all available tags
