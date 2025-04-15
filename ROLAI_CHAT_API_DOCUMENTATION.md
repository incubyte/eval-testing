# Chat and Conversation API Documentation

## Base URL

All endpoints are prefixed with `/:organizationId` where `organizationId` is the ID of the organization.

## Authentication

All endpoints require authentication. Include the Bearer token in the Authorization header.

## Valid Values

### Chat Models

Valid values for `modelName`:

- `gpt-3.5-turbo`
- `gpt-4`
- `gpt-4-turbo`
- `gpt-4o`
- `gemini-1.5-pro`
- `gemma2-9b-it`
- `llama3-70b-8192`
- `llama3-8b-8192`
- `mixtral-8x7b-32768`
- `gpt-4o-mini`
- `claude-3-5-sonnet-20240620`
- `o1`
- `o1-mini`
- `o3-mini`
- `gemini-2.0-flash`
- `gemini-2.0-flash-thinking`
- `gemini-2.0-pro`
- `gemini-2.5-pro`
- `claude-3-5-sonnet`
- `claude-3-5-haiku`
- `claude-3-7-sonnet`
- `pixtral-large`
- `mistral-small`
- `llama-3.3-70b-versatile`
- `sonar-pro`
- `sonar`
- `deepseek-r1`

### Chat Providers

Valid values for `provider`:

- `openai`
- `googleai`
- `groqai`
- `anthropic`
- `perplexity`
- `mistral`
- `deepseek`

### Message Types

Valid values for `messageType`:

- `USER`
- `ASSISTANT`
- `MODEL_CHANGE_NOTIFICATION`
- `SMART_TASK_SELECTED`
- `CHAINED_SMART_TASKS_SELECTED`
- `KNOWLEDGE_BASE_NOTIFICATION`
- `USER_DOCUMENT`
- `FLOW_RUN_INPUT`
- `FLOW_RUN_OUTPUT`
- `DEEP_RESEARCH`
- `WEB_SEARCH_ENABLED_NOTIFICATION`
- `WEB_SEARCH_DISABLED_NOTIFICATION`
- `DEEP_RESEARCH_NOTIFICATION`

### Interaction Types

Valid values for `interactionType`:

- `CHATMODEL`
- `AGENT`

## Chat Endpoints

### 1. Send Chat Message

- **Endpoint**: `POST /:organizationId/chat`
- **Description**: Send a chat message and get a response
- **Request Body**:
  ```json
  {
    "userRequest": "What is the capital of France?",
    "interactionType": "CHATMODEL",
    "provider": "openai",
    "modelName": "gpt-4"
  }
  ```
- **Response**:
  ```json
  {
    "id": "msg_123",
    "content": "The capital of France is Paris.",
    "createdAt": "2024-03-20T10:30:00Z"
  }
  ```
- **Error**: Returns 400 Bad Request if request body is missing or invalid

### 2. Stream Chat Message

- **Endpoint**: `POST /:organizationId/chat/stream`
- **Description**: Stream chat messages (Server-Sent Events)
- **Request Body**:
  ```json
  {
    "userRequest": "Explain quantum computing",
    "interactionType": "CHATMODEL",
    "provider": "openai",
    "messageType": "USER",
    "conversationId": "conv_123",
    "userTimezone": "America/New_York",
    "useKnowledgeBase": true,
    "modelName": "gpt-4"
  }
  ```
- **Response**: Server-Sent Events stream with chunks:
  ```json
  {
    "token": "Quantum",
    "isLastToken": false
  }
  ```
- **Error**: Returns 400 Bad Request if request body is missing or invalid

### 3. Save Message to Conversation

- **Endpoint**: `POST /:organizationId/chat/conversations/:conversationId`
- **Description**: Save a message to a specific conversation
- **Parameters**:
  - `conversationId`: ID of the conversation
- **Request Body**:
  ```json
  {
    "displayContents": ["Hello, how can I help you?"],
    "messageType": "ASSISTANT",
    "interactionType": "CHATMODEL",
    "model": "gpt-4"
  }
  ```
