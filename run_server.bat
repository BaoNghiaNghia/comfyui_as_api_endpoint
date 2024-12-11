@REM @echo off
@REM REM Stop and remove the container if it exists
@REM docker ps -a --filter "name=ytbthumbnailssc" --format "{{.Names}}" | findstr /I "ytbthumbnailssc" >nul

@REM IF %ERRORLEVEL% EQU 0 (
@REM     REM Container exists, stopping and removing the container
@REM     echo Container 'ytbthumbnailssc' exists. Stopping and removing the container...
@REM     docker stop ytbthumbnailssc
@REM     docker rm ytbthumbnailssc
@REM ) ELSE (
@REM     REM Container does not exist
@REM     echo Container 'ytbthumbnailssc' does not exist.
@REM )

@REM REM Remove all previous Docker images
@REM echo Removing all previous Docker images...
@REM for /f "tokens=*" %%i in ('docker images -q') do docker rmi -f %%i

@REM REM Rebuild the Docker image
@REM echo Rebuilding Docker image 'ytbthumbnailssc'...
@REM docker build -t ytbthumbnailssc .

@REM REM Restart the container with the new image
@REM echo Starting the container with the new image...
@REM docker run -d -p 8000:8000 --env-file .env --name ytbthumbnailssc ytbthumbnailssc

@REM exit

uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000