# Rolai Backend API Documentation

## Table of Contents
1. [Authentication Endpoints](#1-authentication-endpoints)
2. [Chat Endpoints](#2-chat-endpoints)
3. [Conversation Endpoints](#3-conversation-endpoints)
4. [Agent Endpoints](#4-agent-endpoints)
5. [Smart Tasks Endpoints](#5-smart-tasks-endpoints)
6. [Organization Endpoints](#6-organization-endpoints)
7. [Deep Research Endpoints](#7-deep-research-endpoints)
8. [Knowledge Base Integration Endpoints](#8-knowledge-base-integration-endpoints)
9. [Flow Endpoints](#9-flow-endpoints)
10. [Document Endpoints](#10-document-endpoints)

## 1. Authentication Endpoints

### 1.1 Login with Password
- **Endpoint**: `GET /api/auth/login/password`
- **Description**: Authenticates a user with email and password
- **Authentication**: Basic authentication
- **Response**:
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "organizations": [
      {
        "organizationId": "org-123",
        "role": "MEMBER",
        "status": "ACTIVE"
      }
    ]
  }
}
```

### 1.2 Signup with Password
- **Endpoint**: `POST /api/auth/signup/password`
- **Description**: Registers a new user with email and password
- **Request**:
```json
{
  "email": "newuser@example.com",
  "password": "securepassword123"
}
```
- **Response**: `204 No Content`

### 1.3 Resend Verification Email
- **Endpoint**: `GET /api/auth/signup/resend-verification-email`
- **Description**: Resends verification email to the user
- **Headers**: `id-token: <token>`
- **Response**: `204 No Content`

## 2. Chat Endpoints

### 2.1 Chat
- **Endpoint**: `POST /api/:organizationId/chat`
- **Description**: Sends a chat message and gets a response
- **Authentication**: Required
- **Request**:
```json
{
  "userRequest": "Tell me about machine learning",
  "interactionType": "CHATMODEL",
  "provider": "ANTHROPIC",
  "modelName": "CLAUDE_3_OPUS"
}
```
- **Response**:
```json
{
  "answer": "Machine learning is a subset of artificial intelligence that focuses on developing systems that can learn from and make decisions based on data..."
}
```

### 2.2 Chat with Agent Stream
- **Endpoint**: `POST /api/:organizationId/chat/with-agent/stream`
- **Description**: Streams a chat response from an agent
- **Authentication**: Required
- **Request**:
```json
{
  "userRequest": "Analyze this data",
  "interactionType": "AGENT",
  "provider": "ANTHROPIC",
  "messageType": "USER",
  "conversationId": "conv-123",
  "userTimezone": "UTC",
  "useKnowledgeBase": true,
  "agentId": "agent-123"
}
```
- **Response**: Server-sent events stream with tokens

### 2.3 Save Message
- **Endpoint**: `POST /api/:organizationId/chat/conversations/:conversationId`
- **Description**: Saves a message to a conversation
- **Authentication**: Required
- **Request**:
```json
{
  "displayContents": ["Hello, how can I help you?"],
  "messageType": "ASSISTANT",
  "content": "Hello, how can I help you?",
  "interactionType": "CHATMODEL",
  "model": "CLAUDE_3_OPUS"
}
```
- **Response**: Message object

### 2.4 Get Messages by Conversation ID
- **Endpoint**: `GET /api/:organizationId/chat/conversations/:conversationId`
- **Description**: Gets all messages in a conversation
- **Authentication**: Required
- **Response**:
```json
[
  {
    "id": "msg-123",
    "conversationId": "conv-123",
    "displayContents": ["Hello, how can I help you?"],
    "messageType": "ASSISTANT",
    "interactionType": "CHATMODEL",
    "model": "CLAUDE_3_OPUS",
    "agent": null,
    "createdAt": "2023-06-15T10:30:00Z",
    "searchSources": null
  }
]
```

## 3. Conversation Endpoints

### 3.1 Create Conversation
- **Endpoint**: `POST /api/:organizationId/conversations`
- **Description**: Creates a new conversation
- **Authentication**: Required
- **Request**:
```json
{
  "title": "New Conversation",
  "interactionType": "CHATMODEL",
  "useKnowledgeBase": false,
  "conversationFolderId": "folder-123",
  "model": "CLAUDE_3_OPUS",
  "isWebSearchEnabled": true,
  "isDeepResearchEnabled": false
}
```
- **Response**: Conversation object

### 3.2 Get Conversations
- **Endpoint**: `GET /api/:organizationId/conversations`
- **Description**: Gets all conversations for the user
- **Authentication**: Required
- **Query Parameters**: `sort=DESC` (optional)
- **Response**:
```json
[
  {
    "id": "conv-123",
    "title": "Machine Learning Discussion",
    "createdAt": "2023-06-15T10:00:00Z",
    "conversationFolderId": "folder-123",
    "lastMessageCreatedAt": "2023-06-15T10:30:00Z"
  }
]
```

### 3.3 Update Conversation Title
- **Endpoint**: `PATCH /api/:organizationId/conversations/:id/title`
- **Description**: Updates the title of a conversation
- **Authentication**: Required
- **Request**:
```json
{
  "title": "Updated Conversation Title"
}
```
- **Response**: `204 No Content`

### 3.4 Update Current Model
- **Endpoint**: `PATCH /api/:organizationId/conversations/:id/current-model`
- **Description**: Updates the current model of a conversation
- **Authentication**: Required
- **Request**:
```json
{
  "interactionType": "CHATMODEL",
  "model": "CLAUDE_3_SONNET"
}
```
- **Response**: Updated Conversation object

## 4. Agent Endpoints

### 4.1 Create Agent
- **Endpoint**: `POST /api/:organizationId/agents`
- **Description**: Creates a new agent
- **Authentication**: Required
- **Request**:
```json
{
  "name": "Data Analysis Agent",
  "description": "An agent that helps with data analysis",
  "instructions": "You are a data analysis expert...",
  "model": "CLAUDE_3_OPUS",
  "capabilities": ["WEB_SEARCH", "CODE_INTERPRETER"],
  "files": [
    {
      "id": "file-123",
      "context": "This file contains data analysis methods"
    }
  ],
  "webPages": [
    {
      "id": "webpage-123",
      "context": "This webpage contains data visualization techniques"
    }
  ],
  "profileImageId": "image-123"
}
```
- **Response**: Agent ID (string)

### 4.2 Update Agent
- **Endpoint**: `PUT /api/:organizationId/agents`
- **Description**: Updates an existing agent
- **Authentication**: Required
- **Request**:
```json
{
  "id": "agent-123",
  "name": "Updated Data Analysis Agent",
  "description": "An updated agent that helps with data analysis",
  "instructions": "You are a data analysis expert...",
  "model": "CLAUDE_3_OPUS",
  "capabilities": ["WEB_SEARCH", "CODE_INTERPRETER"],
  "files": [
    {
      "id": "file-123",
      "context": "This file contains data analysis methods"
    }
  ],
  "webPages": [
    {
      "id": "webpage-123",
      "context": "This webpage contains data visualization techniques"
    }
  ],
  "profileImageId": "image-123"
}
```
- **Response**: Agent ID (string)

### 4.3 Get Agent
- **Endpoint**: `GET /api/:organizationId/agents/:agentId`
- **Description**: Gets an agent by ID
- **Authentication**: Required
- **Response**:
```json
{
  "id": "agent-123",
  "name": "Data Analysis Agent",
  "description": "An agent that helps with data analysis",
  "instructions": "You are a data analysis expert...",
  "model": "CLAUDE_3_OPUS",
  "capabilities": ["WEB_SEARCH", "CODE_INTERPRETER"],
  "createdBy": "John Doe",
  "createdByUserId": "user-123",
  "files": [
    {
      "id": "file-123",
      "name": "data_analysis.pdf",
      "context": "This file contains data analysis methods"
    }
  ],
  "webPages": [
    {
      "id": "webpage-123",
      "url": "https://example.com/data-viz",
      "context": "This webpage contains data visualization techniques"
    }
  ],
  "profileImageId": "image-123"
}
```

## 5. Smart Tasks Endpoints

### 5.1 Get Smart Task
- **Endpoint**: `GET /api/:organizationId/smart-tasks/id`
- **Description**: Gets a smart task by ID
- **Authentication**: Required
- **Query Parameters**: `id=task-123&userTimezone=UTC`
- **Response**:
```json
{
  "id": "task-123",
  "name": "Data Analysis Task",
  "tags": ["data", "analysis"],
  "categoryId": 1,
  "category": "Data Science",
  "optimalModel": "CLAUDE_3_OPUS",
  "agent": {
    "id": "agent-123",
    "name": "Data Analysis Agent"
  },
  "interactionType": "AGENT",
  "useCase": "Analyze data sets",
  "mandatoryPersonalizationOptions": ["dataset"],
  "optionalPersonalizationOptions": ["format"],
  "overview": "This task helps analyze data sets",
  "additionalRequests": ["Provide data in CSV format"],
  "sampleResult": "Sample analysis result...",
  "createdBy": "user-123",
  "published": true,
  "latest": true,
  "version": 1,
  "prompt": "Analyze the following data..."
}
```

### 5.2 Generate Manual Smart Task Sample Result
- **Endpoint**: `POST /api/:organizationId/manual-smart-task/generate-sample-result`
- **Description**: Generates a sample result for a manual smart task
- **Authentication**: Required
- **Request**:
```json
{
  "prompt": "Analyze this data set",
  "name": "Data Analysis",
  "interactionType": "CHATMODEL",
  "model": "CLAUDE_3_OPUS"
}
```
- **Response**: Server-sent events stream with tokens

## 6. Organization Endpoints

### 6.1 Get Organization
- **Endpoint**: `GET /api/organization/get/:organizationId`
- **Description**: Gets organization details
- **Authentication**: Required
- **Response**:
```json
{
  "id": "org-123",
  "name": "Example Organization",
  "status": "ACTIVE",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z"
}
```

### 6.2 Get Organization Name
- **Endpoint**: `GET /api/organization/name/:organizationId`
- **Description**: Gets only the organization name
- **Authentication**: Required
- **Response**:
```json
{
  "name": "Example Organization"
}
```

## 7. Deep Research Endpoints

### 7.1 Deep Research Stream
- **Endpoint**: `POST /api/:organizationId/deep-research/stream`
- **Description**: Streams deep research results
- **Authentication**: Required
- **Request**:
```json
{
  "query": "What are the latest advancements in quantum computing?"
}
```
- **Response**: Server-sent events stream with research progress

### 7.2 Save Deep Research Steps
- **Endpoint**: `POST /api/:organizationId/deep-research/save`
- **Description**: Saves deep research steps
- **Authentication**: Required
- **Request**:
```json
{
  "messageId": "msg-123",
  "steps": [
    {
      "title": "Initial Research",
      "content": "Quantum computing uses quantum bits...",
      "sources": ["https://example.com/quantum"]
    }
  ]
}
```
- **Response**: `204 No Content`

## 8. Knowledge Base Integration Endpoints

### 8.1 Get Knowledge Base Files
- **Endpoint**: `POST /api/:organizationId/knowledge-base-integrations/:externalknowledgesource/files`
- **Description**: Gets files from an external knowledge source
- **Authentication**: Required
- **Request**:
```json
{
  "email": "user@example.com",
  "folderId": "folder-123",
  "siteId": "site-123",
  "driveId": "drive-123"
}
```
- **Response**:
```json
[
  {
    "id": "file-123",
    "name": "document.pdf",
    "type": "PDF",
    "size": 1024,
    "lastModified": "2023-06-15T10:00:00Z",
    "url": "https://example.com/files/document.pdf"
  }
]
```

### 8.2 Get Integrations Token
- **Endpoint**: `GET /api/:organizationId/knowledge-base-integrations/token`
- **Description**: Gets authentication token for knowledge base integrations
- **Authentication**: Required
- **Response**:
```json
{
  "authToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 9. Flow Endpoints

### 9.1 Get Flow
- **Endpoint**: `GET /api/:organizationId/flows/:flowId`
- **Description**: Gets a flow by ID
- **Authentication**: Required
- **Response**:
```json
{
  "id": "flow-123",
  "flowName": "Data Processing Flow",
  "flowSchema": {
    "nodes": [],
    "edges": [],
    "trigger": {
      "type": "WEBHOOK",
      "id": "trigger-123"
    }
  },
  "createdBy": "user-123",
  "actionsLogoList": ["https://example.com/logo1.png"],
  "isFlowTriggerActive": true
}
```

### 9.2 Save Flow
- **Endpoint**: `POST /api/:organizationId/flows`
- **Description**: Saves a flow
- **Authentication**: Required
- **Request**:
```json
{
  "flowName": "Data Processing Flow",
  "flowSchema": {
    "nodes": [],
    "edges": [],
    "trigger": {
      "type": "WEBHOOK",
      "id": "trigger-123"
    }
  }
}
```
- **Response**: Flow ID (string)

## 10. Document Endpoints

### 10.1 Get Files Count By Knowledge Base Source
- **Endpoint**: `GET /api/:organizationId/documents/count`
- **Description**: Gets the count of files by knowledge base source
- **Authentication**: Required
- **Response**:
```json
{
  "ONEDRIVE": 5,
  "SHAREPOINT": 3,
  "GOOGLE_DRIVE": 2,
  "UPLOAD": 10
}
```

### 10.2 Get Uploaded Document
- **Endpoint**: `GET /api/:organizationId/documents/:id`
- **Description**: Gets an uploaded document by ID
- **Authentication**: Required
- **Response**:
```json
{
  "id": "doc-123",
  "name": "document.pdf",
  "status": "COMPLETED",
  "createdAt": "2023-06-15T10:00:00Z",
  "knowledgeSource": "UPLOAD",
  "documentUrl": "https://example.com/documents/document.pdf"
}
```
