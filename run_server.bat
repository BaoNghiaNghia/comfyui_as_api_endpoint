docker build -t ytbthumbnailssc .
docker run -d -p 8000:8000 --env-file .env --name ytbthumbnailssc ytbthumbnailssc