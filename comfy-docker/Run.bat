:: Stop container if running already
docker stop comfyui_installed_container

:: Start container
docker start comfyui_installed_container

:: Start ComfyUI in container
docker exec -it comfyui_installed_container /ComfyUIDocker/Scripts/StartComfyUI.sh

:: Pause so errors can be read.
pause