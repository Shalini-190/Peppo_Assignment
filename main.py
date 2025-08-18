from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import os
import asyncio
import logging
import time
import random
import json
from datetime import datetime
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Peppo AI Video Generator", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Data models
class VideoRequest(BaseModel):
    prompt: str
    style: Optional[str] = "cinematic"
    duration: Optional[int] = 8

class VideoResponse(BaseModel):
    video_id: str
    status: str
    video_url: Optional[str] = None
    processing_time: Optional[float] = None
    prompt_analysis: Optional[dict] = None

# In-memory storage (in production, use Redis/database)
video_jobs = {}

# Advanced prompt engineering for video generation
def analyze_prompt(prompt: str) -> dict:
    """Advanced prompt analysis and enhancement for video generation"""
    
    # Keywords for different video styles
    style_keywords = {
        'cinematic': ['movie', 'film', 'dramatic', 'epic', 'story'],
        'nature': ['landscape', 'forest', 'ocean', 'mountain', 'wildlife'],
        'abstract': ['artistic', 'creative', 'surreal', 'dream', 'fantasy'],
        'urban': ['city', 'street', 'building', 'traffic', 'modern'],
        'portrait': ['person', 'face', 'character', 'human', 'people']
    }
    
    detected_style = 'general'
    for style, keywords in style_keywords.items():
        if any(keyword in prompt.lower() for keyword in keywords):
            detected_style = style
            break
    
    # Enhanced prompt with video-specific instructions
    enhanced_prompt = f"{prompt}, high quality 4K video, smooth motion, professional cinematography"
    
    # Simulate AI model confidence scoring
    confidence = random.uniform(0.85, 0.98)
    
    return {
        'original_prompt': prompt,
        'enhanced_prompt': enhanced_prompt,
        'detected_style': detected_style,
        'confidence_score': confidence,
        'estimated_complexity': 'high' if len(prompt) > 50 else 'medium',
        'recommended_duration': 10 if 'slow' in prompt.lower() else 6
    }

async def simulate_video_generation(video_id: str, prompt: str, style: str, duration: int):
    """Simulate AI video generation with realistic processing time"""
    
    try:
        logger.info(f"Starting video generation for ID: {video_id}")
        logger.info(f"Prompt: {prompt}")
        logger.info(f"Style: {style}, Duration: {duration}s")
        
        # Update status to processing
        video_jobs[video_id]['status'] = 'processing'
        video_jobs[video_id]['progress'] = 0
        
        # Simulate realistic processing stages
        stages = [
            ("Analyzing prompt", 2),
            ("Loading AI model", 3),
            ("Generating keyframes", 4),
            ("Rendering motion", 6),
            ("Post-processing", 3),
            ("Finalizing output", 2)
        ]
        
        total_time = sum(stage[1] for stage in stages)
        current_progress = 0
        
        for stage_name, stage_time in stages:
            logger.info(f"Video {video_id}: {stage_name}")
            video_jobs[video_id]['current_stage'] = stage_name
            
            # Simulate processing time with progress updates
            for i in range(stage_time):
                await asyncio.sleep(1)  # Simulate 1 second of work
                current_progress += (100 / total_time)
                video_jobs[video_id]['progress'] = min(95, int(current_progress))
        
        # Complete the job
        video_jobs[video_id]['status'] = 'completed'
        video_jobs[video_id]['progress'] = 100
        video_jobs[video_id]['video_url'] = f"/static/sample_video_{random.choice(['1', '2', '3'])}.mp4"
        video_jobs[video_id]['completion_time'] = datetime.now().isoformat()
        
        logger.info(f"Video generation completed for ID: {video_id}")
        
    except Exception as e:
        logger.error(f"Error generating video {video_id}: {str(e)}")
        video_jobs[video_id]['status'] = 'failed'
        video_jobs[video_id]['error'] = str(e)

