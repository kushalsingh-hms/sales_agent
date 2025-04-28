# Vapi Sales Agent

A Python-based sales calling agent using the Vapi platform for making outbound sales calls.

## Setup

1. Activate the virtual environment:
```bash
workon multiagent
```

or create virtualenv for first instance
```bash
mkvirtualenv multiagent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Vapi API key:
```
VAPI_API_KEY=your_api_key_here
```

## Configuration

### Phone Number Setup
1. The phone number must be in E.164 format (international format)
2. Format: `+[country code][phone number]`
3. Examples:
   - US: `+14155552671`
   - UK: `+442071234567`
   - India: `+919876543210`

### Assistant ID Setup
1. Go to [Vapi Dashboard](https://dashboard.vapi.ai/)
2. Click on "Assistants" in the sidebar
3. Click "Create New Assistant"
4. Configure your assistant:
   - Name: "Sales Agent"
   - Voice: Select preferred voice
   - Language: Select preferred language
   - Conversation Settings: Configure for sales calls
5. After creation, copy the Assistant ID from the dashboard

### Update Configuration
1. Open `sales_agent.py`
2. Update these values in the `main()` function:
```python
phone_number = "+14155552671"  # Replace with your target phone number
assistant_id = "your_assistant_id"  # Replace with your Vapi assistant ID
```

## Usage

Run the sales agent:
```bash
python sales_agent.py
```

The agent will:
- Validate the phone number format
- Make an outbound call to the specified number
- Use your configured Vapi assistant for the conversation
- Print call events and status updates in real-time
- Handle any errors that occur during the call

## Features

- Outbound sales call initiation
- Phone number format validation
- Real-time call event monitoring
- Error handling and logging
- Configurable through environment variables 