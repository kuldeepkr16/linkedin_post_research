#!/usr/bin/env bash
# Download Qwen2.5-VL vision model for local receipt extraction.
# Requires Ollama: https://ollama.com
# Then run:  python extract_receipt.py <image> --backend ollama

set -e
echo "Pulling Qwen2.5-VL 7B (document/receipt vision model)..."
ollama pull qwen2.5vl:7b
echo "Done. Use:  python extract_receipt.py <image.jpg> --backend ollama --pretty"
