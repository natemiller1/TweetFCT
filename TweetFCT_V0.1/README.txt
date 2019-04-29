This is a file explaining how to run the FactomTweets Web App using the docker
compose image.

Prerequisites/Setup:
--> Make sure docker is installed on whatever machine you are running. If you
    have not installed docker go to https://docs.docker.com/install/ and find the
    proper installation instructions for your machine.
--> Additionally, make sure you have installed docker-compose as you will be
    launching the web app with docker-compose from the command line. If you have
    not installed docker compose visit https://docs.docker.com/compose/install/
    and see how to install for your machine.
--> NOTE: While not an explicit Prerequisite, there is likely some information within
    the files you will want to change for security reasons before running the docker
    container. I will detail them below:
    --> Within the Twitter_APP folder, navigate to the readtweets folder and then
        go to the settings.py file.
    --> Once within this folder, find where it says 'ALLOWED_HOSTS'. Currently,
        it is listed as ALLOWED_HOSTS = ['*'], which signifies that anyone can be
        a host of the web app. While fine for development purposes within your local machine,
        you will likely want to change this if hosting from a private server.
    --> Next: You will want to specify what IP address you want to use for the database and
        host the web app at. Currently, for local development use it is specified at
        0.0.0.0:8000, which may not be agreeable for hosting.
    --> navigate to docker-compose.yml file  within the Twitter_App directory. Under the
        Services section, there is a subsection called web. Within here go to the
        line with the variable 'command'
    --> You will see the line 'python manage.py runserver 0.0.0.0:8000'
    --> Change the IP and port to whatever you choose for your application
    --> NOTE: If you change the port here, you will have to change it in the ports
        variable underneath the command line in the docker-compose.yml file.
--> Once you finish this your application should be good to run the docker image and create a container
    that runs the web app.


Instructions:
--> From your command line navigate to the Twitter_App folder.
--> From the command line, run:
    ```
    sudo docker-compose run web django-admin startproject factomtweets .
    ```
--> this will start the docker image in a container using the web service image and configuration
--> Verify that all necessary files are there by running
    ```
    ls -l
    ```
    if you see your files listed with you as the admin you should be fine. make sure you are listed
    as the admin for everything. If not go to https://docs.docker.com/compose/django/ for assistance
    on how to overcome this issue.
--> Everything should be good to run at this point. Make sure you are within the Twitter_App directory
    in your command line. From here all you should need to run is
    ```
    docker-compose up
    ```
    If successful, everything should run fine and your terminal should display the
    localhost address that you plug into your browser to go to and see the POC.
--> Can always check from command line that containers are running in a separate window by
    navigating to the Twitter_App folder and running:
    ```
    docker container ls
    ```
    If everything is operating as it should, there should be two containers displayed on the terminal
    one for the postgress and one for the django web app 
