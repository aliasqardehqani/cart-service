
```markdown
# 🛒 Cart Service (Django Backend)

A backend microservice built with Django REST Framework to manage an e-commerce cart and order system for auto parts. This service supports part listing, adding/removing items to a cart, placing orders, and managing delivery and payment statuses.

---

## 🚀 Features

- List available car parts with inventory and category
- Add/remove/update parts in a user’s cart
- Create and manage orders
- Handle delivery type and track order status
- Webhook support for payment confirmation
- Persian language support in responses/messages

---

## 🧰 Tech Stack

- **Backend:** Django 4+ & Django REST Framework  
- **Database:** Default Django ORM (PostgreSQL / SQLite / etc.)  
- **Authentication:** Django `AbstractUser` model (customized)  
- **Serialization:** DRF `ModelSerializer`  
- **Pagination:** DRF pagination (page size configurable)  
- **Languages:** Python 3.10+

---

## 🧱 Project Structure

```

cart-service/
├── cart\_service/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── cart\_service.py
│   └── ...
├── manage.py
├── requirements.txt
└── README.md

````

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/aliasqardehqani/cart-service.git
cd cart-service

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (for admin access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
````

---

## 🔐 Authentication

* The service uses Django's custom `User` model named `Person`
* Login is required for cart and order operations
* Auth method: Session or Token (you can add JWT if needed)

---

## 📤 API Endpoints

| Method | Endpoint                | Description                          |
| ------ | ----------------------- | ------------------------------------ |
| GET    | `/parts/`               | List available parts                 |
| POST   | `/add/`                 | Add item to cart                     |
| GET    | `/list-cart/`           | View current user’s cart             |
| DELETE | `/delete/<item_id>/`    | Remove item from cart                |
| DELETE | `/clear/`               | Clear user’s cart                    |
| POST   | `/orders/create/`       | Create a new order from the cart     |
| POST   | `/orders/payment/`      | Simulate payment gateway interaction |
| POST   | `/orders/final-status/` | Webhook callback for payment status  |

---

## 📄 Models Overview

### `PartUnified`

Represents a single car part, merged with category and image info.

### `Cart` & `CartItem`

User’s active shopping cart and its contents.

### `Order`

Created from a cart. Includes delivery type, status, and total price.

### `Person`

Extends Django's `AbstractUser` with profile info like phone, address, etc.

---

## 📦 Example Request: Add to Cart

```json
POST /add/
{
  "part_id": 3,
  "quantity": 2
}
```

**Response:**

```json
{
  "message": "2 عدد از محصول به سبد خرید اضافه شد."
}
```

---

## 📥 Invoice Sample (Generated After Order)

```
فاکتور سفارش       
کد سفارش: X8KJ2Z9LMN
نام کاربر: ali_qardehqani
تاریخ ایجاد سفارش: 2025-07-29 16:21:00
نوع ارسال: تیپاکس
تاریخ تحویل: 2025-08-01
مجموع قیمت: 850,000 تومان

آیتم‌ها:
- لنت ترمز | تعداد: 2 | قیمت واحد: 350,000 | قیمت کل: 700,000
- فیلتر روغن | تعداد: 1 | قیمت واحد: 150,000 | قیمت کل: 150,000

با تشکر از خرید شما.
```


---

## 📌 TODOs

* [ ] Add JWT authentication
* [ ] Add admin UI for managing parts/orders
* [ ] Write unit and integration tests
* [ ] Swagger/OpenAPI auto docs
* [ ] Redis caching for popular parts

---

## 📄 License

MIT License © [aliasqardehqani](https://github.com/aliasqardehqani)

