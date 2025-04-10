#🧠 Research Paper Summarization – Multi-Agent System
-A multi-agent system that automates the discovery, processing, summarization, and podcast generation of academic research papers. Built to help users stay updated on research across disciplines efficiently.

##📌 Features
* 🔍 Search for research papers via topic, URL, DOI, or PDF uploads
* 🧠 Extract and process content from academic papers
* 🗂️ Classify papers by topic
* ✍️ Summarize individual papers and synthesize across topics
* 🎧 Generate audio podcast versions of summaries
* 📎 Include citation tracking in summaries


##Agent	Role:
-🔍 Discovery Agent	Searches papers via topic, DOI, URL
-📄 Extraction Agent	Extracts metadata, abstract, and body content
-🏷️ Classification Agent	Categorizes paper using user-defined topic list
-📝 Summarization Agent	Creates structured summaries of individual papers
-🔄 Synthesis Agent	Merges insights across papers within a topic
-🔊 Audio Agent	Converts text summaries to speech using TTS
* Agents are modular and communicate via internal task routing, ensuring extensibility and parallel processing.

##⚙️ Setup Instructions
-🐳 Option 1: Docker (Recommended)
###bash
    -docker build -t research-summarizer .
    -docker run -p 5000:5000 research-summarizer
    
###💻 Option 2: Manual

-python -m venv venv
-source venv/bin/activate
-pip install -r requirements.txt
-python app.py

##📌 Citation System
-All outputs include traceable citations referencing the source paper and section for verifiability.

##🛠️ Tech Stack
-Python (FastAPI / Flask)
-LangChain + OpenAI (or other LLM)
-BeautifulSoup / PyMuPDF
-gTTS / pyttsx3 / ElevenLabs (for audio)
-Docker (for packaging)

##🚧 Limitations
-Complex math or formulae not summarized well
-Audio lacks expressive narration
-Limited to English papers

##🔮 Future Improvements
-Add UI for summary review and editing
-Support non-English papers
-Add better voice customization and podcast structure
