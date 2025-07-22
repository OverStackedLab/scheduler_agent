# Scheduler Agent

A scheduling agent application that helps manage and organize tasks and appointments using Google Calendar API and OpenAI.

## Description

This project is a FastAPI-based scheduling agent that assists in managing and organizing tasks and appointments. It provides an intelligent interface for scheduling and managing time-based activities through integration with Google Calendar and AI-powered assistance.

## Features

- Task scheduling and management
- Google Calendar integration
- AI-powered scheduling suggestions
- OAuth2 authentication for Google services
- RESTful API with FastAPI
- Interactive API documentation

## Getting Started

### Prerequisites

- Python 3.9 or higher
- uv (Python package installer)
- Google Cloud Console project with Calendar API enabled
- OpenAI API key

### Installation

1. Clone the repository:

```bash
git clone https://github.com/OverStackedLab/scheduler_agent.git
cd scheduler_agent
```

2. Install uv (if not already installed):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create and activate a virtual environment, then install dependencies:

```bash
uv venv
source .venv/bin/activate  # On macOS/Linux
uv pip install -e .
```

4. Set up environment variables:

```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:

- `OPENAI_API_KEY`: Your OpenAI API key
- `GOOGLE_CLIENT_ID`: Your Google OAuth2 client ID
- `GOOGLE_CLIENT_SECRET`: Your Google OAuth2 client secret
- `GOOGLE_API_KEY`: Your Google API key

5. Run the application:

```bash
fastapi dev main.py
```

The server will start at http://127.0.0.1:8000 with interactive documentation at http://127.0.0.1:8000/docs

### Google Cloud Setup

To use the Google Calendar integration, you'll need to set up a Google Cloud project:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API" and enable it
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Configure the OAuth consent screen if prompted
   - Set application type to "Web application"
   - Add authorized redirect URIs (e.g., `http://localhost:8000/auth/callback`)
5. Download the client configuration and update your `.env` file with the client ID and secret

### Usage

Once the server is running, you can:

1. Visit http://127.0.0.1:8000/docs to see the interactive API documentation
2. Authenticate with Google OAuth2 to access calendar features
3. Send messages to the agent endpoint to interact with the scheduling assistant

Example API request:

```bash
curl -X POST "http://127.0.0.1:8000/agent" \
  -H "Content-Type: application/json" \
  -d '{"message": "Schedule a meeting for tomorrow at 2 PM"}'
```

Traces: https://platform.openai.com/traces

## Development

### Running in Development Mode

For development with auto-reload:

```bash
fastapi dev main.py
```

### Project Structure

- `main.py` - FastAPI application entry point
- `agent.py` - Core agent logic and message processing
- `pyproject.toml` - Project dependencies and configuration
- `.env.example` - Template for environment variables

### Dependencies

Key dependencies include:

- FastAPI - Web framework
- Google API Client - Google Calendar integration
- OpenAI Agents - AI agent functionality
- Python-dotenv - Environment variable management

## Troubleshooting

### Common Issues

1. **Google API Authentication Errors**

   - Ensure your Google Cloud project has the Calendar API enabled
   - Check that your OAuth2 credentials are correctly configured
   - Verify the redirect URIs match your application settings

2. **OpenAI API Errors**

   - Confirm your OpenAI API key is valid and has sufficient credits
   - Check that the API key is correctly set in your `.env` file

3. **Module Import Errors**
   - Ensure you've activated the virtual environment
   - Run `uv pip install -e .` to install the project in development mode

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

[Add your contact information or preferred method of communication]
