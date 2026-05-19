@echo off
REM 每日热点定时抓取脚本
REM 需要 Chrome 已打开且 bb-browser/opencli 扩展已连接
REM 运行时间: 每日 9:00

set OUTDIR=D:\github\zmyAI\每日热点
set TODAY=%DATE:~0,10%
set OUTFILE=%OUTDIR%\%TODAY%.md

echo # 每日热点 — %TODAY% > "%OUTFILE%"
echo. >> "%OUTFILE%"

REM 逐个抓取平台数据（失败则跳过）
bb-browser site toutiao/hot >> "%OUTFILE%" 2>nul || echo [头条 抓取失败] >> "%OUTFILE%"
echo --- >> "%OUTFILE%"
bb-browser site 36kr/newsflash >> "%OUTFILE%" 2>nul || echo [36氪 抓取失败] >> "%OUTFILE%"

echo. >> "%OUTFILE%"
echo 抓取完成: %OUTFILE%