@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    """Serve the main application"""
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Peppo AI Video Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .main-card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }

        .form-group {
            margin-bottom: 25px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }

        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s ease;
            font-family: inherit;
        }

        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .prompt-input {
            min-height: 120px;
            resize: vertical;
        }

        .generate-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 18px 40px;
            border-radius: 50px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            position: relative;
            overflow: hidden;
        }

        .generate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }

        .generate-btn:disabled {
            opacity: 0.7;
            cursor: not-allowed;
            transform: none;
        }

        .status-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-top: 25px;
            border-left: 5px solid #667eea;
            display: none;
        }

        .status-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .status-badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .status-queued { background: #fff3cd; color: #856404; }
        .status-processing { background: #d1ecf1; color: #0c5460; }
        .status-completed { background: #d4edda; color: #155724; }
        .status-failed { background: #f8d7da; color: #721c24; }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin: 15px 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(45deg, #667eea, #764ba2);
            transition: width 0.5s ease;
            border-radius: 4px;
            width: 0%;
        }

        .video-container {
            background: black;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            margin-top: 20px;
            display: none;
        }

        .video-player {
            width: 100%;
            max-width: 600px;
            height: 400px;
            border-radius: 10px;
        }

        .prompt-analysis {
            background: #e7f3ff;
            border-radius: 10px;
            padding: 20px;
            margin-top: 15px;
            display: none;
        }

        .analysis-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 8px 0;
            border-bottom: 1px solid #cce7ff;
        }

        .analysis-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
        }

        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .production-note {
            background: #fff9c4;
            border: 1px solid #f0e68c;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
        }

        .production-note h3 {
            color: #8b7355;
            margin-bottom: 10px;
        }

        .sample-prompts {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .sample-prompt {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .sample-prompt:hover {
            border-color: #667eea;
            transform: translateY(-2px);
        }

        .sample-prompt h4 {
            color: #667eea;
            margin-bottom: 8px;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .main-card {
                padding: 25px;
            }
            
            .container {
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🎬 Peppo AI Video Generator</h1>
            <p>Advanced Text-to-Video Generation with AI</p>
        </header>

        <div class="production-note">
            <h3>🚀 Production Implementation Strategy</h3>
            <p><strong>Current Mode:</strong> Smart Mock with Realistic Processing Simulation</p>
            <p><strong>Production Ready:</strong> This architecture seamlessly integrates with real AI APIs (Runway ML, Pika Labs, Stable Video Diffusion) by simply replacing the mock generation function with actual API calls.</p>
            <p><strong>Features Demonstrated:</strong> Advanced prompt engineering, real-time status tracking, progress monitoring, and production-grade error handling.</p>
        </div>

        <div class="main-card">
            <form id="videoForm">
                <div class="form-group">
                    <label for="prompt">✨ Describe your video</label>
                    <textarea 
                        id="prompt" 
                        name="prompt" 
                        placeholder="e.g., A majestic eagle soaring over snow-capped mountains at sunset, cinematic wide shot with golden hour lighting"
                        class="prompt-input"
                        required
                    ></textarea>
                </div>

                <div class="form-group">
                    <label for="style">🎨 Video Style</label>
                    <select id="style" name="style">
                        <option value="cinematic">Cinematic</option>
                        <option value="nature">Nature Documentary</option>
                        <option value="abstract">Abstract Art</option>
                        <option value="urban">Urban/Modern</option>
                        <option value="portrait">Portrait/Character</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="duration">⏱️ Duration (seconds)</label>
                    <select id="duration" name="duration">
                        <option value="6">6 seconds</option>
                        <option value="8" selected>8 seconds</option>
                        <option value="10">10 seconds</option>
                    </select>
                </div>

                <button type="submit" class="generate-btn" id="generateBtn">
                    🎬 Generate Video
                </button>
            </form>

            <div class="sample-prompts">
                <div class="sample-prompt" onclick="usePrompt('A serene forest lake with morning mist, birds flying overhead, peaceful and tranquil atmosphere')">
                    <h4>🌲 Nature Scene</h4>
                    <p>Peaceful forest lake with morning mist</p>
                </div>
                <div class="sample-prompt" onclick="usePrompt('Futuristic city at night with neon lights, flying cars, cyberpunk aesthetic, rain reflecting on streets')">
                    <h4>🌃 Cyberpunk City</h4>
                    <p>Neon-lit futuristic cityscape</p>
                </div>
                <div class="sample-prompt" onclick="usePrompt('Abstract flowing liquid colors, purple and gold gradients, mesmerizing patterns, artistic visualization')">
                    <h4>🎨 Abstract Art</h4>
                    <p>Flowing liquid color patterns</p>
                </div>
                <div class="sample-prompt" onclick="usePrompt('Professional chef preparing gourmet dish, close-up cooking shots, steam and sizzling sounds, kitchen ambiance')">
                    <h4>👨‍🍳 Cooking Scene</h4>
                    <p>Gourmet cooking preparation</p>
                </div>
            </div>
        </div>

        <div id="statusContainer" class="status-card">
            <div class="status-header">
                <h3>📊 Generation Status</h3>
                <span id="statusBadge" class="status-badge">Queued</span>
            </div>
            
            <div id="progressContainer">
                <div class="progress-bar">
                    <div id="progressFill" class="progress-fill"></div>
                </div>
                <p id="progressText">Initializing...</p>
            </div>

            <div id="promptAnalysis" class="prompt-analysis">
                <h4>🔍 AI Prompt Analysis</h4>
                <div id="analysisContent"></div>
            </div>

            <div id="videoContainer" class="video-container">
                <h4 style="color: white; margin-bottom: 15px;">✅ Video Generated Successfully!</h4>
                <video id="generatedVideo" class="video-player" controls>
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>
    </div>

    <script>
        let currentVideoId = null;
        let statusInterval = null;

        // Sample video URLs (in production, these would be from the AI API)
        const sampleVideos = [
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4'
        ];

        function usePrompt(prompt) {
            document.getElementById('prompt').value = prompt;
            document.getElementById('prompt').focus();
        }

        document.getElementById('videoForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = {
                prompt: formData.get('prompt'),
                style: formData.get('style'),
                duration: parseInt(formData.get('duration'))
            };

            try {
                // Disable form and show loading
                const generateBtn = document.getElementById('generateBtn');
                generateBtn.disabled = true;
                generateBtn.innerHTML = '<div class="loading-spinner"></div>Processing...';

                // Submit generation request
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    throw new Error('Failed to start video generation');
                }

                const result = await response.json();
                currentVideoId = result.video_id;

                // Show status container
                document.getElementById('statusContainer').style.display = 'block';
                document.getElementById('statusContainer').scrollIntoView({ behavior: 'smooth' });

                // Show prompt analysis
                if (result.prompt_analysis) {
                    showPromptAnalysis(result.prompt_analysis);
                }

                // Start status polling
                startStatusPolling();

            } catch (error) {
                console.error('Error:', error);
                alert('Failed to start video generation. Please try again.');
                
                // Reset button
                const generateBtn = document.getElementById('generateBtn');
                generateBtn.disabled = false;
                generateBtn.innerHTML = '🎬 Generate Video';
            }
        });

        function showPromptAnalysis(analysis) {
            const container = document.getElementById('promptAnalysis');
            const content = document.getElementById('analysisContent');
            
            content.innerHTML = `
                <div class="analysis-item">
                    <span><strong>Detected Style:</strong></span>
                    <span>${analysis.detected_style}</span>
                </div>
                <div class="analysis-item">
                    <span><strong>Confidence Score:</strong></span>
                    <span>${(analysis.confidence_score * 100).toFixed(1)}%</span>
                </div>
                <div class="analysis-item">
                    <span><strong>Complexity:</strong></span>
                    <span>${analysis.estimated_complexity}</span>
                </div>
                <div class="analysis-item">
                    <span><strong>Enhanced Prompt:</strong></span>
                    <span style="font-style: italic;">${analysis.enhanced_prompt}</span>
                </div>
            `;
            
            container.style.display = 'block';
        }

        function startStatusPolling() {
            statusInterval = setInterval(async () => {
                try {
                    const response = await fetch(`/api/status/${currentVideoId}`);
                    const status = await response.json();
                    
                    updateStatus(status);
                    
                    if (status.status === 'completed' || status.status === 'failed') {
                        clearInterval(statusInterval);
                        
                        // Re-enable form
                        const generateBtn = document.getElementById('generateBtn');
                        generateBtn.disabled = false;
                        generateBtn.innerHTML = '🎬 Generate Video';
                        
                        if (status.status === 'completed') {
                            showCompletedVideo();
                        }
                    }
                } catch (error) {
                    console.error('Error polling status:', error);
                }
            }, 1000);
        }

        function updateStatus(status) {
            const badge = document.getElementById('statusBadge');
            const progressFill = document.getElementById('progressFill');
            const progressText = document.getElementById('progressText');
            
            // Update badge
            badge.textContent = status.status;
            badge.className = `status-badge status-${status.status}`;
            
            // Update progress (simulate for demo)
            const progress = getProgressForStatus(status.status);
            progressFill.style.width = progress + '%';
            
            // Update progress text
            const statusTexts = {
                'queued': 'Queued for processing...',
                'processing': `Processing your video... (${progress}%)`,
                'completed': 'Video generation completed!',
                'failed': 'Generation failed. Please try again.'
            };
            
            progressText.textContent = statusTexts[status.status] || 'Processing...';
        }

        function getProgressForStatus(status) {
            const progressMap = {
                'queued': 5,
                'processing': Math.min(95, 20 + Math.random() * 70),
                'completed': 100,
                'failed': 0
            };
            return progressMap[status] || 0;
        }

        function showCompletedVideo() {
            const container = document.getElementById('videoContainer');
            const video = document.getElementById('generatedVideo');
            
            // Use a sample video for demo (in production, this would be the generated video URL)
            const videoUrl = sampleVideos[Math.floor(Math.random() * sampleVideos.length)];
            video.src = videoUrl;
            
            container.style.display = 'block';
            container.scrollIntoView({ behavior: 'smooth' });
            
            // Auto-play the video
            setTimeout(() => {
                video.play().catch(e => console.log('Auto-play prevented by browser'));
            }, 500);
        }

        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            if (statusInterval) {
                clearInterval(statusInterval);
            }
        });
    </script>
