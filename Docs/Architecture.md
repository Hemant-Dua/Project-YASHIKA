# Y.A.S.H.I.K.A. Architecture Documentation

## System Overview

Yashika is a multi-component personal AI system built around a FastAPI backend engine that orchestrates local LLM processing, web search capabilities, and system integration through dual frontend interfaces.

## Architecture Diagram
![Architecture Diagram](arch.svg)

*Figure 1: Complete system architecture showing component relationships and data flow*

## Component Architecture

### Core Engine (FastAPI Server)
Central orchestration layer handling all system operations:

```
FastAPI Server
├── Route Management
├── Context Processing  
├── Model Communication (Ollama)
├── Web Search Integration (DuckDuckGo)
├── System Command Execution
└── Memory Management
```

**Key Responsibilities:**
- Request routing and API endpoint management
- Context injection and conversation state management
- Integration between Ollama server and client interfaces
- Web search coordination and result processing
- System process execution and response handling

### LLM Processing Layer

**Ollama Server Integration:**
- Local model hosting and inference
- Context window management
- Model switching capabilities
- Prompt injection and response generation

**API Communication Flow:**
```
Client Request → FastAPI → Context Retrieval → Ollama API Call → Response Processing → Client
```

### Memory & Context Management

**Storage Architecture:**
- **Memory (memory.json)**: Complete conversation history persistence
- **Context (context.json)**: Latest 5 chat sessions in working memory
- **Logs (log.txt)**: Structured storage for all the conversation threads

**Prompt Injection Strategy:**
```
Base Prompt + Context + Relevant Memory + Current Input → Model Input
```

## Frontend Architecture

### Frontend 1: Web Interface
**Technology Stack:** HTML/CSS/JavaScript  
**Purpose:** Web Accessible Interface

```
User Input (Web) → FastAPI Engine → Engine Processing → Web Response
```

**Features:**
- Real-time chat interface
- Web search result integration
- Template-based UI rendering
- Cross-platform browser compatibility

**API Endpoints Used:**
- `POST /chat` – Primary conversation endpoint. Handles user input, local commands, search queries, and LLM responses.
- `GET /` – Serves the main HTML UI.
- `/static` – Serves static assets like CSS, JS, and images.

### Frontend 2: GTK Application

**Technology Stack:** GTK + Python  
**Purpose:** Desktop interface for system integration, hardware control, and interacting with FastAPI services

```
System Triggers → GTK App → FastAPI Server → Engine Services
```

**Features:**
- Native desktop interface with full-screen dashboard  
- Real-time clock, date, and battery monitoring  
- Chat interface for AI interaction  
- Process automation and triggers (planned for future)  

**FastAPI Endpoint Used by GTK App:**
- `POST /chat` – Sends user messages and receives streaming responses from the server.

**Note:** All other UI elements like dashboard buttons, clock, and battery display are handled locally. The GTK app acts as a client to the FastAPI server.

## Service Integration

### Web Search (DuckDuckGo)
**Integration Pattern:**
```
Search Trigger (/search <Query>) → DDGS API Call → Result Fetching → Result Summarization → Model Response
```

**Implementation Details:**
- Search is triggered from the chat via `/search <Query>` commands  
- Query is sent to the DuckDuckGo Search (DDGS) API  
- Raw results are fetched and summarized locally using the model  
- Summarized results are returned as part of the chat response  
- Fully integrated into the chat workflow for seamless interaction

### System Integration
**Process Execution Flow:**
```
User Command → Local Command Detection (against allowed command dictionaries) → Execute via Python Subprocess/os.startfile
```

**Capabilities:**
- Launch only pre-approved applications and games (e.g., VS Code, Chrome, Valorant)  
- Open allowed folders and system directories (e.g., Downloads, Desktop)  
- Execute whitelisted OS utilities (e.g., CMD, PowerShell, Settings)  
- Manage permitted processes and system tools (e.g., Task Manager, Snipping Tool)  
- Automate predefined tasks based on keyword triggers

## Data Flow Patterns

### Standard Chat Flow
```
Web UI/GTK App → FastAPI → Prompt Injection → Ollama API → Response Generation → Memory & Context Update → UI Update
```

### Web-Enhanced Chat Flow
```
Web UI / GTK App → FastAPI → Search Detection (/search <query>) → DuckDuckGo Search API → Result Fetch & Summarization → Model Response → Context & Memory Update → UI Update
```

### Local Command Detection and Execution
```
Web UI / GTK App → FastAPI → Keyword + Application/Process name → Command Execution → [Permission Check if Admin Task] → UI Update
```

