# django-crud with mongodb as DB

### API's
### Signup
* http://localhost:8000/api/signup)http://localhost:8000/api/signup
* user will make post request with data email, password, name, bio,profile_photo 
* here email will be unique and valid I have implemented checks for it and have written code according to it
* here if every check is passed then the password is hashed using bycrypt and with the above data it is saved in MongoDB. 

### Login
* http://localhost:8000/api/login
* user will make post request with data email, password
* if the email and password both are valid and the email exist then I have sent an access token in response that will require for using further API's

### UPDATE
* http://localhost:8000/api/update
* user will make patch request with the access token received after login and fields to be updated with email(email will not be updated)
* if the access token is valid and if it is not expired then user info will be updated

### Delete
* http://localhost:8000/api/delete
* Only the admin can use this API for deleting any user from Mongodb
* for this case I have kept the user with email "admin@gmain.com" as admin, admin has to log in and then make a delete request passing his access token received after login in headers and the email of the user in the to-be deleted in the body of the request, if the email exists then the user will be deleted from MongoDB

### Logout
* http://localhost:8000/api/logout
* user will make post request with access token and if token is not expired then he will be logged out

### wrote unit test cases in crud app for above features
### [sceenshots of working app](https://github.com/pritamp17/django-crud/tree/main/working%20SS)
