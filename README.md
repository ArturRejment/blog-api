# Blog API
An API for simple blog built with Django, Django Rest Framework and Postgres database.
User authentication is provided by Djoser.

API Endpoints allow to sign up and sing in, view all posts and comments, browse comments for specific post, like posts and comments.

## Run server with Docker

- Clone this repo
- In terminal hit `docker-compose run blogserver`
- Close running process with `Ctrl + C`
- Run server with `docker-compose up`
- Open new terminal
- Go to the server container with `docker exec -it blogserver bash`
- Migrate database with `python manage.py migrate`
- Now you can [load test data](#load-test-data-to-your-database)
- And create superuser with `python manage.py createsuperuser`

## ER Diagram for the database

![blog-api1.png](https://github.com/ArturRejment/blog-api/blob/main/static/images/blog-api1.png)

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
        "github_link": "https://github.com/",
        "linkedin_link": "https://www.linkedin.com/feed/",
        "facebook_link": "https://www.facebook.com/",
        "following": false
    }
}
```

### Multiple Users Objects
```json
{
    "users": [
        {
            "id": 5,
            "username": "agi324",
            "first_name": "Agata",
            "last_name": "Kowalska",
            "bio": "Agata K. | Student | Photographer | Cat Lover",
            "imageURL": "http://127.0.0.1:7000/static/images/user_pics/person1.jpg",
            "github_link": "https://github.com/",
            "linkedin_link": "https://www.linkedin.com/feed/",
            "facebook_link": "https://www.facebook.com/",
            "following": false
        },
        {
            "id": 4,
            "username": "tom23",
            "first_name": "Tomas",
            "last_name": "Faster",
            "bio": "Hi, I'm Tomas and I'm from Germany. Backend developer and Gym lover. Feel free to dm me!",
            "imageURL": "http://127.0.0.1:7000/static/images/user_pics/person2.jpg",
            "github_link": "https://github.com/",
            "linkedin_link": "https://www.linkedin.com/feed/",
            "facebook_link": "https://www.facebook.com/",
            "following": false
        }
    ]
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
            "github_link": "https://github.com/",
            "linkedin_link": "https://www.linkedin.com/feed/",
            "facebook_link": "https://www.facebook.com/",
            "following": false
        },
        "title": "Space",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "content": "Space is the boundless three-dimensional extent in which objects and events have relative position and direction.[1] In classical physics, physical space is often conceived in three linear dimensions, although modern physicists usually consider it, with time, to be part of a boundless four-dimensional continuum known as spacetime.",
        "imageURL": "http://127.0.0.1:7000/static/images/post_pics/spaghetti_bJniGRs.png",
        "createdAt": "2021-07-31T16:01:53.829804+00:00",
        "next_post_id": 2,
        "previous_post_id": null,
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
                "github_link": "https://github.com/",
                "linkedin_link": "https://www.linkedin.com/feed/",
                "facebook_link": "https://www.facebook.com/",
                "following": false
            },
            "title": "Rekrutacja",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "content": "The world is so big, it is beautiful",
            "imageURL": "http://127.0.0.1:7000/static/images/default.png",
            "createdAt": "2021-07-31T16:01:53.829804+00:00",
            "next_post_id": 3,
            "previous_post_id": 1,
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
                "github_link": "https://github.com/",
                "linkedin_link": "https://www.linkedin.com/feed/",
                "facebook_link": "https://www.facebook.com/",
                "following": false
            },
            "title": "Space",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "content": "Space is the boundless three-dimensional extent in which objects and events have relative position and direction.[1] In classical physics, physical space is often conceived in three linear dimensions, although modern physicists usually consider it, with time, to be part of a boundless four-dimensional continuum known as spacetime.",
            "imageURL": "http://127.0.0.1:7000/static/images/post_pics/spaghetti_bJniGRs.png",
            "createdAt": "2021-07-31T16:01:53.829804+00:00",
            "next_post_id": 2,
            "previous_post_id": null,
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
            "github_link": "https://github.com/",
            "linkedin_link": "https://www.linkedin.com/feed/",
            "facebook_link": "https://www.facebook.com/",
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
                "github_link": "https://github.com/",
                "linkedin_link": "https://www.linkedin.com/feed/",
                "facebook_link": "https://www.facebook.com/",
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
                "github_link": "https://github.com/",
                "linkedin_link": "https://www.linkedin.com/feed/",
                "facebook_link": "https://www.facebook.com/",
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

- ### users/
  - `POST` Creates new user

- ### token/login/
  - `POST` Allows to log in

- ### post
  - `GET` Returns all [posts](#multiple-posts-objects) on the service
    - This endpoint makes use of pagination. The default size is 10 posts per page
    - Allowed url params: `author`, `tag`, `page`
    - Example: `post?author=marco&tag=Django` returns all posts whom author is marco and they are about Django
    - Example: `post?page=3` returns 10 posts on 3rd page
  - `POST` Creates new [post](#post-object)

- ### post/\<id>
  - `GET` Returns [post](#post-object) specified by id
  - `PUT` Allows to update post specified by id
  - `DELETE` Allows to delete post specified by id

- ### post/\<id>/comments
  - `GET` Returns comments for post specified by id specified
  - `POST` Create comment for post specified by id

- ### post/\<id>/favorite (Authentication required)
  - `POST` Adds [post](#post-object) specified by id to favorites
  - `DELETE` Deletes [post](#post-object) specified by id from favorites

- ### user/\<username>
  - `GET` Returns [user](#user-object) object specified by username

- ### user/\<username>/fav_posts
  - `GET` Returns [posts](#multiple-posts-objects) that user (specified by username) added to favorites

- ### user/\<username>/fav_comments
  - `GET` Returns [comments](#multiple-comments-object) that user (specified by username) added to favorites

- ### top_users
  - `GET` Returns top 3 [users](#multiple-users-objects)

- ### comment/\<id>/favorite
  - `DELETE` Returns [comment](#comment-object) object, deletes comment from favorite
  - `POST` Returns [comment](#comment-object) object, adds comment to favorite

- ### tags
  - `GET` Returns [tags list](#tags-list) that contains all available tags

## Load test data to your database

```python
# load data for users
python manage.py loaddata users

# load data for tags
python manage.py loaddata tags

# load data for posts
python manage.py loaddata posts
```
