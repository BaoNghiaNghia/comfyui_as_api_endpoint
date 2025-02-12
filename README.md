# **YtbThumbnail - AI-Powered Creativity**

YtbThumbnail is an AI-powered image generator that allows users to create high-quality, creative images using ComfyUI and integrates with a local Large Language Model (LLM) via Ollama. This project includes a FastAPI backend, a dynamic web interface, and support for user-configurable models and servers.

---

## **Table of Contents**

- [**YtbThumbnail - AI-Powered Creativity**](#ytbthumbnail---ai-powered-creativity)
  - [**Table of Contents**](#table-of-contents)
  - [**Setup**](#setup)
    - [**Requirements**](#requirements)
    - [**Installation**](#installation)
  - [**Running the Server**](#running-the-server)
    - [**Local Environment**](#local-environment)
  - [**Running with Docker**](#running-with-docker)
    - [**1. Build the Docker Image**](#1-build-the-docker-image)
    - [**2. Run the Docker Container**](#2-run-the-docker-container)
    - [**3. Access the Application**](#3-access-the-application)
  - [**Functionality**](#functionality)
    - [**Positive and Negative Prompts**](#positive-and-negative-prompts)
    - [**LLM-Assisted Prompt Generation**](#llm-assisted-prompt-generation)
    - [**Quick Prompts**](#quick-prompts)
    - [**Image Caching and Navigation**](#image-caching-and-navigation)
    - [**UI Reset**](#ui-reset)
  - [**Architecture**](#architecture)
    - [**Backend**](#backend)
      - [**Key Endpoints**](#key-endpoints)
    - [**Frontend**](#frontend)
      - [**UI Components**](#ui-components)
    - [**Tools and Libraries**](#tools-and-libraries)
  - [**Testing**](#testing)
  - [**Kill Server**](#kill-server)
  - [API Request: Generate YouTube Thumbnail](#api-request-generate-youtube-thumbnail)
    - [Câu lệnh `curl`](#câu-lệnh-curl)
    - [Các tham số](#các-tham-số)
    - [Ví dụ kết quả trả về](#ví-dụ-kết-quả-trả-về)

---

## **Setup**

### **Requirements**

1. **Conda Environment**:

   - The project uses Conda for environment management. Make sure Conda is installed on your system.

2. **ComfyUI**:

   - ComfyUI should be installed and running. You must have the checkpoint `realvisxlV50Lightning.Ng9I.safetensors` installed in the `checkpoints` folder for the workflow.
   - Alternatively, you can modify `workflow.json` to use any other model/checkpoint.

3. **Ollama**:

   - Ollama LLM server should be installed and accessible.

### **Installation**

1. **Clone the Repository**:

   ```bash
    git clone https://github.com/Teachings/YtbThumbnail.git
    cd YtbThumbnail
   ```

2. **Set Up Conda Environment**:

   Create and activate the Conda environment:

    ```bash
      conda create --name ytbthumbnailssc python=3.12
      conda activate ytbthumbnailssc
    ```

3. **Install Dependencies**:

   Install the project dependencies listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up `.env` File**:

   Ensure the `.env` file exists in the project root and contains the correct server addresses for ComfyUI and Ollama.

    ```bash
      COMFYUI_SERVER_ADDRESS=192.168.1.10:8188
    ```

---

## **Running the Server**

### **Local Environment**

To run the FastAPI server in your local environment, use the following command:

```bash
  uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

This will start the app on `http://localhost:8000/`.

To ensure that ComfyUI is functioning correctly, you can test the connection using the workflow defined in `workflow.json`.

---

## **Running with Docker**

If you prefer to run the application inside a Docker container, the following steps guide you through building and running the containerized application.

### **1. Build the Docker Image**

Navigate to the project directory and build the Docker image:

```bash
  docker build -t ytbthumbnailssc .
```

### **2. Run the Docker Container**

Once the Docker image is built, run the container:

```bash
  docker run -d -p 8000:8000 --env-file .env --name ytbthumbnailssc ytbthumbnailssc
```

This command will:

- Start the container in **detached mode** (`-d`).
- Map port **8000** of the container to port **8000** on your host.
- Use the `.env` file to set environment variables.

### **3. Access the Application**

You can now access the application at `http://localhost:8000/`

---

## **Functionality**

### **Positive and Negative Prompts**

- **Positive Prompt**: Specifies the elements to include in the generated image (e.g., "4k, highly detailed, hyperrealistic").
- **Negative Prompt**: Specifies elements to avoid in the image (e.g., "blurry, watermark").

### **LLM-Assisted Prompt Generation**

- **Ask LLM for a Creative Idea**: The user can request a creative prompt suggestion from a locally hosted LLM (Ollama). The generated prompt can be applied to the positive prompt field.

### **Quick Prompts**

- **Preconfigured Prompts**: Both positive and negative quick prompts are available via buttons. Clicking a button auto-fills the corresponding input field.
- **Custom Prompts**: Themed prompts (like **Halloween** or **Christmas**) are dynamically loaded from the `quick_prompts.json` file. Adding new themes is as easy as editing this file.

### **Image Caching and Navigation**

- **Image History**: The app caches generated images within the session. Users can navigate through cached images using the **Previous** and **Next** buttons.
- **Cache Clearing**: Cached images are cleared when the browser is refreshed or when the **Reset** button is clicked.

### **UI Reset**

- The **Reset** button clears all input fields, resets generated images, and clears the image cache.

---

## **Architecture**

### **Backend**

The backend is powered by **FastAPI** and handles the following operations:

- Generating images using ComfyUI.
- Fetching creative suggestions from the local LLM.
- Serving quick prompts from configuration files.

#### **Key Endpoints**

1. **POST /generate_images/**

   - **Description**: Generates an AI image using the provided prompts and image settings.
   - **Request Example**:

    ```json
      {
        "positive_prompt": "a beautiful sunset",
        "negative_prompt": "blurry",
        "steps": 25,
        "width": 512,
        "height": 512
      }
    ```

   - **Response**: A binary stream containing the generated image.

2. **POST /ask_llm/**

   - **Description**: Requests a creative prompt from the local LLM server (Ollama).
   - **Request Example**:

     ```json
     {
       "positive_prompt": "a beautiful sunset"
     }
     ```

   - **Response**:

     ```json
     {
       "assistant_reply": "How about a stunning sunset over the mountains with golden light reflecting on the water?"
     }
     ```

3. **GET /quick_prompts/**
   - **Description**: Retrieves quick prompt configurations from the `quick_prompts.json` file for dynamic UI updates.
   - **Response Example**:

     ```json
     {
       "Positive Quick Prompts": [
         { "label": "4K", "value": "4K" },
         { "label": "Highly Detailed", "value": "highly detailed" }
       ],
       "Negative Quick Prompts": [
         { "label": "Blurry", "value": "blurry" },
         { "label": "Watermark", "value": "watermark" }
       ],
       "Halloween": [
         { "label": "Black Background", "value": "black background" },
         { "label": "Witch", "value": "witch" }
       ]
     }
     ```

### **Frontend**

The frontend is built with HTML, CSS, and JavaScript. It dynamically interacts with the backend for:

- Generating images.
- Fetching creative prompts from the LLM.
- Loading quick prompt configurations from `quick_prompts.json`.

#### **UI Components**

1. **Image Generation Form**:

   - Includes fields for positive and negative prompts, image steps, width, and height.
   - Quick prompt buttons for easy input.

2. **LLM Integration**:

   - A section that allows users to request and apply creative prompts generated by the LLM.

3. **Image Display and Navigation**:

   - Displays the generated images and includes buttons for navigating through cached images.

4. **Reset Functionality**:
   - A **Reset** button to clear all input fields and generated image history.

### **Tools and Libraries**

1. **FastAPI**: Web framework for building the backend.
2. **Uvicorn**: ASGI server used to run the FastAPI application.
3. **Ollama**: Locally hosted LLM for generating creative prompts.
4. **Pillow**: Python Imaging Library used to handle image operations.
5. **Bootstrap**: CSS framework for styling the UI.
6. **JavaScript (Fetch API)**: Handles asynchronous requests to the backend.

---

## **Testing**

You can test the ComfyUI workflow by running the FastAPI server as described above. Use the `/generate_images/` endpoint to generate images and validate that the workflow is functioning correctly.

To test the LLM integration, use the `/ask_llm/` endpoint to request a creative prompt from the locally hosted Ollama LLM.

For Docker-based setups, ensure that the `.env` file is correctly set up with the server addresses and run the container as described in the [Running with Docker](#running-with-docker) section.

## **Kill Server**

If you need to force kill the server process, you can use the following command:

```bash
sudo kill -9 $(sudo lsof -t -i :8000)
```

## API Request: Generate YouTube Thumbnail

Để tạo thumbnail YouTube, bạn có thể sử dụng API sau:

### Câu lệnh `curl`

```bash
curl --location 'http://sscrender.ddns.net:8000/generate_images/thumbnail-youtube' \
--header 'Content-Type: application/json' \
--data '{
    "positive_prompt": "Merry Christmas",
    "thumb_style": "realistic photo",
    "thumbnail_number": 1,
    "domain": "http://claim-api.simplesolution.co/api/v2",
    "token": "1087|KpWpSfAu15jBSqHJKrpIglrX9CzVp8iViIhohqfH"
}'
```

### Các tham số

- **positive_prompt**: Mô tả tiêu đề và chủ đề của thumbnail (ví dụ: "Merry Christmas").
- **thumb_style**: Mô tả phong cách ảnh thumbnail. Các kiểu phong cách có thể bao gồm:
      - realistic photo (ảnh chụp)
      - illustration (minh họa)
      - 3d (3D)
      - cartoon fun (hoạt hình vui nhộn)
      - comic (truyện tranh)
      - dark (tối)
      - water color (sơn nước)
      - pixel art (nghệ thuật pixel)
      - surreal (siêu thực)
      - oil painting (sơn dầu)
      - nature (thiên nhiên)
      - ink print (in mực)
      - pencil (bút chì)
      - retrowave (retro sóng)
      - vintage japanese (nhật bản cổ điển)
      - lifestyle (lối sống)
      - collage (ghép ảnh)
      - glitchart (nghệ thuật lỗi)
      - retroglow (ánh sáng cổ điển)
      - lowkey cinematic (điện ảnh nhẹ nhàng)
      - analog memories (kỷ niệm analog)
      - trippy illustration (minh họa kỳ ảo)
      - fantasy cartoon (hoạt hình giả tưởng)
      - pastel paint (sơn pastel)
      - arcadebits (bit arcade)
      - squishy 3d (3D nở ra)
      - product photography (chụp ảnh sản phẩm)
      - historical (lịch sử)
      - felted (dệt)
      - podium (bục)
      - redveil (màn đỏ)
      - darklight dreamscaped (ánh sáng tối, cảnh mơ)
      - dreamlandscapes (cảnh mơ)
      - linework (làm việc với đường nét)
      - sonny anime (anime Sonny)
      - soft pasty (mềm mại, nhạt màu)
      - soft retro (retro nhẹ nhàng)
      - plushy world (thế giới nhồi bông)
      - film effect (hiệu ứng phim)
      - anime (anime)
      - warnand cold (ấm và lạnh)
      - sparking (tỏa sáng)
      - blurry long exposure (phơi sáng mờ)
      - flutted glass (kính gợn sóng)
      - glimmerish (lấp lánh)
      - 40s influence (ảnh hưởng thập niên 40)
      - dadapop (dadapop)
      - 80smovie (phim thập niên 80)
      - renaissance fashion (thời trang phục hưng)
      - fineart (nghệ thuật tinh tế)
      - neo classicart (nghệ thuật cổ điển mới)
      - highend light (ánh sáng cao cấp)
      - fantasy anime (anime giả tưởng)
      - 3d colorful (3D đầy màu sắc)
      - illustrator photo (ảnh họa sĩ minh họa)
- **thumbnail_number**: Số lượng thumbnail tối đa có thể tạo trong một lần. (Tối đa 5 thumbnail hiện tại).
- **domain** và **token**: Dùng cho xác thực (hiện tại chưa sử dụng).

### Ví dụ kết quả trả về

```json
{
    "images": [
        {
            "filename": "ytb_thumbnail_img_00019_.png",
            "subfolder": "",
            "type": "output",
            "file_path": "http://sscrender.ddns.net:8000/download-images?file_name=ytb_thumbnail_img_00019_.png"
        }
    ],
    "seed": 786172516883911
}
```

Với `file_path` là đường dẫn để download thumbnail


```json
python.exe -m pip install torch==2.5.1+cu121 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

pip install xformers==0.0.29.post3
```