<h1>Clown management System</h1>


this is a microservice application.

I spent too much time fixing the existing code because somehow it was not working.

I implemented the login from scratch on the authentication service and also the check authentication functionality on the client service.

to run the application first run the authentication service and register users and then log in

the service must have independent virtual environments

first install the required dependencies

``pip install -r requirements.txt``

after that run the services


To test the Authorization service use the following endpoints:

``POST: /register``

``POST: /login``

``
GET: /logout``

``
GET: /current-user
``
the json body:
```
{
    "email": "111@gmail.com",
    "password": "55wtr6"

}
```
To test the Client service do not logout also copy the api key that gets returned by the login endpoint

```
GET: /clients
POSt: /clients
GET: /clients/<id>
PUT;/clients/<id>
```

the json body
```
{
    "contact_name": "smanga",
    "contact_number": "smanga",
    "contact_email": "smanga@gmail.com"
}
```
Please make sure you copy the api_key and in headers put

``
Authorization: api_key
``