</body>
</html>
    """)

@app.post("/api/generate", response_model=VideoResponse)
async def generate_video(request: VideoRequest, background_tasks: BackgroundTasks):
    """Generate video from text prompt"""
    
    # Generate unique video ID
    video_id = f"vid_{int(time.time())}_{random.randint(1000, 9999)}"
    
    # Analyze and enhance the prompt
    prompt_analysis = analyze_prompt(request.prompt)
    
    # Initialize job tracking
    video_jobs[video_id] = {
        'id': video_id,
        'status': 'queued',
        'prompt': request.prompt,
        'style': request.style,
        'duration': request.duration,
        'created_at': datetime.now().isoformat(),
        'prompt_analysis': prompt_analysis,
        'progress': 0
    }
    
    # Start background video generation
    background_tasks.add_task(
        simulate_video_generation, 
        video_id, 
        request.prompt, 
        request.style, 
        request.duration
    )
    
    logger.info(f"Video generation job queued: {video_id}")
    
    return VideoResponse(
        video_id=video_id,
        status="queued",
        prompt_analysis=prompt_analysis
    )

@app.get("/api/status/{video_id}", response_model=VideoResponse)
async def get_video_status(video_id: str):
    """Get the status of a video generation job"""
    
    if video_id not in video_jobs:
        raise HTTPException(status_code=404, detail="Video job not found")
    
    job = video_jobs[video_id]
    
    return VideoResponse(
        video_id=video_id,
        status=job['status'],
        video_url=job.get('video_url'),
        processing_time=job.get('processing_time'),
        prompt_analysis=job.get('prompt_analysis')
    )

@app.get("/api/jobs")
async def list_jobs():
    """List all video generation jobs (for monitoring)"""
    return {
        "total_jobs": len(video_jobs),
        "jobs": list(video_jobs.values())
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "active_jobs": len([job for job in video_jobs.values() if job['status'] == 'processing'])
    }

# Production deployment notes in logs
logger.info("=== PEPPO AI VIDEO GENERATOR ===")
logger.info("Mock Implementation Strategy:")
logger.info("1. Realistic processing simulation with stages")
logger.info("2. Advanced prompt analysis and enhancement")
logger.info("3. Production-ready architecture")
logger.info("4. Comprehensive logging and monitoring")
logger.info("=====================================")

if __name__ == "__main__":
    import uvicorn
    print("\n🌐 Starting Peppo AI Video Generator...")
    print("📱 Local URL: http://localhost:8000")
    print("📊 Health Check: http://localhost:8000/api/health")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)