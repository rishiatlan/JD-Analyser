# Job Description Analyser

A smart application that enables recruiters to refine job descriptions for clarity, inclusivity, and industry alignment. The application dynamically enhances JDs by analyzing structure, language biases, readability, and SEO performance.

## Features

- Multiple input methods (text, file upload, structured form)
- Dynamic JD structuring & enhancement
- Gender-neutral & bias-free language optimization
- Readability & SEO analysis
- Interactive enhancement with user confirmation
- Atlan-aligned design & branding

## Tech Stack

- Backend: Python FastAPI
- Frontend: React with TypeScript
- Database: PostgreSQL
- AI/ML: OpenAI GPT-4
- Authentication: JWT

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the backend:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

## Environment Variables

Create a `.env` file with the following variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/jd_analyzer
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET=your_jwt_secret
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 