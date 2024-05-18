# User Data App

This is a Django application that manages user data, specifically `Parent` and `Child` entities.

## Requirements

- Python 3.12.0
- Django 5.0.6
- Django REST Framework 3.15.1

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sakibshadman19/django-crud-app.git
   cd django-crud-app
2. Install the dependencies: 
   ```bash
   pip install -r requirements.txt
3. Run the migrations:
   ```bash
   python manage.py migrate
4. Start the development server: 
   ```bash
   python manage.py runserver
## API Endpoints

### Parents Endpoints
- **GET** `/api/parents/`: List all parents
- **POST** `/api/parents/`: Create a new parent
- **GET** `/api/parents/{id}/`: Retrieve a parent by ID
- **PUT** `/api/parents/{id}/`: Update a parent by ID
- **DELETE** `/api/parents/{id}/`: Delete a parent by ID

### Children Endpoints
- **GET** `/api/children/`: List all children
- **POST** `/api/children/`: Create a new child
- **GET** `/api/children/{id}/`: Retrieve a child by ID
- **PUT** `/api/children/{id}/`: Update a child by ID
- **DELETE** `/api/children/{id}/`: Delete a child by ID 


### Conclusion

You now have a complete Django application that stores user data for `Parent` and `Child` entities, along with a set of APIs to create, update, and delete this data. The application is tested to ensure it works properly. Follow the instructions in the `README.md` file to set up and run the application.
