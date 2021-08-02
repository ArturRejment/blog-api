Authentication for this project is provided by Djoser. Default fiedl used for auhtentication is username. After you obtain auth_token you should send it as header: `Authorization: Token <your_auth_token>`.

## Login
In order to log in use endpoint `token/login/` with `POST` method.
You should send `username` and `password` fields as x-www-form-urlencoded
As respone you will recieve `auth_token`. Keep it and send with other requests in headers as long as user is logged in.

## Register
To register new user use endpoint `users/` with `POST` method.

- Required fields to send in body as x-www-form-urlencoded:
  - username
  - email
  - first_name
  - last_name
  - password
  - re_password
- Optional fields:
  - user_pic
  - phone
  - bio
  - github_link
  - linkedin_link
  - facebook_link

## Logout

To logout user and close current session use endpoint `token/logout/` with `auth_token` as header. This action will disable this auth_token, so it will be no longer valid. In order to obtain new token you should login again.

## Me

To obtain information about currently logged user use `users/me/` endpoint with `GET` method. It will return User instance based on the auth_token.
