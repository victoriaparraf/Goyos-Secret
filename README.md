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
