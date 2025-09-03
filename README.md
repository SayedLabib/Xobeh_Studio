# 🎨 XobehStudio - AI Image Generation Service

A powerful FastAPI-based service for generating high-quality images using Stable Diffusion v1.5 from Hugging Face.

## 🌟 Features

- **Stable Diffusion v1.5**: High-quality image generation using the popular runwayml/stable-diffusion-v1-5 model
- **RESTful API**: Clean, well-documented API endpoints
- **Automatic Model Download**: Downloads the model from Hugging Face Hub on first use
- **GPU/CPU Support**: Automatically detects and uses the best available device (CUDA, MPS, or CPU)
- **Memory Optimization**: Includes memory management and cleanup utilities
- **Interactive Documentation**: Swagger UI and ReDoc documentation
- **Base64 Output**: Returns generated images as base64 encoded strings

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) NVIDIA GPU with CUDA support for faster generation

### Installation

1. **Clone or download the project**
   ```bash
   cd XobehStudio
   ```

2. **Install dependencies**
   
   **Windows:**
   ```cmd
   setup.bat
   ```
   
   **Linux/macOS:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   
   **Manual installation:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the service**
   ```bash
   cd app
   python main.py
   ```

4. **Access the service**
   - Main interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 📋 API Endpoints

### Generate Image
**POST** `/api/v1/stable-diffusion/generate`

Generate an image from a text prompt.

**Request Body:**
```json
{
  "prompt": "A beautiful landscape with mountains and a lake at sunset",
  "negative_prompt": "blurry, low quality, distorted, deformed",
  "width": 512,
  "height": 512,
  "num_inference_steps": 50,
  "guidance_scale": 7.5,
  "seed": null
}
```

**Response:**
```json
{
  "success": true,
  "message": "Image generated successfully",
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "generation_time": 12.34,
  "model_info": {
    "model_id": "runwayml/stable-diffusion-v1-5",
    "device": "cuda",
    "pipeline_type": "StableDiffusionPipeline"
  }
}
```

### Health Check
**GET** `/api/v1/stable-diffusion/health`

Check if the service is ready and the model is loaded.

### Model Information
**GET** `/api/v1/stable-diffusion/model-info`

Get detailed information about the loaded model.

### Cleanup Resources
**POST** `/api/v1/stable-diffusion/cleanup`

Clean up GPU memory and model resources.

## 🎯 Usage Examples

### Python Example
```python
import requests
import base64
from PIL import Image
import io

# Generate an image
response = requests.post(
    "http://localhost:8000/api/v1/stable-diffusion/generate",
    json={
        "prompt": "A serene forest with sunlight filtering through the trees",
        "width": 768,
        "height": 768,
        "num_inference_steps": 30
    }
)

if response.status_code == 200:
    result = response.json()
    
    # Decode base64 image
    image_data = base64.b64decode(result["image_base64"])
    image = Image.open(io.BytesIO(image_data))
    
    # Save the image
    image.save("generated_image.png")
    print(f"Image generated in {result['generation_time']:.2f} seconds")
```

### cURL Example
```bash
curl -X POST "http://localhost:8000/api/v1/stable-diffusion/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "A futuristic city skyline at night with neon lights",
       "width": 512,
       "height": 512
     }'
```

### JavaScript Example
```javascript
const generateImage = async () => {
  const response = await fetch('http://localhost:8000/api/v1/stable-diffusion/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      prompt: 'A magical wizard casting spells in an enchanted forest',
      width: 512,
      height: 512,
      num_inference_steps: 40
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    // Display the base64 image
    const img = document.createElement('img');
    img.src = `data:image/png;base64,${result.image_base64}`;
    document.body.appendChild(img);
  }
};
```

## ⚙️ Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | **required** | Text description of the image to generate |
| `negative_prompt` | string | "blurry, low quality..." | What to avoid in the image |
| `width` | integer | 512 | Image width (256-1024) |
| `height` | integer | 512 | Image height (256-1024) |
| `num_inference_steps` | integer | 50 | Number of denoising steps (10-100) |
| `guidance_scale` | float | 7.5 | How closely to follow the prompt (1.0-20.0) |
| `seed` | integer | null | Random seed for reproducible results |

## 🔧 Technical Details

### Model Information
- **Model**: runwayml/stable-diffusion-v1-5
- **Type**: Text-to-Image Diffusion Model
- **Scheduler**: DPM Solver Multistep (for faster inference)
- **Safety**: Safety checker disabled for flexibility

### Performance Optimizations
- Automatic device detection (CUDA > MPS > CPU)
- Memory-efficient attention for CUDA devices
- Attention slicing to reduce memory usage
- Automatic memory cleanup after generation

### File Structure
```
app/
├── main.py                           # FastAPI application
├── features/
│   └── features-6/
│       ├── stable_diffusion_route.py # API routes
│       ├── stable_diffusion_schema.py # Request/response schemas
│       └── stable_diffusion_service.py # Core image generation logic
```

## 🐳 Docker Support

The project includes Docker configuration for easy deployment:

```bash
# Build the Docker image
docker build -t xobehstudio .

# Run the container
docker run -p 8000:8000 xobehstudio

# Or use docker-compose
docker-compose up
```

## 🛠️ Troubleshooting

### Common Issues

1. **CUDA Out of Memory**
   - Reduce image dimensions
   - Lower num_inference_steps
   - Use the cleanup endpoint between generations

2. **Slow Generation**
   - Ensure CUDA is available and working
   - Reduce num_inference_steps for faster (but lower quality) results

3. **Model Download Issues**
   - Ensure stable internet connection
   - The model (~4GB) will download automatically on first use

### Logs
The service provides detailed logging. Check the console output for any error messages or status updates.

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support, please open an issue in the project repository or contact the development team.

---

**Happy Creating! 🎨✨**
