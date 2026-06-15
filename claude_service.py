import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
MODEL = 'claude-sonnet-4-6'

CODEBASE_PROMPT = """You are a technical documentation generator. Analyze the following codebase and generate comprehensive documentation in Markdown format.

File structure:
{file_tree}

File contents:
{content}

Generate the following sections:
1. Project Overview - what the project does, its purpose
2. Architecture - how the components fit together
3. File-by-File Breakdown - brief description of each significant file's role
4. Setup and Installation Instructions
5. Key Functions/Classes - document important functions/classes with purpose, parameters, return values
6. Suggested Inline Comments - for complex or non-obvious sections, suggest comments to add, referencing file and function name

Output only the Markdown documentation, no preamble."""

SCHEMATIC_PROMPT = """You are a technical documentation generator for electronics and circuit design. Analyze the circuit schematic in the image and generate structured documentation in Markdown format.

Generate the following sections:
1. Circuit Overview - what this circuit does and its purpose
2. Components List - identify each component, its type, and approximate value/rating if visible
3. Connections and Signal Flow - describe how components are connected and how signals/power flow through the circuit
4. Working Principle - explain the operation of the circuit
5. Possible Applications
6. Notes and Observations - potential issues, improvements, or missing labels

Output only the Markdown documentation, no preamble."""

def stream_codebase_docs(file_tree, content):
    prompt = CODEBASE_PROMPT.format(file_tree='\n'.join(file_tree), content=content)

    with client.messages.stream(
        model=MODEL,
        max_tokens=4096,
        messages=[{'role': 'user', 'content': prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield f'data: {json.dumps({"text": text})}\n\n'

    yield f'data: {json.dumps({"done": True})}\n\n'

def stream_schematic_docs(image_data, media_type):
    with client.messages.stream(
        model=MODEL,
        max_tokens=4096,
        messages=[{
            'role': 'user',
            'content': [
                {
                    'type': 'image',
                    'source': {
                        'type': 'base64',
                        'media_type': media_type,
                        'data': image_data
                    }
                },
                {
                    'type': 'text',
                    'text': SCHEMATIC_PROMPT
                }
            ]
        }]
    ) as stream:
        for text in stream.text_stream:
            yield f'data: {json.dumps({"text": text})}\n\n'

    yield f'data: {json.dumps({"done": True})}\n\n'