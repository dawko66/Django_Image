## Django Image Application

The Django Image Application is a tool that allows you to add, browse, and
manage images. Below, you will find instructions on how to run this
application and the available links to different functionalities.

**Running the Application**

You can run the application using Docker Compose. To do so, follow these
steps:

1.  Open a terminal.

2.  Navigate to the directory where the **docker-compose.yml** file,
    containing the application configuration, is located.

3. Create the `entrypoint.sh` file and change its contents in Visual Studio Code to:
```
#!/bin/sh

echo "Apply database migrations"
python manage.py migrate
exec "$@"

```

4. Start the application by entering the following command:

> docker-compose up -d --build

This command will launch the application in Docker containers on your local server.

5. After a successful launch, the application will be accessible at
    **http://localhost:8001**.

**Available Links**

Once the application is up and running, you can use the following links:

-   **Login:** To log in to the application, use the link below:

    -   [http://localhost:8001/api-auth/login/?next=/imageapp/api/](http://localhost:8001/api-auth/login/?next=/imageapp/api/)

    -   Login credentials:

        -   **Superuser:** Username: dawid, Password: 1234

        -   **Basic:** Username: BasicUser, Password: zaq1@WSX

        -   **Premium:** Username: PremiumUser, Password: zaq1@WSX

        -   **Enterprise:** Username: EnterpriseUser, Password: zaq1@WSX

-   **Add Images:** To upload new images, use the link below:

    -   [http://localhost:8001/imageapp/api/images-upload/](http://localhost:8001/imageapp/api/images-upload/)

-   **List Images:** To browse a list of available images, use the link
    below:

    -   [http://localhost:8001/imageapp/api/images-list/](http://localhost:8001/imageapp/api/images-list/)

The above links will lead you to different functionalities of the application, allowing you to make the most of its features.

Now, after launching the application and logging in, you can easily manage images within the Markdown Application.
