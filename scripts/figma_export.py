#!/usr/bin/env python3
"""
figma_export.py — Step 1 of the fragment pilot: "Extract" (direct API, not Figma MCP)

Pulls ONE frame from a Figma file via Figma's plain REST API and writes a static,
self-contained JSON artifact to design/<feature>.json. Every later phase of the
pipeline (spec, plan, build) reads that file — Figma is never touched again after
this one run, which is the whole point: no live MCP connection, no tool-schema
reload on every turn.

Usage:
    export FIGMA_TOKEN=figd_xxx...                     # personal access token
    python figma_export.py <figma_url> <feature-name>

Example:
    python figma_export.py \\
        "https://www.figma.com/design/ABC123/Auth-UI?node-id=12-345" \\
        authentication-ui

Figma REST API endpoints used (https://www.figma.com/developers/api):
    GET /v1/files/:file_key/nodes?ids=:node_id   -> layout tree for one frame
    GET /v1/images/:file_key?ids=:node_id        -> a PNG render of that frame
"""

import json
import os
import re
import sys
import urllib.request
import urllib.parse

FIGMA_API = "https://api.figma.com/v1"


def parse_figma_url(url: str):
    """Extract (file_key, node_id) from a Figma design/file URL."""
    m = re.search(r"figma\.com/(?:design|file)/([a-zA-Z0-9]+)/", url)
    if not m:
        raise ValueError(f"Could not find a file key in this URL: {url}")
    file_key = m.group(1)

    node_id = None
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    if "node-id" in qs:
        # Figma shows node-id in the URL as "12-345"; the API wants "12:345"
        node_id = qs["node-id"][0].replace("-", ":")
    return file_key, node_id


def figma_get(path: str, token: str):
    req = urllib.request.Request(f"{FIGMA_API}{path}", headers={"X-Figma-Token": token})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def walk(node, out):
    """Flatten the parts of the node tree that actually matter for a spec:
    text content, interactive-looking components, and basic layout facts.
    Skips deeply nested visual-only groups to keep the artifact small."""
    entry = {
        "id": node.get("id"),
        "name": node.get("name"),
        "type": node.get("type"),
    }
    box = node.get("absoluteBoundingBox")
    if box:
        entry["box"] = {k: round(box[k]) for k in ("x", "y", "width", "height") if k in box}

    if node.get("type") == "TEXT":
        entry["text"] = node.get("characters", "")

    # Component instances are usually the meaningful interactive elements
    # (buttons, input fields, links) — worth flagging explicitly for the spec step.
    if node.get("type") in ("INSTANCE", "COMPONENT"):
        entry["component"] = True

    out.append(entry)
    for child in node.get("children", []):
        walk(child, out)


def extract_style_tokens(doc_root):
    """Pull a de-duplicated list of solid fill colors used in the frame —
    a lightweight stand-in for full design-token extraction."""
    seen = {}

    def visit(node):
        for fill in node.get("fills", []) or []:
            if fill.get("type") == "SOLID" and "color" in fill:
                c = fill["color"]
                key = tuple(round(c.get(ch, 0), 3) for ch in ("r", "g", "b"))
                if key not in seen:
                    seen[key] = "#{:02X}{:02X}{:02X}".format(
                        int(c.get("r", 0) * 255), int(c.get("g", 0) * 255), int(c.get("b", 0) * 255)
                    )
        for child in node.get("children", []):
            visit(child)

    visit(doc_root)
    return sorted(seen.values())


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    url, feature = sys.argv[1], sys.argv[2]
    token = os.environ.get("FIGMA_TOKEN")
    if not token:
        print("ERROR: set FIGMA_TOKEN (a personal access token) in your environment first.")
        sys.exit(1)

    file_key, node_id = parse_figma_url(url)
    if not node_id:
        print("ERROR: URL has no node-id — open the specific frame in Figma and copy that link.")
        sys.exit(1)

    print(f"Pulling file={file_key} node={node_id} ...")
    nodes_resp = figma_get(f"/files/{file_key}/nodes?ids={node_id}", token)
    frame_doc = nodes_resp["nodes"][node_id]["document"]

    flat_nodes = []
    walk(frame_doc, flat_nodes)
    text_content = [n["text"] for n in flat_nodes if n.get("type") == "TEXT" and n.get("text")]
    style_tokens = extract_style_tokens(frame_doc)

    images_resp = figma_get(f"/images/{file_key}?ids={node_id}&format=png", token)
    image_url = images_resp.get("images", {}).get(node_id)

    artifact = {
        "feature": feature,
        "source": {"file_key": file_key, "node_id": node_id, "figma_url": url},
        "frame_name": frame_doc.get("name"),
        "nodes": flat_nodes,
        "text_content": text_content,
        "style_tokens": style_tokens,
        "screenshot_url": image_url,
    }

    out_path = f"design/{feature}.json"
    os.makedirs("design", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(artifact, f, indent=2)

    print(f"Wrote {out_path} — {len(flat_nodes)} nodes, {len(text_content)} text strings.")
    print("Figma is not touched again after this — every later phase reads this file.")


if __name__ == "__main__":
    main()
