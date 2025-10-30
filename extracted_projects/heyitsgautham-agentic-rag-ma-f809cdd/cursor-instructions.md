# Cursor AI Instructions: M&A Due Diligence Agentic RAG Demo

## Project Overview
This is a Jupyter notebook demonstrating Agentic RAG for M&A Due Diligence analysis using Contextual AI's platform. The notebook includes:
- Document parsing and ingestion
- RAG agent creation with Grounded Language Model (GLM)
- Multi-document financial analysis
- Component demonstrations (Parser, Reranker, GLM, LMUnit)

## Critical Modification Required

### File Upload Cell Enhancement
**Location:** Step 3 - Document upload cell (search for `files_to_upload` variable)

**Current Behavior:**
- Downloads files from GitHub URLs directly
- No fallback mechanism if download fails

**Required Change:**
Modify the file upload cell to implement URL download with **automatic fallback to manual upload** if the URL fails.

### Implementation Requirements

1. **Try URL Download First**
   - Attempt to download from provided URL
   - Handle timeout errors (10 second timeout)
   - Handle HTTP errors (404, 500, etc.)
   - Handle network connection failures
   - Show clear status: "✓ Successfully downloaded" or "✗ Download failed"

2. **Fallback to Manual Upload**
   - If URL download fails for ANY reason, automatically trigger Google Colab file upload widget
   - Use `from google.colab import files` and `files.upload()`
   - Display clear prompt: "📁 Please upload {filename} manually:"
   - Move uploaded file to `data/` directory
   - Confirm successful manual upload

3. **Error Handling**
   - Wrap all download attempts in try-except blocks
   - Log specific error messages for debugging
   - Continue processing remaining files if one fails
   - Display final summary: "📊 Successfully processed X files"

4. **Preserve Existing Functionality**
   - Keep the datastore ingestion logic unchanged
   - Maintain the `document_ids` list tracking
   - Keep all print statements for progress tracking
   - Don't modify the Contextual AI API calls

### Files to Modify
- **Primary:** The cell containing `files_to_upload` list (currently around cell 15-20 in the notebook)
- **Variables to preserve:** `datastore_id`, `document_ids`, `files_to_upload`

### Testing Requirements
After implementation, verify:
1. Valid URL → Downloads successfully
2. Invalid URL → Triggers manual upload prompt
3. No URL provided → Triggers manual upload prompt
4. All files successfully ingest to Contextual AI datastore
5. `document_ids` list populated correctly

## Existing Architecture (Do Not Modify)

### Components Used
- **Parser:** Contextual AI's multi-modal document parser (VLM + OCR)
- **Reranker:** Instruction-following reranker v2
- **GLM:** Grounded Language Model v1 (prevents hallucinations)
- **LMUnit:** Natural language unit testing for evaluation
- **Datastore:** ElasticSearch vector database

### Current Document Types
- Financial statements (10-K, quarterly reports)
- Legal contracts (acquisition agreements)
- Market analysis reports (industry research)

### Agent Configuration
The agent uses:
- System prompt defining role and guidelines
- Suggested queries for common use cases
- ElasticSearch datastore for retrieval
- GLM for grounded generation

## M&A Use Case Context
The demo is being adapted for M&A Due Diligence presentations focusing on:
- Debt structure risk assessment
- Regulatory compliance analysis
- Competitive positioning evaluation
- Synergy realization probability
- Multi-document financial synthesis

## Constraints
1. **Single-file notebook:** All changes must be in-notebook cells
2. **Colab environment:** Must work in Google Colab
3. **No breaking changes:** Existing cells must continue to work
4. **Manual upload compatibility:** Must support Colab's file upload widget
5. **URL flexibility:** Should handle both valid URLs and placeholder text

## Code Style Guidelines
- Use clear variable names matching existing conventions
- Include informative print statements with emoji indicators (✓, ✗, 📁, 📊)
- Handle exceptions gracefully with specific error messages
- Maintain consistent indentation (4 spaces)
- Add comments for complex logic

## Implementation Notes
- The `requests` library is already imported in the notebook
- The `google.colab.files` module must be imported for manual upload
- File paths use `data/` directory convention
- Contextual AI client (`client`) is already initialized
- The `datastore_id` variable exists and is ready to use

## Success Criteria
✅ URL download works when valid URL provided
✅ Manual upload triggers automatically on URL failure
✅ Clear user prompts and status messages displayed
✅ All files successfully ingest to datastore
✅ No breaking changes to existing functionality
✅ Robust error handling for all edge cases

## Additional Context
This modification enables seamless demo experience during hackathon presentations where:
- GitHub URLs might be rate-limited
- Network connectivity might be unreliable
- Presenters want flexibility to use local files
- Audience members want to try with their own documents

---

**Task:** Implement the file upload fallback mechanism in the document upload cell while preserving all existing functionality and following the requirements above.