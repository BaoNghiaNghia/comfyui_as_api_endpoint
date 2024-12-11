@echo off
cd %~dp0

echo ARE YOU ABSOLUTELY SURE YOU WANT TO RUN THIS? RUNNING THIS MORE THAN ONCE WILL REMOVE PREVIOUS COMFYUI DOCKER CONTAINERS. 
choice /C YN /N /M "Press Y for Yes or N for No: "
if errorlevel 2 goto End
if errorlevel 1 goto ContinueWithPath

:ContinueWithPath

:: Retrieve hostname and store in hostname variable
for /f "tokens=*" %%i in ('hostname') do set hostname=%%i

:: try stopping/removing containers in case they've already been started and failed.
echo Attempting to stop and remove previous containers, if they exist, otherwise ignore
docker stop comfyui_initial_container 2>nul || echo .
docker container rm comfyui_initial_container 2>nul || echo .
docker stop comfyui_installed_container 2>nul || echo .
docker container rm comfyui_installed_container 2>nul || echo .
docker image rm comfyui_installed 2>nul || echo .
docker image rm comfyui_initial 2>nul || echo .

:: Build Docker image from the docker file into just an initial bash shell state
docker build -f .\ComfyUI.Dockerfile -t comfyui_initial .

:: Remove and recreate Docker volume for the mounted folder
docker volume rm ComfyUIDocker 2>nul || echo .
docker volume create --driver local --opt type=none --opt device="C:/ComfyUIDocker/Mounted" --opt o=bind ComfyUIDocker

:: Pause so if there are any errors they can be read
echo Pausing so that if there were any errors they can be read
pause
echo Continuing, please wait...

:: Construct the Docker command, mount the folder this is in so it will be accessible.
set dockerCommand=docker run -it --gpus all -p 127.0.0.1:8189:8189 ^
  --hostname %hostname%-ComfyUI ^
  --mount source=ComfyUIDocker,target=/ComfyUIDocker ^
  --name comfyui_initial_container comfyui_initial

:: Execute the Docker command
%dockerCommand%

:: Pause so if there are any errors they can be read
echo Pausing so that if there were any errors they can be read
pause
echo Continuing, please wait...

:: Committing the container after installation so those steps can be skipped in the future
echo Committing initial container to installed image
docker commit comfyui_initial_container comfyui_installed

:: Construct the Docker command for the installed version, so we will have a container we can use going forward
set dockerCommand=docker run -d --gpus all -p 127.0.0.1:8189:8189 ^
  --hostname %hostname%-ComfyUI ^
  --mount source=ComfyUIDocker,target=/ComfyUIDocker ^
  --name comfyui_installed_container comfyui_installed tail -f /dev/null

:: Execute the Docker command
%dockerCommand%

:: sleep for 5 seconds to give the detached container time to start
timeout /t 5 /nobreak >nul

:: Stop the detached container 
docker stop comfyui_installed_container

echo Pausing so if there were any errors they can be read
echo Finished, please run Run.bat now to continue
pause

:End
echo Goodbye
