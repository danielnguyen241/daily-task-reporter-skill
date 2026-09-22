#!/usr/bin/env bash
set -e

echo "🚀 Đang cài đặt Daily Task Reporter Skill..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_SKILL="$SCRIPT_DIR/daily-task-reporter"

# 1. Cài vào Antigravity
AG_SKILLS_DIR="$HOME/.gemini/config/skills"
if [ -d "$HOME/.gemini" ]; then
    mkdir -p "$AG_SKILLS_DIR"
    rm -rf "$AG_SKILLS_DIR/daily-task-reporter"
    cp -R "$SOURCE_SKILL" "$AG_SKILLS_DIR/daily-task-reporter"
    echo "✅ Đã cài đặt vào Google Antigravity: $AG_SKILLS_DIR/daily-task-reporter"
fi

# 2. Cài vào Codex
CODEX_SKILLS_DIR="$HOME/.codex/skills"
if [ -d "$HOME/.codex" ]; then
    mkdir -p "$CODEX_SKILLS_DIR"
    rm -rf "$CODEX_SKILLS_DIR/daily-task-reporter"
    cp -R "$SOURCE_SKILL" "$CODEX_SKILLS_DIR/daily-task-reporter"
    echo "✅ Đã cài đặt vào OpenAI Codex: $CODEX_SKILLS_DIR/daily-task-reporter"
fi

echo "🎉 Cài đặt hoàn tất 100%! Từ nay trong Codex hoặc Antigravity, bạn chỉ cần gõ:"
echo "   👉 'Điền task hôm nay vào sheet'"
