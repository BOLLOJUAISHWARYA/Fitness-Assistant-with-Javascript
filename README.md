# Fitness-Assistant-with-Javascript

The main aim of this Fitness Assistant is to make its users active, fit, and healthy. For this, it offers personalized fitness training that can be done anywhere anytime. It turns your smartphone into a personal fitness trainer, that utilizes media pipe to track your fitness techniques.

## DEMO

https://user-images.githubusercontent.com/59137401/198189046-46423d1b-bc75-4033-9909-5451eed1c623.mp4

## TECH DETAILS

We have used Flask framework to build the application, socketio and zmq for communication , postgres to save the login details of user , mediapipe for tracking.

## FEATURES

    • Face login for the web app
    • Food intake form 
    • Demo of Exercise
    • Tracking the exercise with proper posture with respective device camera
    • Automatic redirection from one exercise to other with a wait timer


## HOW TO USE

![Home](https://user-images.githubusercontent.com/59137401/175223854-d55554ea-cac2-4741-a71d-e942ed5c5523.png)

STEP 1: Please click on register.

![Registration](https://user-images.githubusercontent.com/59137401/175223941-015df08c-1574-4811-943e-3416a3240032.png)

STEP 2: Provide the required details for registration , username should be unique . It may ask to change the username if it already exists.

![login](https://user-images.githubusercontent.com/59137401/175223969-cb66bfb2-e081-4ff9-8cb7-fcd8fae2002c.png)

STEP 3: After successful registration  you will be redirected to the login page, as it is the first time login , you can’t login using face as face is not registered . So, login with password , face registration steps will be provided.

![after_login](https://user-images.githubusercontent.com/59137401/175224058-ec40c557-fa80-4d82-a04c-d1a998abd7e4.png)

STEP 4: You can register for face login by clicking on settings. Below are the options provided after clicking on settings.

![settings](https://user-images.githubusercontent.com/59137401/175224099-ad9d83ac-f79b-46a8-a009-c763568089d8.png)

STEP 5: Click on Capture Face then webcam opens, when you are ready capture the photo ,image will get captured.Make sure the face is clear.

STEP 6: After that in the same page, whenever you want to do exercise fill the details and click next, depending on the intake it redirects to respective page like light/medium/heavy workout.

![workout](https://user-images.githubusercontent.com/59137401/175224241-ab828b22-19c6-4ebe-9cc1-5d20aaf84628.png)

STEP 7: Gives the option to watch the demo of exercise.

![exercise](https://user-images.githubusercontent.com/59137401/175224177-4f55d0bf-7773-41de-92a4-9b3f54148a5b.png)

STEP 8: If you finish watching the demo , click on Try the exercise. Your camera will open.
Before proceeding to exercise make sure your body is completely visible in the camera , make sure nobody is moving around /in front of the camera.


