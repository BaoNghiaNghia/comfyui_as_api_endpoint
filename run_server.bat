@echo off
REM Stop and remove the container if it exists
docker ps -a --filter "name=ytbthumbnailssc" --format "{{.Names}}" | findstr /I "ytbthumbnailssc" >nul

IF %ERRORLEVEL% EQU 0 (
    REM Container exists, stopping and removing the container
    echo Container 'ytbthumbnailssc' exists. Stopping and removing the container...
    docker stop ytbthumbnailssc
    docker rm ytbthumbnailssc
) ELSE (
    REM Container does not exist
    echo Container 'ytbthumbnailssc' does not exist.
)

REM Remove all previous Docker images
echo Removing all previous Docker images...
for /f "tokens=*" %%i in ('docker images -q') do docker rmi -f %%i

REM Rebuild the Docker image
echo Rebuilding Docker image 'ytbthumbnailssc'...
docker build -t ytbthumbnailssc .

REM Restart the container with the new image
echo Starting the container with the new image...
docker run -d -p 8000:8000 --env-file .env --name ytbthumbnailssc ytbthumbnailssc

exit