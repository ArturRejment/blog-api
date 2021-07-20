# Blog API
An API for simple blog built with Django, Django Rest Framework and Postgres database.
User authorization is provided by Djoser.

API Endpoints allow to sign up and sing in, view all posts and comments, browse comments for specific post, like posts and comments.

## Run server with Docker

- Clone this repo
- In terminal hit `docker-compose run blogserver`
- Close running process with `Ctrl + C`
- Go to the server container with `docker exec -it blogserver bash`
- Migrate database with `python manage.py migrate`
- Run server with `docker-compose up`

## Endpoints

- `post/`
  - `GET` Returns all posts on the service
  - `POST` Creates new post

- `post/<id>/`
  - `PUT` Allows to update post specified by id
  - `DELETE` Allows to delete post specified by id

- `post/<id>/comments`
  - `GET` Returns comments for post specified by id
  - `POST` Create comment for post specified by id

- `post/<id>/likes/`
  - `GET` Returns all people who liked post specified by id

- `post/<id>/like/` (Authentication required)
  - `POST` Likes post specified by id by currently logged user

- `comments/`
  - `GET` Returns all comments on the service

- `comment/<id>/like/` (Authentication required)
  - `POST` Likes comment specified by id by currently logged user

## Examplary responses

### /post/8/
```json
{
    "id": 8,
    "author": {
        "username": "marco123",
        "first_name": "Marco",
        "last_name": "Polo",
        "imageURL": "http://127.0.0.1:7000/static/images/default.png"
    },
    "title": "Spaghetti Bolognese",
    "content": "Cook the ground beef in a large pot over high heat, stirring quickly and constantly until completely browned 7 to 10 minutes. Stir the onion into the beef; cook and stir until the onion begins to turn translucent, about 5 minutes more. Drain excess grease from meat mixture. Add the mushroom to the mixture; allow to cook until it begins to soften, 1 to 2 minutes. Pour the diced tomatoes and tomato soup into the pot, stir, reduce heat to medium, and bring the mixture to a simmer.",
    "number_of_likes": 1,
    "imageURL": "http://127.0.0.1:7000/static/images/post_pics/spaghetti_qKbK0jq.png"
}
```