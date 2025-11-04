# Prometheus

[![Python](https://badges.0xleo.dev/badge?text=Python\&bgColor=3776AB\&textColor=FFFFFF\&iconColor=FFFFFF\&icon=simple-icons\:python)](https://www.python.org/)
[![TypeScript](https://badges.0xleo.dev/badge?text=TypeScript\&bgColor=3178C6\&textColor=FFFFFF\&iconColor=FFFFFF\&icon=simple-icons\:typescript)](https://www.typescriptlang.org/)
[![Next.js](https://badges.0xleo.dev/badge?text=Next.js\&bgColor=000000\&textColor=FFFFFF\&iconColor=FFFFFF\&icon=simple-icons\:nextdotjs)](https://nextjs.org/)
[![Flask](https://badges.0xleo.dev/badge?text=Flask\&bgColor=000000\&textColor=FFFFFF\&iconColor=FFFFFF\&icon=simple-icons\:flask)](https://flask.palletsprojects.com/)
[![Firebase](https://badges.0xleo.dev/badge?text=Firebase\&bgColor=FFCA28\&textColor=000000\&iconColor=000000\&icon=simple-icons\:firebase)](https://firebase.google.com/)
[![Google AI](https://badges.0xleo.dev/badge?text=Google%20AI\&bgColor=4285F4\&textColor=FFFFFF\&iconColor=FFFFFF\&icon=simple-icons\:google)](https://ai.google/)
[![React](https://badges.0xleo.dev/badge?text=React\&bgColor=61DAFB\&textColor=000000\&iconColor=000000\&icon=simple-icons\:react)](https://reactjs.org/)
[![Tailwind CSS](https://badges.0xleo.dev/badge?text=Tailwind%20CSS\&bgColor=06B6D4\&textColor=FFFFFF\&iconColor=FFFFFF\&icon=simple-icons\:tailwindcss)](https://tailwindcss.com/)

A platform for finding people using natural language. Prometheus reimagines talent discovery through conversational AI, enabling employers to find ideal candidates and professionals to be discovered through intelligent, progressive search capabilities.

---

## Overview

Prometheus transforms traditional recruitment by replacing keyword-based searches with natural language conversations. Our AI-powered platform understands context, intent, and nuance, delivering more accurate and efficient talent matching than conventional Applicant Tracking Systems.

## Core Technology

### Conversational Search Engine
- Natural language processing for intuitive candidate discovery
- Progressive filtering that refines results through multi-turn conversations
- Semantic matching that identifies transferable skills and potential

### Dual Platform Architecture
- **For Employers**: Conversational search interface for precise talent acquisition
- **For Professionals**: Passive discovery system that matches opportunities automatically

### AI-Powered Matching
- Google ADK agents trained on recruitment domain knowledge
- Real-time conversation context maintenance
- Confidence scoring and detailed match explanations

## System Architecture

![System Architecture](architecture.png)

The platform consists of:
- **Frontend**: Next.js-based web application with responsive design
- **Backend**: Flask API server handling AI agent orchestration
- **AI Layer**: Google ADK agents for natural language processing and matching
- **Data Layer**: Firebase Firestore for scalable user data management
- **Communication**: Integrated messaging for seamless employer-candidate interaction

## Technology Stack

### Backend
| Technology              | Purpose                          |
| ----------------------- | -------------------------------- |
| Python 3.8+             | AI orchestration and core logic  |
| Flask                   | REST API endpoints               |
| Google ADK              | Conversational AI agents         |
| Firebase Admin SDK      | Server-side data management      |

### Frontend
| Technology           | Purpose                     |
| -------------------- | --------------------------- |
| TypeScript           | Type-safe development       |
| Next.js              | Server-side rendered React  |
| React                | Component-based UI          |
| Tailwind CSS         | Utility-first styling       |

### Infrastructure
| Component         | Platform          |
| ----------------- | ----------------- |
| Hosting           | Vercel + Railway  |
| Database          | Firebase Firestore|
| Authentication    | Firebase Auth     |
| AI Services       | Google AI         |
| Messaging         | Twilio            |

## Key Features

- **Conversational Search**: Find candidates through natural language queries
- **Progressive Refinement**: Each conversation builds on previous context
- **Semantic Matching**: AI understands skills, experience, and potential
- **Real-time Communication**: Integrated chat for immediate engagement
- **Scalable Architecture**: Built for enterprise-level deployment

## Business Value

Prometheus addresses critical inefficiencies in modern recruitment:

- **Time Reduction**: 70% faster candidate identification through AI
- **Quality Improvement**: Better matches through semantic understanding
- **Cost Efficiency**: Reduced recruitment overhead and agency fees
- **Scalability**: Handles large talent pools with consistent accuracy

## Use Cases

- **Enterprise Recruitment**: Large organizations managing high-volume hiring
- **Specialized Staffing**: Technical roles requiring specific skill combinations
- **Freelance Platforms**: Project-based talent matching
- **Career Development**: Professional skill assessment and market positioning

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 18+
- Firebase project
- Google AI API access

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/LeonardoCerv/Prometheus.git
   cd Prometheus
   ```

2. **Backend Setup**
   ```bash
   pip install -r requirements.txt
   python server.py
   ```

3. **Frontend Setup**
   ```bash
   cd Frontend
   npm install
   npm run dev
   ```

4. **Configuration**
   - Configure Firebase credentials
   - Set up Google AI API keys
   - Initialize database with sample data

## Deployment

The platform is designed for cloud deployment with:
- Containerized backend services
- CDN-optimized frontend delivery
- Auto-scaling infrastructure
- Enterprise-grade security and compliance

## Acknowledgments

- Google AI team for advanced language models
- Firebase team for scalable backend infrastructure
- Open-source community for foundational technologies