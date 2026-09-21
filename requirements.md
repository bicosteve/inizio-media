# Revised assignment requirements

## Goal

Build a web app that accepts a keyword phrase, fetches the first page of Google search results using only organic results, extracts them into a structured machine-readable format (not HTML), and provides unit tests verifying the extraction/output correctness.

1. Web UI
   Create an HTML page with one input.
   When the user submits the input, the page must trigger a request to your backend to perform the search + extraction.
   The UI may either:
   - display the extracted results, and/or
   - download them as a file (optional).

2. Google fetching + organic-only extraction
   Implement functionality that, given a query, retrieves Google results corresponding to:
   - Page 1 (the first SERP),
   - Only organic results (explicitly exclude):
     ads (sponsored/paid),
     knowledge panels / featured blocks (if present in your chosen data source),
     “People also ask” blocks,
     any non-organic modules that are not standard organic blue-link results.
     Since unit tests must be deterministic, your extraction/parsing layer must be testable without relying on live Google in CI.
     Use fixtures (saved example responses) for unit tests, OR
     Use a search API provider that returns structured SERP data (preferred).
     Note: If your solution fetches live data, you must structure the code so that the parsing logic can be tested using fixed fixtures.

3. Output format (structured, machine-readable)
   The extracted output must be saved in a structured format that is not HTML.
   Your output must be JSON and must follow a documented schema.
   For each query, output JSON in this schema format:

   ```json
   {
     "query": "string",
     "engine": "google",
     "page": 1,
     "results": [
       {
         "position": 1,
         "title": "string",
         "url": "string",
         "snippet": "string|null"
       }
     ]
   }   }

   ```

Save the JSON to the project as a downloadable file or return it via an endpoint (either is acceptable), but the format must match the schema above.

1. Unit tests
   Cover your code with unit tests.
   Unit tests must at least verify correctness of the output, including:
   parsing/extraction correctness from fixtures (not live Google),
   filtering to organic-only,
   output schema validation (fields exist and types are correct),
   stable ordering (position starts at 1 and is sequential for the extracted organic items).
   Tests must pass and should be runnable via a single command.
