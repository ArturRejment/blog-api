Post object is a form of an article. It's a longer text about specific topic.

## Retrieve all posts
In order to retrieve all posts use `post` endpoint with `GET` method. This endpoint makes use of pagination, so all posts splitted on different pages.
> Authentication is not required.
- Every page contains 10 posts sorted by the creation time.
- To retrieve other pages add `page` as url param.
  - Example: `post?page=3` will return 10 posts from 3rd page.
- If you specify page number that does not exists API will return 1st page.
- You can also specify other params: `author` and `tag`
  - Example: `post?author=marco&tag=Django` will return all posts whom author is marco and they are about Django

## Retrieve specific post
To retrieve specific post use `post/<id>` endpoint with `GET` method.
> Authentication is not required.

## Add post to favorite
In order to add post to favorite use `post/<id>/favorite` with `POST` method.
> Authentication is required.

## Remove post from favorite
In order to remove post from favorite use `post/<id>/favorite` with `DELETE` method.
> Authentication is required.
