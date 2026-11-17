@echo off
chcp 65001 >nul
title OILS-3: Oops, I Learnt Something! - 3rd Sem Master Arcade
mode con: cols=112 lines=42 >nul 2>&1
python "%~dp0play.py" --new-window
pause
