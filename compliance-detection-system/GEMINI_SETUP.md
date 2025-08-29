# 🔑 Google AI Studio API Key Setup

This guide shows how to set up a Google AI Studio API key for Gemini integration in the CDS system.

## Quick Setup (Recommended)

### 1. Get Your API Key
- Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
- Click **"Create API Key"**
- Copy the generated API key (starts with `AIzaSy`)

### 2. Add to Environment
Edit your `.env` file and add:
```bash
GOOGLE_API_KEY=AIzaSyD...your-actual-key-here
```

### 3. Test Setup
```bash
python test_gemini_api.py
```

You should see: `✅ Google AI Studio API key is working!`

## Alternative: Google Cloud Vertex AI

If you prefer using Google Cloud Vertex AI instead:

```bash
# In .env file
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

## Configuration Options

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `GOOGLE_API_KEY` | Google AI Studio API key | None |
| `GEMINI_API_KEY` | Alternative name for API key | None |
| `GEMINI_MODEL` | Model to use | `gemini-1.5-pro` |
| `GEMINI_TEMPERATURE` | Response creativity (0.0-1.0) | `0.2` |
| `GEMINI_MAX_TOKENS` | Maximum response length | `2048` |

## Usage in CDS

Once configured, Gemini will be used automatically in:
- `cds explain` - Generate compliance explanations
- `cds pipeline` - LLM analysis in full pipeline
- Any compliance analysis requiring reasoning

## Troubleshooting

### ❌ "API key not found"
- Make sure `.env` file exists in the project root
- Check that `GOOGLE_API_KEY` is set correctly
- Run `python test_gemini_api.py` to verify

### ❌ "API key invalid"
- Verify the key starts with `AIzaSy`
- Check for extra spaces or characters
- Generate a new key if needed

### ❌ "Quota exceeded"
- Check your usage at [Google AI Studio](https://makersuite.google.com)
- Consider upgrading your plan
- Vertex AI has higher quotas but more complex setup

## Security Notes

⚠️ **Never commit your API key to version control!**

- Keep `.env` in `.gitignore`
- Use environment variables in production
- Rotate keys regularly
- Monitor usage for unexpected activity
