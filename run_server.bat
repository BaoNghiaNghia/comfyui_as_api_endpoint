@echo off
REM Check if the container 'ytbthumbnailssc' is already running or exists
docker ps -a --filter "name=ytbthumbnailssc" --format "{{.Names}}" | findstr /I "ytbthumbnailssc" >nul

IF %ERRORLEVEL% EQU 0 (
    REM Container exists, stopping and removing it
    echo Container 'ytbthumbnailssc' exists. Stopping and removing the container...
    docker stop ytbthumbnailssc
    docker rm ytbthumbnailssc
) ELSE (
    REM Container does not exist
    echo Container 'ytbthumbnailssc' does not exist.
)

REM Rebuild the Docker image
echo Rebuilding Docker image 'ytbthumbnailssc'...
docker build -t ytbthumbnailssc .

REM Restart the container with the new image
echo Starting the container with the new image...
docker run -d -p 8000:8000 --env-file .env --name ytbthumbnailssc ytbthumbnailssc

REM Optional: Display status or message
echo Docker container 'ytbthumbnailssc' is running on port 8000.

