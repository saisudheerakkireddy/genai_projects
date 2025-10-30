# Arovia Test Suite

Comprehensive testing framework for the Arovia AI Health Desk Agent.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                # Pytest configuration and shared fixtures
├── test_triage_agent.py       # Core triage agent functionality
├── test_emergency_detection.py # Emergency detection system
├── test_voice_input.py        # Voice input and transcription
├── test_medical_analysis.py   # Medical analysis and triage logic
└── README.md                  # This file
```

## Running Tests

### Prerequisites
1. Set up your Groq API key in `.env` file:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

2. Install test dependencies:
   ```bash
   pip install pytest pytest-cov
   ```

### Running All Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=agents --cov=utils --cov=models

# Run with verbose output
pytest tests/ -v
```

### Running Specific Test Files
```bash
# Test triage agent
pytest tests/test_triage_agent.py

# Test emergency detection
pytest tests/test_emergency_detection.py

# Test voice input
pytest tests/test_voice_input.py

# Test medical analysis
pytest tests/test_medical_analysis.py
```

### Running Specific Test Classes
```bash
# Test only emergency detection
pytest tests/test_emergency_detection.py::TestEmergencyDetection

# Test only cardiac emergencies
pytest tests/test_emergency_detection.py::TestEmergencyDetection::test_cardiac_emergency
```

## Test Categories

### 1. Core Functionality Tests (`test_triage_agent.py`)
- Agent initialization
- Emergency case detection
- Standard case assessment
- Multilingual support
- Model information retrieval

### 2. Emergency Detection Tests (`test_emergency_detection.py`)
- Cardiac emergencies
- Neurological emergencies
- Respiratory emergencies
- Trauma emergencies
- Mental health emergencies
- Non-emergency case validation

### 3. Voice Input Tests (`test_voice_input.py`)
- Supported languages validation
- Language code verification
- Whisper client initialization
- Model information
- Voice recording (manual tests)

### 4. Medical Analysis Tests (`test_medical_analysis.py`)
- Urgency scoring system
- Symptom extraction
- Red flag detection
- Specialty recommendations
- Triage categorization
- Action recommendations
- Multilingual medical analysis

## Test Data

### Emergency Test Cases
- "I have severe chest pain for 30 minutes, radiating to my left arm"
- "I think I'm having a stroke, my face is drooping"
- "I can't breathe and my lips are turning blue"
- "Severe bleeding from a deep cut"
- "I want to kill myself"

### Urgent Test Cases
- "High fever for 3 days with severe headache"
- "Severe abdominal pain for 2 hours"
- "Difficulty breathing with chest tightness"
- "Persistent vomiting for 6 hours"

### Standard Test Cases
- "Mild headache since this morning"
- "Small cut on my finger"
- "Slight cough and runny nose"
- "Mild stomach ache"

### Multilingual Test Cases
- Hindi: "मुझे तेज सिरदर्द है और बुखार भी है"
- Bengali: "আমার বুকে ব্যথা হচ্ছে"
- Telugu: "నాకు తీవ్రమైన ఛాతీ నొప్పి ఉంది"
- Tamil: "எனக்கு கடுமையான தலைவலி உள்ளது"
- Gujarati: "મને છાતીમાં દુખાવો છે"

## Manual Tests

Some tests require manual execution due to audio recording requirements:

```python
# Voice recording tests (manual)
pytest tests/test_voice_input.py::TestVoiceInput::test_voice_recording -s
pytest tests/test_voice_input.py::TestVoiceInput::test_voice_to_triage_pipeline -s
```

## Continuous Integration

The test suite is designed to work with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    pip install -r requirements.txt
    pytest tests/ --cov=agents --cov=utils --cov=models --cov-report=xml
```

## Contributing Tests

When adding new test cases:

1. Follow the existing naming conventions
2. Use descriptive test names
3. Include both positive and negative test cases
4. Add multilingual test cases where applicable
5. Update this README with new test categories

## Test Coverage

Target coverage areas:
- Core triage logic: 90%+
- Emergency detection: 95%+
- Voice input: 80%+ (excluding manual tests)
- Medical analysis: 85%+

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```
   GROQ_API_KEY not found in environment variables
   ```
   Solution: Set up your `.env` file with the correct API key.

2. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'agents'
   ```
   Solution: Run tests from the project root directory.

3. **Audio Recording Issues**
   ```
   Error recording audio: [Errno -9996] Invalid input device
   ```
   Solution: Check microphone permissions and audio device availability.

### Debug Mode

Run tests with debug output:
```bash
pytest tests/ -v -s --tb=long
```

## Performance Testing

For performance testing, use:
```bash
pytest tests/ --durations=10
```

This will show the 10 slowest tests, helping identify performance bottlenecks.
