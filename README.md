# Author's Website

Designed to deepen the connection between authors and their readers. This website offers a range of features, including book browsing, purchasing information, author background and blog posts. For those who sign up, an innovative chatbot awaits, providing an interactive experience with characters from the children's book "Sam Satito".

Authorized users (authors) can manage blog posts effortlessly, with capabilities to create, edit, and delete content directly from the platform. These users will also have an admin view where they'll be able to see the total amount of users that have signed up and the number of posts that have been created. 

Link to deplyed app: https://capstone-project-authors-interactive.onrender.com


## App Build Overview

#### How to Run the App:

- **Step 1:** Once repository has been cloned, go into your terminal, navigate to your repository and create a virtual enviroment. 
- **Step 2:** Activate virtual enviroment and use command `pip install -r requirements.txt` in the termanal to copy over the needed dependencies. 
- **Step 3:** Create your database and start server. To create a database enter `createdb authors_website_db` in the terminal.
- **Step 4:** Generate an API key for the OpenAI API (visit this [link](https://platform.openai.com/docs/quickstart?context=python) for details). This will allow the chat functionality.
- **Step 5:** Run server. This app uses Flask framework for the backend, therefore, to run the server type `flask run`.
- **Step 6:** Enjoy playing around with the app!

***Note: The API used in this app is a free version of OpenAi which contains strict rate limits: 40,000 TPM (tokens per minute), 3 RPM (request per minutes) and 200 RPD (request per day). For more information about rate limits visit https://platform.openai.com/docs/guides/rate-limits***


#### Technologies Used

- **Python/Flask:** The backend is developed using the Flask framework to handle routing, requests, and server-side logic.

- **PostgreSQL/SQLAlchemy:** The app uses a PostgreSQL database to store user data, blog posts, and other relevant information. SQLAlchemy is employed as an Object-Relational Mapping (ORM) tool to interact with the database.

- **OpenAI API:** The OpenAI API is integrated for the innovative chatbot functionality. Users can interact with characters from the children's book "Sam Satito" using AI-generated responses.

- **HTML, CSS, JavaScript:** Frontend development is achieved using these standard web technologies to create dynamic and visually appealing user interfaces.

#### App Structure

- **User Authentication:** The app supports user signup, login, and logout functionalities. User data is securely stored and managed.

- **Blog Post Management:** Authorized users (authors) can create, edit, and delete blog posts. Admin views offer insights into the total number of signed-up users and created blog posts.
  
- **Admin Dashboard:** An admin dashboard provides key metrics, including the total number of users, total blog posts, and new users signed up in the last week.
  
- **Chatbot Integration:** The innovative chatbot powered by OpenAI allows users to interact with characters from "Sam Satito." The conversation history is stored in the session for a seamless experience.

- **Book Landing Pages:** Each book has a dedicated landing page where users can explore detailed information about the book.

- **Admin Dashboard:** An admin dashboard provides key metrics, including the total number of users, total blog posts, and new users signed up in the last week.