## API Design

### Base URL
```
http://<host-ip>:7860
```

### Endpoints
1. ```POST /chat``` – Primary conversation endpoint. Handles user input, command detection, web search, and LLM-based responses.

    **Request Body (JSON):**
    ```
    {
    "message": "your input text here"
    }
    ```

    **Processing Flow:**

    - If message starts with /search <query> → performs DuckDuckGo search via yashika_browse.

    - Else if message matches local commands (handle_local_commands) → executes mapped system task.

    - Else → builds prompt with memory + context → streams response from the LLM.

    - Response (StreamingResponse, text/plain):
    Text stream of AI’s response (can be plain result, command output, or LLM-generated text).

2. ```GET /``` – Serves the main Web UI (HTML page).

    **Response:** Contents of index.html.

3. ```/static/{path}``` – Serves static assets for the web frontend (CSS, JS, images, etc.).

    **Response:** File contents with appropriate MIME type.

### Request/Response Patterns
#### 1. Chat with AI

**Request:** POST /chat  
Content-Type: application/json
```json
{
  "message": "Hello Yashika!"
}
```

**Response:**
```
Hi there! Ready to dominate another day, hero? 😎
```

#### 2. Search Example

**Request:** POST /chat  
Content-Type: application/json
```json
{
  "message": "/search FastAPI CORS example"
}
```

**Response:**
```
**To enable CORS in FastAPI, add the CORSMiddleware middleware and specify allowed origins in the allow_origins parameter.** - See FastAPI documentation on CORS for more information.
```

#### 3. Local Command Example

**Request:** POST /chat  
Content-Type: application/json
```json
{
  "message": "open chrome"
}
```

**Response:**
```
Opening chrome...
```

#### Key Notes

**Memory Management:**
- Context and memory updated per user input.
- Retains last 5 messages in context.

**Security:**
- Local commands are whitelisted only (from actions.py).
- No arbitrary command execution allowed.

**Streaming Responses:**
- Both search results and LLM outputs are streamed for real-time feel.

## Database Schema
*Not decided yet, Works purely on JSON*

## Development Considerations

### Security Implementation
- **Command Validation**: All system commands are defined beforehand and safe
- **Context Integration**: User input is injected with prompts and context before model processing

### Performance Optimization
- **Context Caching**: Frequent context patterns cached in memory
- **Async Processing**: Non-blocking operations for UI responsiveness
- **Model Warm-up**: Keep Ollama model loaded for instant responses
- **Memory Management**: Automatic cleanup of old conversation data

### Error Handling
- **Graceful Degradation**: System continues working if components fail
- **Fallback Mechanisms**: Alternative paths when services unavailable
- **Comprehensive Logging**: Detailed error tracking for debugging
- **User Feedback**: Clear error messages through both interfaces

## Deployment Architecture

### Local Development Setup
```
Ollama Server (Port 11434) → FastAPI Backend (Port 23256) → Web UI (Port 7860) + GTK App
```

### Production Deployment
- **Process Management**: Single bat file for automatic startup
- **Log Rotation**: Automated log management and cleanup
- **Update Mechanisms**: In-place updates without data loss

## Monitoring and Debugging

### Logging Strategy
- **Engine Logs**: FastAPI request/response logging
- **Model Logs**: Ollama interaction and performance metrics

### Performance Metrics
- **Response Times**: Model inference and API response latency
- **Memory Usage**: Context size and system resource utilization
- **Search Performance**: DuckDuckGo integration response times
- **System Command Execution**: Hardware operation success rates

### Debug Modes
- **Verbose Logging**: Detailed operation tracking
- **Context Inspection**: View exact context sent to model
- **API Tracing**: Track request flow through system components
- **Model Debugging**: Ollama server interaction details

## Implementation Notes

### Thread Safety
- **Concurrent Requests**: FastAPI handles multiple simultaneous conversations
- **Context Locking**: Prevent context corruption during updates
- **Model Queue**: Manage Ollama request queuing for resource optimization

### Resource Management
- **Memory Limits**: Configurable context window sizes
- **CPU Throttling**: Model inference rate limiting
- **Disk Usage**: Automatic conversation history cleanup
- **Network Bandwidth**: Efficient web search result processing

### Scalability Considerations
- **Model Switching**: Runtime model changes without restart
- **Distributed Processing**: Potential for multiple Ollama instances
- **Caching Strategies**: Optimize frequently accessed conversation patterns