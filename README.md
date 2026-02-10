# 🎯 SmartRecruit - AI-Powered Job Recruitment Platform with Intelligent Chatbot

![Java](https://img.shields.io/badge/Java-17-orange?style=for-the-badge&logo=java)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.x-brightgreen?style=for-the-badge&logo=springboot)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Ollama](https://img.shields.io/badge/Ollama-AI%20Chat-purple?style=for-the-badge&logo=meta)
![AI](https://img.shields.io/badge/AI-Powered-red?style=for-the-badge&logo=openai)

## 🌟 Overview

SmartRecruit is an **intelligent, full-stack web application** that revolutionizes the recruitment process by integrating:
- 🤖 **AI-powered candidate screening** (Python)
- 💬 **Intelligent chatbot assistant** (Ollama LLM)
- 🎯 **Automated resume evaluation**
- 📊 **Smart HR dashboard**

The platform combines **Java Spring Boot** backend, **Python AI algorithms**, and a **locally-running Ollama chatbot** to create a complete, intelligent recruitment solution.

**🎓 AI Degree Project | SLIIT | Full-Stack Development + Dual AI Integration**

---

## ✨ Key Features

### 🏢 For Employers (HR Dashboard)
- ✅ **Post Job Openings** - Create detailed job listings
- 🤖 **AI Auto-Screening** - Python-based resume evaluation
- 💬 **AI Chatbot Assistant** - Get recruitment advice from SmartRecruit Bot
- 📊 **Smart Dashboard** - Manage all postings and applications
- 🎯 **Intelligent Filtering** - Auto-accept candidates scored >50%
- 📄 **Resume Management** - Download and review CVs
- ✏️ **Full CRUD Operations** - Edit and delete job listings

### 💼 For Job Seekers
- 🔍 **Advanced Job Search** - Filter by title, location, keywords
- 📤 **One-Click Apply** - Upload resume instantly
- 💬 **24/7 AI Assistant** - Chat with SmartRecruit Bot for help
- 🤖 **Career Guidance** - Get personalized job recommendations
- 🔐 **Secure Profiles** - Authentication and profile management
- 📱 **Responsive Design** - Apply from any device

### 🤖 Dual AI-Powered Features

#### AI Resume Screening (Python)
- 🧠 Intelligent resume parsing
- 📈 0-100% candidate scoring
- 🚫 Auto-rejection (≤50%)
- ✅ Auto-acceptance (>50%)
- 🎯 Keyword matching with job requirements

#### AI Chatbot (Ollama)
- 💬 **Natural conversations** - Context-aware responses
- 🎭 **Custom character** - Trained as SmartRecruit assistant
- 📚 **Recruitment expertise** - Answers job-related questions
- 🕐 **24/7 availability** - Always ready to help
- 🔒 **Runs locally** - Privacy-focused, no external API calls
- 🚀 **Real-time responses** - Fast, intelligent assistance

---

## 🛠️ Tech Stack

### Backend (Java)
- **Java 17** - Modern Java development
- **Spring Boot 3.x** - Application framework
- **Spring Security** - Authentication & authorization
- **Spring Data JPA** - ORM and database operations
- **H2 Database** - Embedded in-memory database
- **Thymeleaf** - Server-side templating
- **Maven** - Dependency management

### AI Modules

#### Resume Screening (Python)
- **Python 3.x** - AI/ML processing
- **Custom Algorithm** - Resume scoring engine
- **Text Analysis** - Keyword extraction
- **File Processing** - PDF/Word parsing

#### Chatbot (Ollama)
- **Ollama** - Local LLM runtime
- **Custom Model** - Trained SmartRecruit character
- **REST API** - Real-time communication
- **Context Management** - Conversation history
- **Prompt Engineering** - Recruitment-focused responses

### Frontend
- **HTML5/CSS3** - Modern web standards
- **Bootstrap 5** - Responsive UI framework
- **JavaScript** - Interactive features
- **Chat Widget** - Embedded chatbot interface
- **Font Awesome** - Professional icons
- **Google Fonts (Poppins)** - Typography
- **AOS.js** - Smooth scroll animations

### Integration Layer
- **Java ↔ Python** - Resume AI processing
- **Java ↔ Ollama** - Chatbot communication
- **File Upload System** - Multipart handling
- **RESTful Architecture** - Clean API design

---

## 📸 Screenshots

### 🏠 Home Page with AI Chatbot
![Home Page](https://via.placeholder.com/800x400/0f172a/d4af37?text=SmartRecruit+with+AI+Chatbot)
*Modern landing page with floating chatbot assistant*

### 💬 AI Chatbot in Action
![Chatbot](https://via.placeholder.com/800x400/0f172a/d4af37?text=SmartRecruit+AI+Assistant)
*Natural language conversation with SmartRecruit Bot*

### 💼 Job Listings
![Job Listings](https://via.placeholder.com/800x400/0f172a/d4af37?text=Job+Listings+Page)
*Search and filter jobs with chatbot help*

### 📊 HR Dashboard
![HR Dashboard](https://via.placeholder.com/800x400/0f172a/d4af37?text=HR+Command+Center)
*Manage postings with AI assistant guidance*

### 🤖 AI Resume Screening
![AI Screening](https://via.placeholder.com/800x400/0f172a/d4af37?text=AI+Candidate+Screening)
*Automated evaluation with color-coded scores*

---

## 🚀 Getting Started

### Prerequisites

```bash
✅ Java 17 or higher (JDK)
✅ Python 3.8 or higher
✅ Maven 3.6+
✅ Ollama (for chatbot)
✅ Git
✅ IDE (IntelliJ IDEA / Eclipse / VS Code)
```

### Installation Steps

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/oshan3kanayake/smartrecruit.git
cd smartrecruit
```

#### 2️⃣ Install Python Dependencies
```bash
# If you have requirements.txt
pip install -r requirements.txt

# Or install manually
pip install [your-python-libraries]
```

#### 3️⃣ Install and Setup Ollama (Chatbot)
```bash
# Install Ollama (visit https://ollama.ai for your OS)

# Pull your model (example: llama2, mistral, etc.)
ollama pull llama2

# Start Ollama server
ollama serve
```

#### 4️⃣ Configure Ollama Character (SmartRecruit Bot)
```bash
# Create Modelfile for custom character
ollama create smartrecruit-bot -f Modelfile

# Example Modelfile content:
# FROM llama2
# SYSTEM """You are SmartRecruit AI Assistant, a helpful recruitment 
# expert. You help job seekers find opportunities and guide HR 
# professionals with hiring advice. You are professional, friendly, 
# and knowledgeable about the job market."""
```

#### 5️⃣ Configure Application
```properties
# src/main/resources/application.properties

# H2 Database
spring.datasource.url=jdbc:h2:mem:smartrecruit
spring.datasource.driverClassName=org.h2.Driver
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect

# File Upload
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB

# Ollama Chatbot (if configured)
ollama.api.url=http://localhost:11434
ollama.model.name=smartrecruit-bot
```

#### 6️⃣ Build the Project
```bash
mvn clean install
```

#### 7️⃣ Run the Application
```bash
# Terminal 1: Start Ollama (if not running)
ollama serve

# Terminal 2: Start Spring Boot
mvn spring-boot:run
```

#### 8️⃣ Access the Application
```
🌐 Application: http://localhost:8080
💬 Chatbot: Available on all pages (bottom-right)
📊 H2 Console: http://localhost:8080/h2-console
🤖 Ollama API: http://localhost:11434
```

---

## 💬 Chatbot Features

### SmartRecruit AI Assistant

The chatbot is powered by **Ollama** running locally and customized with a SmartRecruit character persona.

#### What the Chatbot Can Do:

✅ **Job Search Help**
```
User: "Show me software engineering jobs"
Bot: "I'd be happy to help! You can use the search bar above to find 
      software engineering positions. Would you like me to guide you 
      through the application process?"
```

✅ **Application Guidance**
```
User: "How do I apply for a job?"
Bot: "To apply: 1) Click on any job listing, 2) Review the details, 
      3) Click 'Apply', 4) Upload your resume. Our AI will automatically 
      screen your application!"
```

✅ **HR Support**
```
User: "How does the AI screening work?"
Bot: "Our AI analyzes resumes against job requirements and scores 
      candidates 0-100%. Scores above 50% are auto-accepted. You can 
      review all scores in the applications page!"
```

✅ **Career Advice**
```
User: "Tips for my resume?"
Bot: "Great question! Make sure to: Include relevant keywords from 
      job descriptions, highlight measurable achievements, keep it 
      concise (1-2 pages), and tailor it for each application."
```

---

## 🤖 AI Systems Breakdown

### System 1: Resume Screening AI (Python)

**Purpose:** Evaluate candidate-job fit automatically

**How it works:**
1. Job seeker uploads resume (PDF/Word)
2. Java backend calls `predicted.py`
3. Python extracts text and analyzes content
4. Scores candidate 0-100% based on:
    - Keyword matching
    - Experience relevance
    - Skills alignment
    - Education background
5. Returns score to Java
6. System auto-accepts (>50%) or rejects (≤50%)

### System 2: Conversational AI (Ollama)

**Purpose:** Provide 24/7 intelligent assistance

**How it works:**
1. User types message in chat widget
2. JavaScript sends message to Java backend
3. ChatbotService calls Ollama API
4. Ollama processes with SmartRecruit character context
5. Returns natural language response
6. JavaScript displays response in chat

**Why Local (Ollama)?**
- ✅ **Privacy** - No data sent to external APIs
- ✅ **Free** - No API costs
- ✅ **Fast** - Low latency responses
- ✅ **Customizable** - Full control over character
- ✅ **Offline capable** - Works without internet (after model download)

---

## 🎯 Scoring System

### AI Resume Evaluation

| Score | Status | Color | Meaning |
|-------|--------|-------|---------|
| **70-100%** | ⭐ Excellent | 🟢 Green | Perfect match - High priority |
| **50-69%** | ✅ Good | 🟡 Yellow | Acceptable match - Auto-accepted |
| **0-49%** | ❌ Poor | 🔴 Red | Weak match - Auto-rejected |

---

## 🔒 Security Features

- 🔐 Spring Security authentication
- 🔑 BCrypt password encryption
- 🛡️ CSRF protection
- 📝 Input validation & sanitization
- 📂 Secure file upload validation
- 🤖 Local AI - No data leaves your server
- 👤 Session management

---

## 🎓 Learning Outcomes

This project demonstrates mastery in:

✅ **Full-Stack Development** - Complete web application  
✅ **Spring Framework** - Boot, Security, Data JPA  
✅ **Dual AI Integration** - Python + Ollama chatbot  
✅ **LLM Implementation** - Local language model deployment  
✅ **Database Design** - ORM, relationships, queries  
✅ **Authentication** - Secure user management  
✅ **File Handling** - Multipart uploads, processing  
✅ **RESTful APIs** - Clean endpoint design  
✅ **Responsive UI/UX** - Modern frontend design  
✅ **System Integration** - Java-Python-Ollama communication  
✅ **Prompt Engineering** - Custom chatbot character  
✅ **Real-time Features** - Live chat implementation

---

## 🚀 Deployment

### For Free Deployment:

#### Option 1: Render.com ⭐ (Recommended)
```bash
1. Push code to GitHub
2. Sign up at render.com
3. Create new Web Service
4. Connect GitHub repository
5. Set build command: mvn clean package
6. Set start command: java -jar target/smartrecruit.jar
7. Add Python environment
8. Deploy!
```

#### Option 2: Railway.app 🚂
- Supports both Java and Python
- Free tier available
- Automatic deployments

#### Option 3: Heroku (Student Pack) 🎓
- Free with GitHub Student Developer Pack
- Buildpacks for Java + Python

**Note:** Chatbot (Ollama) runs locally for demos. Production deployment would require VPS with adequate resources.

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Browser                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Web Pages  │  │  Chat Widget │  │ File Upload  │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│              Spring Boot Application                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Controllers (REST Endpoints)                    │  │
│  └──────┬────────────┬──────────────┬────────────┬──┘  │
│         │            │              │            │      │
│  ┌──────▼───┐  ┌────▼─────┐  ┌────▼─────┐  ┌───▼────┐ │
│  │ Security │  │ Services │  │   JPA    │  │ Config │ │
│  └──────────┘  └────┬─────┘  └────┬─────┘  └────────┘ │
└──────────────────────┼─────────────┼────────��──────────┘
                       │             │
          ┌────────────┼─────────────┼────────────┐
          │            │             │            │
          ▼            ▼             ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
    │   H2    │  │ Python  │  │ Ollama  │  │  File   │
    │Database │  │AI Score │  │Chatbot  │  │ System  │
    └─────────┘  └─────────┘  └─────────┘  └─────────┘
     (In-mem)    (predicted)   (Local LLM)  (uploads/)
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

---

## 📝 Future Enhancements

- [ ] Chatbot personality customization
- [ ] Multi-language chatbot support
- [ ] Video interview scheduling via chatbot
- [ ] Email notifications with AI summaries
- [ ] Advanced analytics dashboard
- [ ] LinkedIn integration
- [ ] Mobile app (React Native)
- [ ] Dark mode theme
- [ ] Export reports (PDF/Excel)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**Oshan Sadaruwan Ekanayake**

🎓 Artificial Intelligence Degree Student  
🏫 Sri Lanka Institute of Information Technology (SLIIT)  
💼 Aspiring AI Engineer & Full-Stack Developer  
🌟 Open to Internship & Collaboration Opportunities

**Specialties:**
- Full-Stack Development (Java, Spring Boot)
- AI/ML Integration (Python, LLMs)
- Chatbot Development (Ollama, Prompt Engineering)
- Database Design & Security

**Connect with me:**
- 🐙 **GitHub:** [@oshan3kanayake](https://github.com/oshan3kanayake)
- 📧 **Email:** oekanayake@gmail.com
- 💼 **LinkedIn:** [Connect with me](https://linkedin.com/in/yourprofile) *(Add your LinkedIn)*
- 🌐 **Portfolio:** *(Add if you have one)*

---

## 🙏 Acknowledgments

- SLIIT Faculty and Professors
- Spring Boot & Spring Security teams
- Python & Ollama communities
- Bootstrap & Font Awesome
- Open source contributors
- My peers and fellow students

---

<div align="center">

### ⭐ Star this repo if you find it useful! ⭐

**Built with ❤️ | Java + Python + Ollama AI**

*AI Degree Capstone Project - SLIIT*

*Showcasing advanced full-stack development with dual AI integration*

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=oshan3kanayake.smartrecruit)

</div>