- **Response**:
  ```json
  {
    "id": "msg_456",
    "conversationId": "conv_123",
    "displayContents": ["Hello, how can I help you?"],
    "messageType": "ASSISTANT",
    "interactionType": "CHATMODEL",
    "model": "gpt-4",
    "createdAt": "2024-03-20T10:35:00Z"
  }
  ```
- **Error**: Returns 400 Bad Request if request body is missing or invalid

### 4. Get Messages by Conversation

- **Endpoint**: `GET /:organizationId/chat/conversations/:conversationId`
- **Description**: Retrieve all messages from a specific conversation
- **Parameters**:
  - `conversationId`: ID of the conversation
- **Response**:
  ```json
  [
    {
      "id": "msg_123",
      "conversationId": "conv_123",
      "displayContents": ["Hello, how can I help you?"],
      "messageType": "ASSISTANT",
      "interactionType": "CHATMODEL",
      "model": "gpt-4",
      "createdAt": "2024-03-20T10:35:00Z"
    },
    {
      "id": "msg_124",
      "conversationId": "conv_123",
      "displayContents": ["What is the capital of France?"],
      "messageType": "USER",
      "createdAt": "2024-03-20T10:36:00Z"
    }
  ]
  ```
- **Error**: Returns 404 Not Found if conversation doesn't exist

### 5. Chat with Document

- **Endpoint**: `POST /:organizationId/chat/with-doc/stream`
- **Description**: Stream chat messages with document context (Server-Sent Events)
- **Request Body**: Same as Stream Chat Message endpoint
- **Response**: Same as Stream Chat Message endpoint

### 6. Chat with Agent

- **Endpoint**: `POST /:organizationId/chat/with-agent/stream`
- **Description**: Stream chat messages with agent context (Server-Sent Events)
- **Request Body**: Same as Stream Chat Message endpoint
- **Response**: Same as Stream Chat Message endpoint

## Conversation Endpoints

### 1. Create Conversation

- **Endpoint**: `POST /:organizationId/conversations`
- **Description**: Create a new conversation
- **Request Body**:
  ```json
  {
    "title": "General Discussion",
    "interactionType": "CHATMODEL",
    "useKnowledgeBase": true,
    "model": "gpt-4",
    "isWebSearchEnabled": true,
    "isDeepResearchEnabled": false
  }
  ```
- **Response**:
  ```json
  {
    "id": "conv_123",
    "title": "General Discussion",
    "interactionType": "CHATMODEL",
    "useKnowledgeBase": true,
    "model": "gpt-4",
    "isWebSearchEnabled": true,
    "isDeepResearchEnabled": false,
    "createdAt": "2024-03-20T10:30:00Z",
    "updatedAt": "2024-03-20T10:30:00Z"
  }
  ```

### 2. Get All Conversations

- **Endpoint**: `GET /:organizationId/conversations`
- **Description**: Retrieve all conversations for the authenticated user
- **Query Parameters**:
  - `sort`: Sort order (default: DESC)
- **Response**:
  ```json
  [
    {
      "id": "conv_123",
      "title": "General Discussion",
      "interactionType": "CHATMODEL",
      "useKnowledgeBase": true,
      "model": "gpt-4",
      "isWebSearchEnabled": true,
      "isDeepResearchEnabled": false,
      "createdAt": "2024-03-20T10:30:00Z",
      "updatedAt": "2024-03-20T10:30:00Z"
    }
  ]
  ```

### 3. Get Single Conversation

- **Endpoint**: `GET /:organizationId/conversations/:id`
- **Description**: Retrieve a specific conversation
- **Parameters**:
  - `id`: Conversation ID
- **Response**:
  ```json
  {
    "id": "conv_123",
    "title": "General Discussion",
    "interactionType": "CHATMODEL",
    "useKnowledgeBase": true,
    "model": "gpt-4",
    "isWebSearchEnabled": true,
    "isDeepResearchEnabled": false,
    "createdAt": "2024-03-20T10:30:00Z",
    "updatedAt": "2024-03-20T10:30:00Z"
  }
  ```

### 4. Delete Conversation

- **Endpoint**: `DELETE /:organizationId/conversations/:id`
- **Description**: Delete a specific conversation
- **Parameters**:
  - `id`: Conversation ID
- **Response**: 204 No Content

### 5. Update Conversation Title

