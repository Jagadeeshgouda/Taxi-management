# Taxi-management

Taxi fleet management is the comprehensive process of overseeing, coordinating, and optimizing the operations of a taxi fleet. 
It involves a set of tasks, activities, and strategies aimed at ensuring a taxi fleet’s efficient operation and optimizing resource utilization.

***** contains*****
* registration form with authentication and email authorization
* login page
* home page to book the taxi
* car page to view availble cars
* invoice page which will gwnwrate invoice after booking
  
** i used Email authorization in this project through the email we will send OTP to Register user mail Id

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_POST = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your mail id' 
EMAIL_HOST_PASSWORD = 'your password'

# replace your mail id and password
