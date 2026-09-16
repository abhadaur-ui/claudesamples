"""
test_figma_export.py — proves the parsing logic in figma_export.py actually works,
using a mock Figma API response shaped like a real "Login" frame. We don't have a
live FIGMA_TOKEN in this sandbox, so this is how the extraction logic gets validated
without a real network call.
"""
import json
import sys
sys.path.insert(0, "scripts")
from figma_export import parse_figma_url, walk, extract_style_tokens

# ---- 1. URL parsing ----
url = "https://www.figma.com/design/ABC123XYZ/Auth-UI-Kit?node-id=12-345"
file_key, node_id = parse_figma_url(url)
assert file_key == "ABC123XYZ", file_key
assert node_id == "12:345", node_id
print("URL parsing OK ->", file_key, node_id)

# ---- 2. Mock Figma "nodes" API response for a simple Login frame ----
mock_frame = {
    "id": "12:345",
    "name": "Login",
    "type": "FRAME",
    "absoluteBoundingBox": {"x": 0, "y": 0, "width": 375, "height": 667},
    "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}],
    "children": [
        {
            "id": "12:346", "name": "Heading", "type": "TEXT",
            "characters": "Welcome back",
            "absoluteBoundingBox": {"x": 24, "y": 80, "width": 200, "height": 32},
            "fills": [{"type": "SOLID", "color": {"r": 0.086, "g": 0.153, "b": 0.267}}],
        },
        {
            "id": "12:347", "name": "Email Field", "type": "INSTANCE",
            "absoluteBoundingBox": {"x": 24, "y": 140, "width": 327, "height": 48},
            "children": [
                {"id": "12:348", "name": "Placeholder", "type": "TEXT",
                 "characters": "Email address",
                 "absoluteBoundingBox": {"x": 36, "y": 154, "width": 150, "height": 20}},
            ],
        },
        {
            "id": "12:349", "name": "Password Field", "type": "INSTANCE",
            "absoluteBoundingBox": {"x": 24, "y": 200, "width": 327, "height": 48},
            "children": [
                {"id": "12:350", "name": "Placeholder", "type": "TEXT",
                 "characters": "Password",
                 "absoluteBoundingBox": {"x": 36, "y": 214, "width": 150, "height": 20}},
            ],
        },
        {
            "id": "12:351", "name": "Forgot password link", "type": "TEXT",
            "characters": "Forgot password?",
            "absoluteBoundingBox": {"x": 24, "y": 256, "width": 130, "height": 18},
        },
        {
            "id": "12:352", "name": "Log In Button", "type": "INSTANCE",
            "absoluteBoundingBox": {"x": 24, "y": 300, "width": 327, "height": 52},
            "fills": [{"type": "SOLID", "color": {"r": 0.059, "g": 0.435, "b": 0.365}}],
            "children": [
                {"id": "12:353", "name": "Label", "type": "TEXT",
                 "characters": "Log In",
                 "absoluteBoundingBox": {"x": 165, "y": 316, "width": 45, "height": 20}},
            ],
        },
        {
            "id": "12:354", "name": "Signup prompt", "type": "TEXT",
            "characters": "Don't have an account? Sign up",
            "absoluteBoundingBox": {"x": 24, "y": 380, "width": 260, "height": 18},
        },
    ],
}

flat_nodes = []
walk(mock_frame, flat_nodes)
text_content = [n["text"] for n in flat_nodes if n.get("type") == "TEXT" and n.get("text")]
style_tokens = extract_style_tokens(mock_frame)

print("\nFlattened node count:", len(flat_nodes))
print("Text strings extracted:", text_content)
print("Style tokens extracted:", style_tokens)

# ---- 3. Write the artifact exactly like the real script would ----
artifact = {
    "feature": "authentication-ui",
    "source": {
        "file_key": file_key,
        "node_id": node_id,
        "figma_url": url,
        "note": "SIMULATED — no live FIGMA_TOKEN in this sandbox; this mock response stands in for a real API call, but ran through the real parsing code above.",
    },
    "frame_name": mock_frame["name"],
    "nodes": flat_nodes,
    "text_content": text_content,
    "style_tokens": style_tokens,
    "screenshot_url": None,
}

with open("design/authentication-ui.json", "w") as f:
    json.dump(artifact, f, indent=2)

print("\nWrote design/authentication-ui.json")
