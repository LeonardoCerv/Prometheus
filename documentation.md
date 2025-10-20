# 🤖 Prometheus - Technical Documentation

## 📋 Table of Contents

- [System Overview](#-system-overview)
- [Technical Architecture](#-technical-architecture)
- [Core Features](#-core-features)
- [Technology Stack](#-technology-stack)
- [Data Models](#-data-models)
- [API Design](#-api-design)
- [AI Integration](#-ai-integration)
- [Implementation Plan](#-implementation-plan)
- [Testing Strategy](#-testing-strategy)
- [Deployment](#-deployment)

---

## 🎯 System Overview

### Problem Statement

Current recruitment processes in LATAM face two critical challenges:

1. **Candidate Side**: Professionals struggle to present their skills effectively. Traditional CVs don't capture transferable skills or context.

2. **Recruiter Side**: Manual filtering of hundreds of resumes takes days. By the time a good candidate is identified, they've often accepted other offers.

**Note**: For this 48-hour hackathon, the entire system operates in English only, though designed for LATAM markets with future multilingual support planned.

### Solution Architecture

Prometheus creates an automated pipeline:

**Input Layer** → Candidates register via LinkedIn OAuth, Gmail OAuth, or manual entry  
**Processing Layer** → Gemini AI analyzes and structures profiles  
**Matching Layer** → Semantic AI matching (not keyword-based)  
**Communication Layer** → WhatsApp delivery (98% open rate)  
**Action Layer** → Automated meeting scheduling via LLM function calling, Google Calendar integration, and **ADK Python agent orchestration**

### Key Metrics

- **Onboarding Time**: 30 seconds (OAuth) vs 2 minutes (manual) vs 15 minutes (traditional forms)
- **Registration Options**: LinkedIn, Gmail, Manual, CV Upload
- **Matching Accuracy**: ~85% with semantic analysis
- **Response Rate**: 98% (WhatsApp) vs 20% (email)
- **Time-to-Meeting**: 2 minutes vs 3-5 days
- **Cost per Match**: $0.005 (Twilio message cost)

---

## 🏗 Technical Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Presentation Layer                  │
│  - Next.js 15 App Router (React Server Components)  │
│  - Tailwind CSS (Styling)                           │
│  - NextAuth.js (OAuth Management)                   │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│                   API Layer                         │
│  - Next.js 15 API Routes (Serverless Functions)     │
│  - RESTful endpoints                                │
│  - Webhook handlers                                 │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│                 Business Logic Layer                │
│  - Profile Analysis (Gemini Pro)                    │
│  - Semantic Matching (Gemini 2.0 Flash)             │
│  - Job Posting Generation (Gemini Pro)              │
│  - Intent Recognition (Function Calling)            │
│  - Agent Automation (Google ADK - Python)           │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│                   Data Layer                        │
│  - Firestore (NoSQL Database)                       │
│  - Firebase Storage (File Storage)                  │
│  - Firebase Auth (Identity Management)              │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│              External Integrations                  │
│  - LinkedIn OAuth 2.0                               │
│  - Twilio WhatsApp API                              │
│  - Google Gemini API                                │
│  - Google Calendar API                              │
│  - Google Agent Development Kit                     │
└─────────────────────────────────────────────────────┘
```

### Component Architecture

**Frontend Components:**
- CandidateRegistration: Multi-option registration (LinkedIn/CV/Manual)
- ChatInterface: Conversational search for recruiters
- MatchCard: Display candidate matches with scores
- ProfilePreview: Show AI-structured profiles

**Backend Services:**
- AuthService: NextAuth configuration and session management
- ProfileAnalysisService: CV parsing with Gemini
- MatchingService: Semantic compatibility calculation
- WhatsAppService: Message sending and webhook processing
- SchedulingService: Meeting creation and management

**Data Flow:**
1. User action → Frontend component
2. Component → API endpoint (Next.js route)
3. API → Business logic service
4. Service → AI processing (Gemini) or database (Firestore)
5. Response → Frontend update

---

## 🚀 Core Features

### 1. Multi-Modal Candidate Registration

**LinkedIn OAuth Flow:**
- Integration with LinkedIn OAuth 2.0
- Scopes: openid, profile, email
- Obtains: name, email, profile picture
- User provides LinkedIn description text
- Gemini extracts structured data

**Gmail OAuth Flow:**
- Integration with Google OAuth 2.0
- Scopes: profile, email
- Obtains: name, email, profile picture
- User provides additional professional details
- Gemini extracts structured data

**Manual Registration Flow:**
- Traditional email/password registration
- Comprehensive profile form
- Skills selection and experience input
- CV upload option
- Email verification required

**CV Upload Flow (Standalone or Combined):**
- **Resume format: PDF files only**
- Text extraction from uploaded PDF documents
- Gemini parsing to structured JSON
- Validation and data cleaning
- Maximum file size: 10MB

**Technical Requirements:**
- NextAuth.js for OAuth management (LinkedIn + Gmail)
- LinkedIn Developer App with verified redirect URLs
- Google Cloud Console with OAuth credentials
- Gemini Pro API for text analysis
- **PDF parsing library (e.g., pdf-parse) for resume extraction**
- Firestore for profile storage
- Firebase Storage for PDF file storage

### 2. Semantic Matching Engine

**Traditional Matching (Keywords):**
- Exact string matching
- Boolean logic (AND/OR)
- Limited context understanding
- High false negative rate

**AI Semantic Matching:**
- Natural language understanding
- Context-aware analysis
- Transferable skills recognition
- Experience relevance evaluation

**Matching Algorithm:**

Input: Candidate profile + Job requirements

Process:
1. Extract skills from both sides
2. Calculate skill overlap
3. Evaluate transferable skills (e.g., Vue.js → React)
4. Assess experience relevance
5. Check availability compatibility
6. Generate composite score (0-100)

Output: Match score + reasoning + strengths + gaps

**Scoring Formula:**
- Skill Match: 50% weight
- Experience Match: 30% weight
- Availability Match: 20% weight
- Threshold: Only show matches ≥ 60%

### 3. Conversational Recruiter Interface

**Natural Language Processing:**
- Recruiter types in plain language
- Gemini extracts structured requirements
- No forms or dropdowns needed

**Example Input (English for Hackathon):**
"I need a senior React developer with Next.js experience for a 3-month project"

**Extracted Structure:**
- Role: React Developer Senior
- Skills: [React, Next.js]
- Type: Freelance
- Level: Senior
- Duration: 3 months

**Search Execution:**
1. Query all candidates from database
2. For each candidate, call matching API
3. Calculate score with Gemini
4. Filter by threshold (≥60%)
5. Sort by score descending
6. Return top 5 matches

### 4. WhatsApp Communication Layer

**Why WhatsApp:**
- 90% penetration in LATAM
- 98% message open rate (vs 20% email)
- Familiar interface for candidates
- Real-time notification delivery
- Two-way conversation support

**Language Limitation (Hackathon):**
- System currently supports English only
- Designed for LATAM market but English-first for demo purposes
- Future iterations will include Spanish and other regional languages

**Message Flow:**

Outbound (System → Candidate):
1. Recruiter selects candidates
2. Gemini generates personalized job posting
3. System formats for WhatsApp (max 300 words)
4. Twilio API sends message
5. Delivery status tracked in database

Inbound (Candidate → System):
1. Twilio webhook receives message
2. System identifies candidate by phone number
3. Gemini processes message with function calling
4. Appropriate action executed
5. Confirmation sent back to candidate

### 5. Automated Scheduling with Function Calling and Agent Orchestration

**Agent-Driven Architecture:**

Google ADK (Python) enables sophisticated multi-step automation:

**SchedulingAgent Flow:**
- Receives candidate scheduling request
- Analyzes calendar availability using Google Calendar API
- Checks for conflicts and suggests alternatives
- Creates calendar events with video conference links
- Sends automated confirmations and reminders
- **Monitors invitation responses and handles status changes**
- **Automatically reschedules when meetings are declined**
- Handles rescheduling and cancellation requests

**CommunicationAgent Flow:**
- Monitors candidate responses and engagement
- Analyzes sentiment and intent from WhatsApp messages
- Generates personalized follow-up communications
- Schedules automated reminder sequences
- **Tracks calendar invitation responses and sends appropriate follow-ups**
- **Manages communication flows based on acceptance/decline status**
- Tracks communication effectiveness

**Function Calling Architecture:**

Gemini 2.0 Flash supports structured function definitions with agent integration:

**Function: schedule_meeting**
- Parameters: candidate_phone, date, time (optional)
- Triggers when: Candidate expresses intent to schedule
- Actions: Create meeting record, create Google Calendar event, send confirmation

**Function: show_interest**
- Parameters: candidate_phone, questions (array)
- Triggers when: Candidate shows interest with questions
- Actions: Log interest, notify recruiter

**Function: decline_offer**
- Parameters: candidate_phone, reason
- Triggers when: Candidate declines
- Actions: Update match status, log reason

**Processing Flow:**
1. Receive WhatsApp message
2. Gemini analyzes intent
3. If function call detected, extract parameters
4. Execute corresponding business logic (including Calendar API)
5. Generate natural language response
6. Send confirmation via WhatsApp

**Google Calendar Integration:**
- Automatic event creation with candidate and recruiter details
- Video conference links (Zoom/Meet) attached to events
- Email notifications sent to all participants
- Calendar sync across devices
- Conflict detection and alternative time suggestions

**Date Parsing:**
- Natural language input: "20 de octubre", "next Monday"
- Gemini extracts ISO format: 2025-10-20
- Validation against available dates and calendar conflicts
- Default time assignment if not specified

---

## 🛠 Technology Stack

### Frontend Framework: Next.js 15

**Rationale:**
- Latest stable version with enhanced performance and features
- App Router for modern React patterns
- Server Components for optimal performance
- API Routes for backend logic
- Built-in TypeScript support
- Built-in optimization (images, fonts)
- Easy Vercel deployment

**Key Features Used:**
- Server Components for data fetching
- Client Components for interactivity
- API Routes as serverless functions
- Middleware for authentication
- Dynamic routing
- TypeScript for type safety

### Authentication: NextAuth.js

**Rationale:**
- Supports multiple OAuth providers (LinkedIn, Gmail)
- Traditional email/password authentication
- Session management out-of-the-box
- JWT token handling
- Secure callbacks
- Easy provider integration

**OAuth Providers:**
- **LinkedIn**: Professional profile data
- **Gmail**: Basic profile and email verification

**Configuration Requirements:**
- LinkedIn Provider setup with app credentials
- Google Provider setup with OAuth client ID/secret
- Email Provider for manual registration
- Callback URL registration for all providers
- Secret generation (openssl)
- Session strategy (JWT)
- Custom callbacks for token handling

### Database: Firebase Firestore

**Rationale:**
- NoSQL flexibility for varied profile structures
- Real-time capabilities (future feature)
- Easy querying with SDK
- Automatic scaling
- Free tier sufficient for hackathon

**Collections Design:**
- candidates/ - User profiles
- matches/ - Compatibility records
- job_postings/ - Recruiter job listings
- meetings/ - Scheduled appointments

**Query Patterns:**
- Get all candidates: collection('candidates').get()
- Filter by type: where('userType', '==', 'talent')
- Find matches: where('candidate_id', '==', candidateId)

### AI Engine: Google Gemini

**Models Used:**

**Gemini Pro:**
- CV analysis and parsing
- Job posting generation
- General text processing
- Cost: Free tier available

**Gemini 2.0 Flash:**
- Function calling support
- Faster inference
- WhatsApp response processing
- Meeting scheduling logic

**API Integration:**
- REST API via @google/generative-ai package
- Prompt engineering for consistent JSON output
- Error handling for malformed responses
- Rate limiting considerations

### Messaging: Twilio WhatsApp

**Setup Requirements:**
- Twilio account (free sandbox for testing)
- WhatsApp Sandbox activation
- Webhook URL configuration
- Account SID and Auth Token

**Sandbox Limitations:**
- 10 messages per day (testing)
- Users must "join" with code
- Pre-approved message templates
- Upgrade to production for unlimited

**API Operations:**
- Send message: client.messages.create()
- Receive webhook: POST to /api/whatsapp-webhook
- Validate Twilio signature
- Parse incoming message body

### Calendar Integration: Google Calendar API

**Rationale:**
- Automated meeting scheduling directly in calendars
- Sync with existing calendar systems
- Automatic reminders and notifications
- Integration with video conferencing tools

**Setup Requirements:**
- Google Cloud Project with Calendar API enabled
- OAuth 2.0 credentials (Client ID and Secret)
- Service account for server-side operations
- Calendar sharing permissions

**API Operations:**
- Create events: calendar.events.insert()
- Update events: calendar.events.update()
- Delete events: calendar.events.delete()
- List events: calendar.events.list()
- Send notifications: calendar.events.patch() with reminders

**Authentication:**
- OAuth 2.0 flow for user consent
- Refresh tokens for long-term access
- Service account authentication for automated operations

### Agent Automation: Google Agent Development Kit (Python)

**Rationale:**
- Advanced AI agent capabilities for complex workflows
- Integration with Google Workspace tools (Calendar, Gmail, Docs)
- Multi-step task automation and decision making
- Enhanced scheduling and communication orchestration
- **Python-based implementation** (separate from Next.js/TypeScript frontend)

**Setup Requirements:**
- Google Cloud Project with ADK enabled
- Service account with appropriate permissions
- Python environment with ADK SDK installation (`pip install google-adk`)
- Agent configuration and tool definitions in Python

**Key Features:**
- **Calendar Agent**: Intelligent scheduling with conflict resolution
- **Communication Agent**: Automated email follow-ups and reminders
- **Document Agent**: Generate meeting notes and feedback forms
- **Workflow Orchestration**: Multi-step recruitment processes

**Agent Types:**
- **SchedulingAgent**: Handles meeting coordination and calendar management
- **CommunicationAgent**: Manages candidate communications and follow-ups
- **MatchingAgent**: Advanced candidate-job matching with contextual analysis
- **OnboardingAgent**: Automates initial candidate engagement workflows

**ADK Python API Operations:**
- Create agent instances: `Agent(name="...", model="...", instruction="...", tools=[...])`
- Execute agent tasks: `await agent.run_async(context)` (where context is InvocationContext)
- Monitor agent status: Use callbacks or check session state
- Handle agent responses: Access via `context.state` or `agent.output_key`

**Integration Architecture:**
- ADK agents run as separate Python services
- Communication with Next.js backend via REST APIs or message queues
- Agents triggered by Next.js API routes when complex workflows are needed
- Agent responses processed and stored in Firestore for frontend consumption

### Hosting: Vercel

**Rationale:**
- Optimized for Next.js
- Automatic deployments from Git
- Environment variables management
- Edge functions support
- Free tier sufficient

**Deployment Process:**
- Connect GitHub repository
- Configure environment variables
- Automatic build on push
- Preview deployments for PRs
- Production deployment on merge

---

## 📊 Data Models

### Candidate Profile

**Schema:**
```
{
  id: string (auto-generated)
  auth: {
    provider: "linkedin" | "google" | "email" | "manual"
    linkedinId: string (optional)
    googleId: string (optional)
    email: string
    emailVerified: boolean
    image: string (URL)
  }
  profile: {
    name: string
    title: string
    location: string
    bio: string (max 200 chars)
    skills: string[] (array of technical skills)
    experience: [
      {
        company: string
        role: string
        duration: string
        description: string
      }
    ]
    availability: "full-time" | "part-time" | "freelance"
    languages: string[]
    experience_years: number
  }
  whatsapp: string (phone number with country code)
  rawCV: string (original text input)
  **cvPdfUrl: string (Firebase Storage URL for uploaded PDF)**
  source: string (registration method)
  created_at: timestamp
  updated_at: timestamp
  status: "active" | "inactive" | "hired"
}
```

### Match Record

**Schema:**
```
{
  id: string
  candidate_id: string (reference)
  job_posting_id: string (reference)
  recruiter_id: string (reference)
  score: number (0-100)
  matchDetails: {
    skillMatch: number
    experienceMatch: number
    availabilityMatch: number
    reasoning: string
    strengths: string[]
    gaps: string[]
  }
  status: "pending" | "contacted" | "scheduled" | "rejected" | "hired"
  whatsapp_sent: boolean
  whatsapp_sent_at: timestamp
  candidate_response: string
  meeting_id: string (optional reference)
  created_at: timestamp
  updated_at: timestamp
}
```

### Job Posting

**Schema:**
```
{
  id: string
  recruiter_id: string
  requirements: {
    role: string
    skills: string[]
    type: "full-time" | "part-time" | "freelance"
    level: "junior" | "mid" | "senior"
    duration: string
    description: string
  }
  generated_description: string (AI-generated text)
  candidates_matched: number
  candidates_contacted: number
  meetings_scheduled: number
  matches: string[] (array of match IDs)
  created_at: timestamp
  status: "active" | "filled" | "cancelled"
}
```

### Meeting

**Schema:**
```
{
  id: string
  candidate_id: string
  candidate_phone: string
  job_posting_id: string
  recruiter_id: string
  scheduled_date: string (YYYY-MM-DD)
  scheduled_time: string (HH:MM)
  timezone: string
  meeting_link: string (Zoom/Meet URL)
  calendar_event_id: string (Google Calendar event ID)
  status: "scheduled" | "completed" | "cancelled" | "rescheduled"
  reminders_sent: boolean
  created_at: timestamp
  completed_at: timestamp (optional)
}
```

### Indexing Strategy

**Firestore Indexes Required:**
- candidates: composite index on (status, created_at)
- matches: composite index on (candidate_id, score DESC)
- matches: composite index on (job_posting_id, score DESC)
- meetings: composite index on (scheduled_date, status)

---

## 🔌 API Design

### Authentication Endpoints

**POST /api/auth/signin/linkedin**
- Initiates LinkedIn OAuth flow
- Redirects to LinkedIn authorization
- Returns to callback URL with code

**GET /api/auth/callback/linkedin**
- Receives OAuth code from LinkedIn
- Exchanges code for access token
- Creates session with user data
- Redirects to registration page

**POST /api/auth/signin/google**
- Initiates Gmail OAuth flow
- Redirects to Google authorization
- Returns to callback URL with code

**GET /api/auth/callback/google**
- Receives OAuth code from Google
- Exchanges code for access token
- Creates session with user data
- Redirects to registration page

**POST /api/auth/signin/email**
- Initiates email/password authentication
- Validates credentials against database
- Creates session on successful login
- Returns user profile data

**POST /api/auth/signup**
- Creates new user account with email/password
- Sends email verification
- Creates basic profile structure
- Redirects to profile completion

### Profile Management Endpoints

**POST /api/analyze-cv**
- Input: cvText (string), linkedinData (object, optional), **pdfFile (File object, optional)**
- Process: Extract text from PDF if provided, Gemini Pro analyzes text
- Output: Structured profile JSON
- **Storage**: PDF stored in Firebase Storage with reference URL
- Error handling: Malformed JSON, API errors, invalid PDF format

**POST /api/linkedin-profile**
- Input: linkedinId, name, email, image
- Process: Creates basic profile from OAuth data
- Output: Profile object with needsCompletion flag
- Note: Limited data from OAuth, user must complete

### Matching Endpoints

**POST /api/calculate-match**
- Input: candidateProfile (object), jobRequirements (object)
- Process: Gemini analyzes compatibility
- Output: Score (0-100), reasoning, strengths, gaps
- Caching: Consider caching for same candidate-job pairs

**POST /api/search**
- Input: jobRequirements (object)
- Process: Query all candidates, calculate matches
- Output: Array of candidates with scores ≥ 60
- Optimization: Parallel matching requests

### Chat Endpoints

**POST /api/chat**
- Input: message (string), conversationHistory (array)
- Process: Gemini extracts intent and requirements
- Output: type ("search" | "conversation"), message, candidates (optional)
- State management: Maintain conversation context

### WhatsApp Endpoints

**POST /api/send-offer**
- Input: candidates (array), jobRequirements, recruiterId
- Process: Generate job posting, send via Twilio
- Output: Success status, message IDs
- Side effects: Create matches in database

**POST /api/whatsapp-webhook**
- Input: Twilio webhook payload (form data)
- Process: Extract message, identify candidate, call Gemini
- Output: 200 OK (Twilio requires quick response)
- Async processing: Queue heavy operations

**GET /api/whatsapp-webhook**
- Purpose: Twilio webhook verification
- Output: Status message

### Scheduling Endpoints

**POST /api/schedule**
- Input: candidateId, date, time, jobPostingId
- Process: Validate date, check calendar conflicts, create meeting record, create Google Calendar event
- Output: Meeting object with confirmation
- Notifications: Send confirmations to both parties, calendar invites

**POST /api/calendar/auth**
- Input: authorization code from Google OAuth
- Process: Exchange code for tokens, store refresh token
- Output: Success status

**GET /api/calendar/events**
- Input: date range (optional)
- Process: Fetch calendar events for conflict checking
- Output: Array of busy time slots

**DELETE /api/calendar/event/:eventId**
- Input: eventId
- Process: Cancel meeting, remove from calendar
- Output: Success status

---

## 🤖 AI Integration

### Google Agent Development Kit Configuration

**Agent Architecture:**
- Modular agent design with specialized capabilities
- Tool integration for Google Workspace APIs
- State management for multi-step workflows
- Error handling and recovery mechanisms

**Parallel Agent Architecture:**
- **Main Orchestrator Agent** (Sequential): Triggers parallel processing, coordinates results, manages overall workflow state
- **Parallel Worker Agents**: Multiple agents working simultaneously for different tasks
- **Communication Pattern**: Orchestrator → Parallel Workers → Results Aggregation → Response

**Parallel Processing Benefits:**
- Process multiple CVs simultaneously (10 CVs in ~3 seconds vs 30 seconds sequential)
- Handle multiple WhatsApp conversations concurrently
- Schedule meetings for different candidates in parallel
- Scale to handle peak loads with multiple recruiters active

**Recommended Agent Structure:**
```
RecruitmentOrchestrator (SequentialAgent)
├── Triggers parallel processing
├── Coordinates results
└── Manages overall workflow state

CandidateProcessor (ParallelAgent)
├── CVAnalyzerAgent #1
├── CVAnalyzerAgent #2
└── CVAnalyzerAgent #3

CommunicationAgents (ParallelAgent)
├── WhatsAppAgent #1
├── WhatsAppAgent #2
└── EmailAgent #1

SchedulingAgents (ParallelAgent)
├── CalendarAgent #1
├── CalendarAgent #2
└── ConflictResolverAgent #1
```

**Why Parallel Agents for Recruitment:**
- Multiple candidates need simultaneous processing
- Recruiters handle multiple job postings concurrently
- WhatsApp conversations happen asynchronously
- Calendar scheduling involves multiple stakeholders
- Faster response times and better user experience

**ADK Agent Instantiation (Python Code):**

```python
from google.adk.agents import Agent
from google.adk.tools import google_search  # Example tool import

# Example SchedulingAgent using ADK's LlmAgent
scheduling_agent = Agent(
    name="scheduling_agent",
    model="gemini-2.0-flash-exp",  # Or other supported models
    instruction="""
    You are a scheduling assistant. Handle meeting coordination, check calendar conflicts, 
    create events, and manage responses. Use tools to interact with calendars and send notifications.
    When a meeting is accepted, send confirmation. If declined, suggest alternatives.
    """,
    tools=[google_calendar_tool, time_parser_tool],  # Actual Python tool objects/functions
    output_key="scheduling_result"  # Optional: Store final response in session state
)

# Example CommunicationAgent
communication_agent = Agent(
    name="communication_agent",
    model="gemini-2.0-flash-exp",
    instruction="""
    You are a communication assistant. Monitor candidate responses, analyze sentiment, 
    generate personalized follow-ups, and schedule reminders. Handle WhatsApp and email communications.
    """,
    tools=[whatsapp_tool, email_tool, sentiment_analyzer_tool],
    output_key="communication_result"
)
```

**Agent Workflow Example:**
1. Candidate expresses interest via WhatsApp
2. CommunicationAgent analyzes response sentiment
3. SchedulingAgent checks calendar availability
4. If available, creates calendar event and sends confirmation
5. If conflict, CommunicationAgent sends alternative time suggestions

**Calendar Invitation Response Handling:**

**Response Status Monitoring:**
- **Accepted**: CommunicationAgent sends confirmation and meeting details
- **Declined**: SchedulingAgent suggests alternative times, CommunicationAgent sends follow-up
- **Tentative**: CommunicationAgent sends reminder with meeting details
- **Needs Action**: CommunicationAgent sends gentle reminder after 24 hours

**Automated Follow-up Sequences:**
- **Immediate Response**: Thank candidate and provide meeting details
- **24h Reminder**: If no response, send gentle reminder
- **Alternative Suggestions**: If declined, propose 2-3 new time slots
- **Final Follow-up**: After multiple declines, notify recruiter for manual intervention

**Smart Rescheduling Logic:**
- **Conflict Detection**: Check both calendars for availability
- **Time Zone Handling**: Convert times to candidate's timezone
- **Business Hours**: Respect typical working hours (9 AM - 6 PM)
- **Buffer Time**: Add 15-minute buffers between meetings

**Complete Meeting Lifecycle Management:**

**Pre-Meeting Phase:**
- Initial scheduling request processing
- Calendar conflict detection and resolution
- Invitation creation and delivery
- Response status monitoring

**Response Phase:**
- Real-time tracking of invitation responses
- Automated follow-ups for non-responses
- Alternative time slot suggestions for declines
- Sentiment analysis of candidate communications

**Confirmation Phase:**
- Final confirmation upon acceptance
- Meeting details delivery via multiple channels
- Calendar event updates with final details
- Reminder scheduling (24h, 1h, 15min before)

**Post-Meeting Phase:**
- Meeting completion tracking
- Follow-up communication scheduling
- Feedback request automation
- Performance analytics and reporting

**Integration with Gemini:**
- ADK agents (Python) can call Gemini for complex reasoning
- Function calling enhanced with agent orchestration
- Multi-agent collaboration for complex tasks
- **Agents communicate with Next.js backend via REST APIs**

**Monitoring and Logging:**
- Agent execution tracking via custom logging
- Performance metrics collection (implement separately)
- Error reporting and recovery
- Audit trails for compliance

### Gemini API Configuration

**Authentication:**
- API Key from Google AI Studio
- Store in environment variable
- Pass as header or query parameter

**Model Selection:**
- gemini-pro: General text processing
- gemini-2.0-flash-exp: Function calling support

**Rate Limits:**
- Free tier: 60 requests per minute
- Consider batching for multiple candidates
- Implement exponential backoff for errors

### Prompt Engineering

**CV Analysis Prompt Structure:**

System Context:
- Define role: "You are a professional profile analyzer"
- Specify output format: "Return ONLY valid JSON"
- List required fields explicitly

Input Processing:
- Include raw CV text
- Add LinkedIn data if available
- Specify field extraction rules

Output Format:
- Define JSON schema
- Specify data types
- Provide examples of expected output

Error Handling:
- Instruct to use reasonable defaults
- Request inference for missing fields
- Avoid hallucination of data

**Matching Prompt Structure:**

Comparison Framework:
- List candidate skills and experience
- List job requirements
- Define evaluation criteria

Scoring Methodology:
- Explain weighting system
- Define transferable skills concept
- Set threshold for recommendation

Output Requirements:
- Structured score breakdown
- Human-readable reasoning
- Specific strengths and gaps

**Job Posting Generation Prompt:**

Content Requirements:
- Attractive title
- Brief introduction (2-3 lines)
- Bullet points for responsibilities
- Clear requirements
- Benefits or value proposition

Format Constraints:
- Maximum 300 words (WhatsApp limit)
- Use emojis appropriately
- Include clear call-to-action
- Professional but approachable tone

**Function Calling Configuration:**

Function Definitions:
```
functions = [
  {
    name: "schedule_meeting"
    description: "Use when candidate wants to schedule"
    parameters: {
      candidate_phone: string
      date: string (YYYY-MM-DD)
      time: string (HH:MM, optional)
    }
  },
  {
    name: "show_interest"
    description: "Use when candidate shows interest with questions"
    parameters: {
      candidate_phone: string
      interest_level: "high" | "medium"
      questions: string[]
    }
  },
  {
    name: "decline_offer"
    description: "Use when candidate declines"
    parameters: {
      candidate_phone: string
      reason: string
    }
  }
]
```

Model Configuration:
- Model: gemini-2.0-flash-exp
- Tools: [{ functionDeclarations: functions }]
- Process response.functionCalls()[0]

### Response Parsing

**JSON Extraction:**
- Use regex to find JSON in response text
- Pattern: /\{[\s\S]*\}/
- Parse with try-catch for errors
- Validate required fields exist

**Error Recovery:**
- Retry with modified prompt if parsing fails
- Use default values for optional fields
- Log failures for debugging
- Return user-friendly error messages

---

## 📅 Implementation Plan (48 Hours)

### Monday - Day 1

**Morning Session (4 hours):**

Hour 1: Environment Setup
- Create Next.js 15 project with TypeScript
- Install dependencies (firebase, @google/generative-ai, twilio, next-auth, googleapis)
- Configure environment variables
- Initialize Firebase project
- Set up Firestore collections
- Configure Google Cloud Project and Calendar API
- **Set up separate Python environment for ADK agents**

Hour 2: Authentication Implementation
- Configure NextAuth with LinkedIn, Gmail, and Email providers
- Create callback routes for all OAuth providers
- Test OAuth flows for each provider
- Implement session management
- Set up Google OAuth for Calendar access
- Create manual registration and login forms

Hour 3: Registration Page
- Build UI with 4 registration options (LinkedIn, Gmail, Manual, CV Upload)
- Create OAuth callback handling for all providers
- Implement email verification for manual registration
- Create profile completion forms
- Add loading states and error handling

Hour 4: CV Analysis API
- Create /api/analyze-cv endpoint
- Integrate Gemini Pro
- Implement JSON parsing
- Test with sample CVs
- Save profiles to Firestore

**Afternoon Session (5 hours):**

Hour 1-2: Chat Interface
- Build conversational UI
- Message history management
- Input handling
- Typing indicators

Hour 3: Matching Engine
- Create /api/calculate-match endpoint
- Implement Gemini matching logic
- Test scoring algorithm
- Validate output format

Hour 4: Search Functionality
- Create /api/chat endpoint
- Implement requirement extraction
- Build /api/search endpoint
- Integrate matching calls

Hour 5: Database Population
- Create 5-10 test candidate profiles
- Vary skills and experience levels
- Test search and matching
- Verify score calculations

**Evening Session (6 hours):**

Hour 1: Job Posting Generation
- Create generation function
- Implement Gemini prompt
- Format for WhatsApp
- Test output quality

Hour 2-3: Twilio Integration
- Set up Twilio account
- Activate WhatsApp Sandbox
- Create send message function
- Build /api/send-offer endpoint

Hour 4: WhatsApp Testing
- Send test messages to personal numbers
- Verify delivery
- Test different message formats
- Handle errors

Hour 5: End-to-End Flow Testing
- Register candidate
- Recruiter searches
- Send offers
- Verify WhatsApp delivery

Hour 6: Bug Fixes and Sleep
- Fix critical issues
- Commit code
- Sleep minimum 1 hour

### Tuesday - Day 2

**Morning Session (4 hours):**

Hour 1: Webhook Setup
- Create /api/whatsapp-webhook endpoint
- Configure Twilio webhook URL
- Test incoming message reception
- Implement candidate identification

Hour 2-3: Function Calling
- Configure Gemini with function definitions
- Implement function execution logic
- Create meeting scheduling logic
- Integrate Google Calendar event creation
- Test calendar API operations

Hour 4: Response Handling
- Generate confirmation messages
- Send via Twilio
- Update database status
- Send calendar notifications
- Test complete scheduling flow

**Afternoon Session (3 hours):**

Hour 1: UI Polish
- Improve styling with Tailwind
- Add loading animations
- Implement error states
- Responsive design adjustments

Hour 2: Comprehensive Testing
- Test LinkedIn OAuth flow
- Test Gmail OAuth flow
- Test manual registration and login
- Test CV analysis accuracy
- Test matching algorithm
- Test WhatsApp bidirectional flow
- Test function calling edge cases

Hour 3: Demo Preparation
- Prepare 3 test profiles with real phone numbers
- Create sample job search queries
- Practice demo flow 3 times
- Record backup video
- Prepare presentation slides

**Presentation (Evening):**
- 5-minute live demo
- Q&A with judges

---

## 🧪 Testing Strategy

### Unit Testing Approach

**Profile Analysis:**
- Test Cases: 5 different CV formats
- Validate: All required fields extracted
- Edge Cases: Missing information, non-standard formats
- Expected Output: Valid JSON matching schema

**Matching Algorithm:**
- Test Cases: High match (90%), medium (70%), low (40%)
- Validate: Score calculations, reasoning quality
- Edge Cases: No skill overlap, all skills match
- Expected Output: Score within expected range

**Function Calling:**
- Test Cases: Schedule intent, interest intent, decline intent
- Validate: Correct function triggered, parameters extracted
- Edge Cases: Ambiguous messages, multiple intents
- Expected Output: Appropriate function call with valid params

### Integration Testing

**OAuth Flows:**
1. **LinkedIn**: Click sign-in → Authorize → Verify callback → Check session → Confirm redirect
2. **Gmail**: Click sign-in → Authorize → Verify callback → Check session → Confirm redirect
3. **Manual Registration**: Fill form → Verify email → Complete profile → Login test

**End-to-End Recruitment Flow:**
1. Candidate registers (any method: LinkedIn/Gmail/Manual)
2. Profile analyzed and saved
3. Recruiter searches
4. Matches calculated
5. Offers sent via WhatsApp
6. Candidate responds
7. Meeting scheduled
8. Confirmations sent

**WhatsApp Communication:**
1. Send message from system
2. Verify delivery status
3. Receive reply via webhook
4. Process with Gemini
5. Send confirmation
6. Verify received by candidate

### Load Testing Considerations

**Concurrent Matching:**
- Scenario: 10 candidates × 1 job posting
- Expected: All matches calculated in parallel
- Timeout: 30 seconds maximum
- Error Handling: Retry failed matches

**Gemini API Limits:**
- Rate: 60 requests per minute (free tier)
- Strategy: Batch processing if > 60 candidates
- Fallback: Queue system for overload

---

## 🚀 Deployment

### Environment Configuration

**Development (.env.local):**
- Use localhost URLs
- ngrok for WhatsApp webhook testing
- Debug mode enabled
- Verbose logging

**Production (Vercel):**
- Production URLs
- Secure credentials
- Error tracking (optional: Sentry)
- Performance monitoring

### Pre-Deployment Checklist

**Code Quality:**
- Remove console.logs
- Add error boundaries
- Implement loading states
- Handle edge cases

**Security:**
- Validate all inputs
- Sanitize user data
- Secure API keys
- Implement rate limiting

**Configuration:**
- Update LinkedIn redirect URLs
- Update Twilio webhook URLs
- Set NEXTAUTH_URL to production domain
- Verify all environment variables

### Vercel Deployment Steps

1. Push code to GitHub
2. Connect repository to Vercel
3. Configure environment variables in dashboard
4. Deploy to production
5. Test deployed application
6. Monitor for errors

### Post-Deployment Updates

**LinkedIn App:**
- Add production redirect URL
- Keep localhost for development
- Verify app

**Twilio:**
- Update webhook URL to production
- Test message sending
- Verify webhook reception

---

## 📈 Performance Optimization

### API Response Times

**Target Times:**
- CV Analysis: < 3 seconds
- Matching Calculation: < 2 seconds per candidate
- Search with 10 candidates: < 30 seconds
- WhatsApp Send: < 1 second
- Webhook Processing: < 5 seconds

**Optimization Strategies:**
- Parallel matching requests
- Cache Gemini responses (optional)
- Optimize Firestore queries
- Use indexes for common queries

### Database Optimization

**Query Optimization:**
- Create compound indexes
- Limit result sets (pagination)
- Use select() to fetch only needed fields
- Cache frequently accessed data

**Connection Pooling:**
- Firebase SDK handles automatically
- Reuse Firestore instance
- Close connections properly

### AI Response Optimization

**Prompt Optimization:**
- Keep prompts concise
- Use clear instructions
- Avoid unnecessary context
- Request structured output explicitly

**Model Selection:**
- Use Gemini 2.0 Flash for speed-critical operations
- Use Gemini Pro for complex analysis
- Consider response time vs. accuracy tradeoff

---

## 🔒 Security Considerations

### Authentication Security

**OAuth Implementation:**
- Use HTTPS only
- Validate state parameter
- Verify token signatures
- Implement CSRF protection

**Session Management:**
- Short-lived sessions (24 hours)
- Secure cookie flags (httpOnly, secure)
- Session invalidation on logout
- Refresh token rotation

### API Security

**Input Validation:**
- Validate all request parameters
- Sanitize user input
- Check data types
- Limit payload sizes

**Rate Limiting:**
- Implement per-IP limits
- Use exponential backoff
- Block malicious actors
- Monitor for abuse

### Data Privacy

**Personal Information:**
- Store minimum required data
- Encrypt sensitive fields
- Implement data retention policies
- GDPR compliance considerations

**WhatsApp Messages:**
- Don't log message content
- Store only metadata
- Anonymize analytics data
- Clear old conversations

---

## 🐛 Error Handling

### API Error Responses

**Standard Error Format:**
```
{
  success: false
  error: string (human-readable message)
  code: string (error code for debugging)
  timestamp: ISO timestamp
}
```

**HTTP Status Codes:**
- 200: Success
- 400: Bad request (invalid input)
- 401: Unauthorized (auth required)
- 403: Forbidden (insufficient permissions)
- 500: Internal server error
- 503: Service unavailable (API down)

### Client-Side Error Handling

**Network Errors:**
- Display user-friendly message
- Provide retry option
- Log error for debugging
- Maintain app state

**Validation Errors:**
- Inline field validation
- Clear error messages
- Highlight problematic fields
- Prevent form submission

### AI Service Errors

**Gemini API Failures:**
- Retry with exponential backoff
- Fall back to simpler prompt
- Return partial results if possible
- Log for manual review

**Parsing Errors:**
- Attempt to extract partial JSON
- Use default values
- Request user to retry
- Notify development team

---

## 📚 Technical Documentation Standards

### Code Documentation

**Function Documentation:**
- Purpose: What the function does
- Parameters: Types and descriptions
- Return Value: Type and description
- Example: Sample usage

**API Documentation:**
- Endpoint URL and method
- Request body schema
- Response body schema
- Error responses
- Example requests

### Database Documentation

**Collection Schemas:**
- Field names and types
- Required vs optional fields
- Validation rules
- Relationships to other collections

**Query Examples:**
- Common query patterns
- Index requirements
- Performance considerations

---

## 🔄 Maintenance and Monitoring

### Monitoring Strategy

**Key Metrics:**
- API response times
- Error rates by endpoint
- Gemini API usage
- Twilio message delivery rate
- User registration conversion

**Monitoring Tools:**
- Vercel Analytics (built-in)
- Firebase Console (database metrics)
- Custom logging (structured logs)

### Maintenance Tasks

**Daily:**
- Check error logs
- Monitor API rate limits
- Verify WhatsApp delivery

**Weekly:**
- Review user feedback
- Analyze matching accuracy
- Update test data

**Monthly:**
- Optimize database indexes
- Review and optimize prompts
- Update dependencies

---

## 📖 Additional Resources

### Official Documentation

- **Next.js**: https://nextjs.org/docs
- **NextAuth.js**: https://next-auth.js.org/
- **Firebase**: https://firebase.google.com/docs
- **Gemini API**: https://ai.google.dev/docs
- **Twilio WhatsApp**: https://www.twilio.com/docs/whatsapp
- **Google Calendar API**: https://developers.google.com/calendar/api
- **Google Agent Development Kit**: https://cloud.google.com/agent-development-kit

### LinkedIn OAuth

- **LinkedIn Developers**: https://www.linkedin.com/developers/
- **OAuth 2.0 Flow**: https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication

### Function Calling

- **Gemini Function Calling Guide**: https://ai.google.dev/docs/function_calling
- **Best Practices**: Parameter descriptions, clear function purposes

---

## 🎯 Success Criteria

### Technical Criteria

- [ ] LinkedIn OAuth fully functional
- [ ] Gmail OAuth fully functional
- [ ] Manual registration and login working
- [ ] CV analysis achieving >80% accuracy
- [ ] Matching algorithm producing relevant scores
- [ ] WhatsApp messages delivered successfully
- [ ] Function calling triggering appropriate actions
- [ ] Google Calendar events created automatically
- [ ] **ADK Python agents orchestrating complex workflows**
- [ ] End-to-end flow working without errors

### User Experience Criteria

- [ ] Registration completed in <1 minute
- [ ] Search results returned in <30 seconds
- [ ] WhatsApp messages formatted properly
- [ ] Meeting scheduling intuitive and fast
- [ ] Error messages clear and actionable

### Performance Criteria

- [ ] API response times within targets
- [ ] No crashes or critical bugs
- [ ] Handles 10+ concurrent users
- [ ] Database queries optimized
- [ ] AI responses within 5 seconds