- **Endpoint**: `PATCH /:organizationId/conversations/:id/title`
- **Description**: Update the title of a conversation
- **Parameters**:
  - `id`: Conversation ID
- **Request Body**:
  ```json
  {
    "title": "Updated Discussion"
  }
  ```
- **Response**: 204 No Content

### 6. Update Conversation Model

- **Endpoint**: `PATCH /:organizationId/conversations/:id/current-model`
- **Description**: Update the current model used in a conversation
- **Parameters**:
  - `id`: Conversation ID
- **Request Body**:
  ```json
  {
    "interactionType": "CHATMODEL",
    "model": "gpt-4-turbo"
  }
  ```
- **Response**:
  ```json
  {
    "id": "conv_123",
    "title": "General Discussion",
    "interactionType": "CHATMODEL",
    "useKnowledgeBase": true,
    "model": "gpt-4-turbo",
    "isWebSearchEnabled": true,
    "isDeepResearchEnabled": false,
    "createdAt": "2024-03-20T10:30:00Z",
    "updatedAt": "2024-03-20T10:40:00Z"
  }
  ```

### 7. Modify Web Search Status

- **Endpoint**: `PATCH /:organizationId/conversations/:id/web-search`
- **Description**: Enable/disable web search for a conversation
- **Parameters**:
  - `id`: Conversation ID
- **Request Body**:
  ```json
  {
    "isWebSearchEnabled": false
  }
  ```
- **Response**:
  ```json
  {
    "id": "conv_123",
    "title": "General Discussion",
    "interactionType": "CHATMODEL",
    "useKnowledgeBase": true,
    "model": "gpt-4-turbo",
    "isWebSearchEnabled": false,
    "isDeepResearchEnabled": false,
    "createdAt": "2024-03-20T10:30:00Z",
    "updatedAt": "2024-03-20T10:45:00Z"
  }
  ```

### 8. Modify Deep Research Status

- **Endpoint**: `PATCH /:organizationId/conversations/:id/deep-research`
- **Description**: Enable/disable deep research for a conversation
- **Parameters**:
  - `id`: Conversation ID
- **Request Body**:
  ```json
  {
    "isDeepResearchEnabled": true
  }
  ```
- **Response**:
  ```json
  {
    "id": "conv_123",
    "title": "General Discussion",
    "interactionType": "CHATMODEL",
    "useKnowledgeBase": true,
    "model": "gpt-4-turbo",
    "isWebSearchEnabled": false,
    "isDeepResearchEnabled": true,
    "createdAt": "2024-03-20T10:30:00Z",
    "updatedAt": "2024-03-20T10:50:00Z"
  }
  ```

### 9. Use Knowledge Base

- **Endpoint**: `POST /:organizationId/conversations/:id/use-kb`
- **Description**: Enable/disable knowledge base usage for a conversation
- **Parameters**:
  - `id`: Conversation ID
- **Request Body**:
  ```json
  {
    "useKnowledgeBase": false
  }
  ```
- **Response**: 204 No Content

### 10. Attach Documents

- **Endpoint**: `POST /:organizationId/conversations/:id/attach-documents`
- **Description**: Attach documents to a conversation
- **Parameters**:
  - `id`: Conversation ID
- **Request Body**:
  ```json
  {
    "documentIds": ["doc_123", "doc_456"]
  }
  ```
- **Response**: 204 No Content

## Shared Conversations

### 1. Get Shared Conversation

- **Endpoint**: `GET /shared-conversations/:id`
- **Description**: Retrieve a shared conversation
- **Parameters**:
  - `id`: Shared conversation ID
- **Response**:
  ```json
  {
    "id": "shared_123",
    "conversationId": "conv_123",
    "sharedWith": ["user_456", "user_789"],
    "createdBy": "user_123",
    "createdAt": "2024-03-20T10:30:00Z"
  }
  ```

### 2. Create Shared Conversation

- **Endpoint**: `POST /:organizationId/shared-conversations`
- **Description**: Create a shared conversation
- **Request Body**:
  ```json
  {
    "conversationId": "conv_123",
    "sharedWith": ["user_456", "user_789"],
    "createdBy": "user_123"
  }
  ```
- **Response**: 204 No Content
