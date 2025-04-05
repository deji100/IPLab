# IPLab

# Django Video Downloader

This project allows you to download videos from a specified YouTube channel using the YouTube Data API and the `yt-dlp` library.

## Requirements

- Docker
- Docker Compose
- Python 3.11 (for local development without Docker)
- PostgreSQL (managed by Docker Compose)

## Project Setup

Follow these steps to clone, set up, and run the project on your local machine.

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a `.env` File

Create a `.env` file in the root directory of the project and add the following environment variables:

```env
# YouTube API Key and Channel ID
YOUTUBE_API_KEY=your_youtube_api_key_here
YOUTUBE_CHANNEL_ID=your_channel_id_here

# Database configuration for development
DB_HOST=db
DB_NAME=your_db_name_here
DB_USER=your_db_user_here
DB_PASSWORD=your_db_password_here
```

Make sure to replace `your_youtube_api_key_here`, `your_channel_id_here`, and the database configuration with the correct values.

### 3. Build and Run with Docker

Ensure that Docker and Docker Compose are installed on your machine.

Run the following command to build and start the containers:

```bash
docker-compose up --build
```

This will build the Docker images for your Django application and PostgreSQL, and then start the containers.

### 4. Apply Migrations

Once the containers are up and running, apply the database migrations:

```bash
docker-compose exec web python manage.py migrate
```

This will create the necessary tables in your PostgreSQL database.

### 5. Access the Application

Once the server is running, you can access the application in your browser at `http://localhost:8000`.

### 6. Download Videos

To start downloading videos from the specified YouTube channel, hit the following endpoint via your browser or a tool like Postman:

```
http://localhost:8000/api/fetch-videos
```

This will trigger the video download process, and the videos will be saved in the `media/videos/` directory inside your project.

## Project Structure

The main components of the project are as follows:

- **Django**: The web framework handling API requests, including the video fetching and downloading process.
- **yt-dlp**: The library used to download videos from YouTube.
- **PostgreSQL**: The database used to store video and channel information.
- **Docker**: The containers that package the app and its dependencies.

## Running the Project Without Docker (Optional)

If you prefer to run the project without Docker, follow these steps:

1. Install Python 3.11 and the required dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the root directory with the same contents as above.

3. Apply the migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the Django development server:

   ```bash
   python manage.py runserver
   ```

5. Access the app at `http://localhost:8000` and hit the endpoint to start downloading videos.

## Additional Notes

- The app fetches and downloads videos from a specific YouTube channel using the YouTube API and `yt-dlp` library.
- The `.env` file contains the correct API keys, channel ID, and database configurations.
- Video downloads are triggered by hitting the endpoint `http://localhost:8000/api/fetch-videos`.

---

This `README.md` provides clear instructions on how to clone, set up, and run the Django project using Docker, with details on how to hit the API endpoint to download videos.