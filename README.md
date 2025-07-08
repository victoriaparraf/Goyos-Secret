# Goyo´s Secrets Restaurants API

API para gestionar restaurantes, reservaciones, usuarios y menús.

## Features

This API provides the following functionalities:

*   **Authentication & Authorization**: Secure user management with different roles.
*   **Restaurant Management**: Create, read, update, and delete restaurant information.
*   **Table Management**: Manage tables within restaurants.
*   **Menu Management**: Handle menu items and pre-orders.
*   **Reservation Management**: Create, cancel, and view reservations.
*   **Dashboard & Analytics**: Get insights into reservations, top pre-ordered dishes, and restaurant occupancy.

## Setup

### Using Docker (Recommended)

1.  **Build and run the Docker containers:**

    ```bash
    docker-compose up --build
    ```

    This will build the Docker images and start the API server and its dependencies (e.g., database).

### Local Development

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd Goyos-Secret
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    Copy `.env.template` to `.env` and fill in the necessary details (e.g., database connection string).

    ```bash
    cp .env.template .env
    ```

5.  **Run database migrations (if applicable):**

    ```bash
    alembic upgrade head
    ```

## Running the Application

Once set up, you can run the application:

```bash
# Using Uvicorn (local development)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be accessible at `http://localhost:8000`.

## API Endpoints

The API provides the following main endpoint categories:

*   `/auth`: User authentication and authorization.
*   `/menu`: Operations related to menu items.
*   `/restaurants`: Management of restaurant information.
*   `/tables`: Management of tables within restaurants.
*   `/reservations`: Handling of reservations.
*   `/dashboard`: Analytics and dashboard data (admin access required).

Detailed API documentation (Swagger UI) will be available at `http://localhost:8000/docs` once the application is running.

## Testing

To run the tests, activate your virtual environment and execute:

```bash
pytest
```

## Project Structure

```
├─── .env.template
├─── .gitignore
├─── alembic.ini
├─── docker-compose.yml
├─── Dockerfile
├─── main.py
├─── pytest.ini
├─── README.md
├─── requirements.txt
├─── alembic/
│    ├─── env.py
│    ├─── README
│    ├─── script.py.mako
│    └─── versions/
│         ├─── 22b7e3793d08_initial_migration.py
│         ├─── 4ed53021ab7d_delete_duplicate_user.py
│         └─── ebe79cf4523d_pruebita.py
└─── modules/
     ├─── auth/
     │    ├─── application/
     │    │    ├─── auth_services.py
     │    │    ├─── user_services.py
     │    │    └─── dtos/
     │    │         ├─── user_login_dto.py
     │    │         ├─── user_modify_dto.py
     │    │         └─── user_register_dto.py
     │    ├─── domain/
     │    │    ├─── user_repository_interface.py
     │    │    └─── user.py
     │    ├─── infrastructure/
     │    │    ├─── auth_controller.py
     │    │    ├─── user_db_model.py
     │    │    └─── user_repository.py
     │    └─── tests/
     │         └─── infrastructure/
     │              └─── test_auth_controller.py
     ├─── core/
     │    └─── db_connection.py
     ├─── dashboard/
     │    ├─── application/
     │    │    └─── dashboard_services.py
     │    └─── infrastructure/
     │         └─── dashboard_controller.py
     ├─── menu/
     │    ├─── application/
     │    │    ├─── menu_services.py
     │    │    └─── dtos/
     │    │         └─── menu_item_dto.py
     │    ├─── domain/
     │    │    ├─── menu_item.py
     │    │    ├─── menu_repository_interface.py
     │    │    └─── pre_order_item.py
     │    ├─── infrastructure/
     │    │    ├─── menu_controller.py
     │    │    ├─── menu_item_db_model.py
     │    │    ├─── menu_repository.py
     │    │    └─── pre_order_item_db_model.py
     │    └─── tests/
     │         ├─── application/
     │         │    └─── test_menu_services.py
     │         └─── infrastructure/
     │              └─── test_menu_controller.py
     ├─── notifications/
     │    └─── notifications.py
     ├─── reservation/
     │    ├─── application/
     │    │    ├─── reservation_services.py
     │    │    └─── dtos/
     │    │         ├─── reservation_create_dto.py
     │    │         └─── reservation_response_dto.py
     │    ├─── domain/
     │    │    ├─── reservation_repository_interface.py
     │    │    └─── reservation.py
     │    ├─── infrastructure/
     │    │    ├─── reservation_controller.py
     │    │    ├─── reservation_db_model.py
     │    │    └─── reservation_repository.py
     │    └─── tests/
     │         └─── application/
     │              └─── test_reservation_services.py
     └─── restaurant/
          ├─── application/
          │    ├─── restaurant_services.py
          │    ├─── table_services.py
          │    └─── dtos/
          │         ├─── restaurant_create_dto.py
          │         ├─── restaurant_response_dto.py
          │         ├─── restaurant_update_dto.py
          │         ├─── table_create_dto.py
          │         ├─── table_response_dto.py
          │         └─── table_update_dto.py
          ├─── domain/
          │    ├─── restaurant_repository_interface.py
          │    ├─── restaurant.py
          │    ├─── table_repository_interface.py
          │    └─── table.py
          ├─── infrastructure/
          │    ├─── restaurant_controller.py
          │    ├─── restaurant_db_model.py
          │    ├─── restaurant_repository.py
          │    ├─── table_controller.py
          │    ├─── table_db_model.py
          │    └─── table_repository.py
          └─── tests/
               ├─── application/
               │    ├─── test_restaurant_service.py
               │    └─── test_table_services.py
               ├─── domain/
               │    └─── test_restaurant.py
               └─── infrastructure/
                    └─── test_restaurant_controller.py