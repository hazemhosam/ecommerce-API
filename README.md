# E-commerce application API

## Features
User Authentication: Secure user registration, login, authentication using JWT (JSON Web Tokens), and create a profile associated with every new user using Signals.

Product Management: CRUD operations for products, including categories, inventory, and pricing with reviews for feedback.

Shopping Cart: Users can add, update, and remove items from their shopping cart.

Order Processing: Users can place orders, view order history, track order status and process payment.

Search and Filtering: Advanced search and filtering options for products.

Pagination: Efficient handling of large datasets with pagination.

API Documentation: Comprehensive API documentation using Swagger/OpenAPI at ```/api/swagger/```.

## Technologies Used
Backend: Django, Django REST Framework (DRF)

Authentication: JWT (JSON Web Tokens) 

Database: MySQL

API Documentation: Swagger/OpenAPI

Payment Method: Stripe

## Installation
### Follow these steps to set up the project locally:
 1-Clone the repository:
 ```bash
 git clone https://github.com//hazemhosam/ecommerce-API.git
 cd ecommerce-API
```
2-Create a virtual environment (optional but recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On mac: source venv/bin/activate 
```
3-Install dependencies:

```bash
pip install -r requirements.txt
```
4-Set up the database:

  Update the DATABASES configuration in settings.py with your database credentials.

  Run migrations:
```bash
python manage.py migrate
```

## Contributing 
Contributions are welcome! If you'd like to contribute 

## License
This project is licensed under the MIT License.

## Contact
If you have any questions or feedback, feel free to reach out:

GitHub: [github](https://github.com/hazemhosam/) 

LinkedIn: [linkedin](https://www.linkedin.com/in/hazem-hosam-4242391b9/)

Email: [email](hazemhosam105@gmail.com)


