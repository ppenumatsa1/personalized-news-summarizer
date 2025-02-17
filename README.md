# Personalized News Summarizer

## Overview
The Personalized News Summarizer is a web application that allows users to input URLs of news articles, which are then scraped for content, summarized using Azure OpenAI, and classified into categories. The application provides APIs for retrieving summaries based on categories and managing articles.

## Project Structure
```
personalized-news-summarizer
├── .github
│   └── workflows
├── backend
│   └── app
│       ├── core
│       ├── db
│       ├── models
│       ├── routers
│       ├── schemas
│       ├── services
│       ├── exceptions
│       ├── logs
│       └── main.py
├── frontend
│   ├── public
│   └── src
│       ├── components
│       └── services
├── infra
│   ├── bicep
│   └── kubernetes
├── scripts
│   ├── db
│   └── other_scripts
├── docs
├── README.md
├── requirements.txt
└── .gitignore
```

## Environment Setup
1. Copy the `.env.example` file to create a new `.env` file in the backend directory:
    ```sh
    cd backend
    cp .env.example .env
    ```

2. Update the `.env` file with your specific configuration:
    ```
    # Database Configuration
    DATABASE_URL=postgresql://user:password@host:5432/database
    TEST_DATABASE_URL=postgresql://user:password@host:5432/test_database

    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY=your_key
    AZURE_OPENAI_ENDPOINT=your_endpoint
    AZURE_OPENAI_MODEL=gpt-4
    AZURE_OPENAI_API_VERSION=2023-05-15

    # Application Settings
    SUMMARY_LENGTH=250
    DEFAULT_CATEGORY=general
    APP_NAME=Personalized News Summarizer
    APP_VERSION=1.0.0
    APP_PREFIX=/api/v1
    ```

3. Install Python dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Install frontend dependencies:
    ```sh
    cd frontend
    npm install
    ```

## Azure OpenAI Configuration
1. Create an Azure OpenAI resource in your Azure portal
2. Deploy GPT-4 or GPT-3.5-turbo model
3. Note down the endpoint and API key
4. Update the `.env` file with these credentials

## API Documentation
### Articles
- `POST /api/articles`: Submit a new article for summarization
- `GET /api/articles`: Retrieve all articles
- `GET /api/articles/{category}`: Get articles by category
- `DELETE /api/articles/{id}`: Delete an article


## Backend
The backend is built using FastAPI and interacts with a PostgreSQL database. It includes:
- **Core**: Configuration and dependency management.
- **DB**: Database interactions and models.
- **Routers**: API endpoints for managing articles and summaries.
- **Schemas**: Data validation using Pydantic.
- **Services**: Business logic for summarization and classification.
- **Exceptions**: Custom error handling.
- **Logs**: Logging setup for monitoring.

## Frontend
The frontend is developed using React and consists of:
- **Public**: Static assets like images and HTML files.
- **Src**: React components and services for API interaction.

## Infrastructure
Infrastructure as code is managed using:
- **Bicep**: Templates for Azure deployment.
- **Kubernetes**: Configuration for container orchestration.

## Database Initialization
The database is initialized using SQL commands defined in `scripts/db/init.sql`.

### Steps to Initialize the Database
1. Log in to PostgreSQL as a user:
    ```sh
    psql -h your_host -p 5432 -U your_username
    ```

2. Run the provided SQL script to create the summaries database and all necessary objects:
    ```sh
    \i scripts/db/init_schema.sql
    ```

## Documentation
Documentation for setup, usage, and API endpoints can be found in the `docs` folder.

## Setup Instructions

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will open in your default browser at http://localhost:3000

### Backend Setup (Coming Soon)
Backend setup instructions will be added once the backend is implemented.

## Usage
- Use the API to submit article URLs for summarization.
- Retrieve summaries and articles based on categories.
- Manage articles through the provided endpoints.

## License
This project is licensed under the MIT License.