# Video Editor API

This project provides a RESTful API for video editing, allowing you to upload, trim, merge videos, and generate shareable links for them.

---

## Features

- **Upload Video**: Save videos to the server and store metadata (e.g., size, duration).
- **Trim Video**: Extract specific segments of a video.
- **Merge Videos**: Combine multiple video files into one.
- **Generate Shareable Link**: Create unique, time-bound links for sharing videos.

---

## Technologies Used

- **Python** (Flask)
- **SQLAlchemy** (Database ORM)
- **MoviePy** (Video processing)
- **SQLite** (Default database for development)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/video-editor-api.git
   cd video-editor-api
   

python3 -m venv venv
source venv/bin/activate  # For Windows, use `venv\Scripts\activate`


To install dependencies
`pip3 install -r requirements.txt`


**To run the server**
`python3 main.py runserver`
