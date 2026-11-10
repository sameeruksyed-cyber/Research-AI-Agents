# ResearchOS

ResearchOS is a Streamlit interface for a four-stage research pipeline:

1. Search for recent and relevant sources with Tavily.
2. Read a selected source in depth.
3. Write a structured research report with Groq.
4. Critique the finished report.

## Setup

Create a root `.env` file:

```env
GROQ_API_KEY=your-groq-api-key
TAVILY_API_KEY=your-tavily-api-key
```

Install dependencies in the project environment:

```powershell
python -m pip install -r requirements.txt
```

Start the app:

```powershell
streamlit run streamlit_app.py
```

The app opens at `http://localhost:8501`.
