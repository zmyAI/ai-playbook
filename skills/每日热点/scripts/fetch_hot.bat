@echo off
REM 每日热点定时抓取脚本
REM 需要 Chrome 已打开且 bb-browser 已连接
REM 运行时间：每日 9:00

set OUTDIR=D:\github\zmyAI\每日热点
set TODAY=%DATE:~0,10%
set OUTFILE=%OUTDIR%\%TODAY%.md

echo # 每日热点 — %TODAY% > "%OUTFILE%"
echo. >> "%OUTFILE%"
echo ^> 抓取时间：%TODAY% ^| 成功：头条、36氪、知乎、B站、雪球、东方财富、ProductHunt、Reddit >> "%OUTFILE%"
echo. >> "%OUTFILE%"

echo --- >> "%OUTFILE%"
echo ## 🔥 AI 相关热点 >> "%OUTFILE%"
echo. >> "%OUTFILE%"

echo [36氪] >> "%OUTFILE%"
bb-browser site 36kr/newsflash >> "%OUTFILE%" 2>nul || echo [36氪 抓取失败] >> "%OUTFILE%"
echo. >> "%OUTFILE%"

echo [知乎 AI] >> "%OUTFILE%"
bb-browser site zhihu/hot >> "%OUTFILE%" 2>nul || echo [知乎 抓取失败] >> "%OUTFILE%"
echo. >> "%OUTFILE%"

echo [B站] >> "%OUTFILE%"
bb-browser site bilibili/popular >> "%OUTFILE%" 2>nul || echo [B站 抓取失败] >> "%OUTFILE%"
echo. >> "%OUTFILE%"

echo [Reddit] >> "%OUTFILE%"
bb-browser site reddit/hot >> "%OUTFILE%" 2>nul || echo [Reddit 抓取失败] >> "%OUTFILE%"
echo. >> "%OUTFILE%"

echo [ProductHunt] >> "%OUTFILE%"
bb-browser site producthunt/today >> "%OUTFILE%" 2>nul || echo [ProductHunt 抓取失败] >> "%OUTFILE%"
echo. >> "%OUTFILE%"

echo [头条] >> "%OUTFILE%"
bb-browser site toutiao/hot >> "%OUTFILE%" 2>nul || echo [头条 抓取失败] >> "%OUTFILE%"
echo. >> "%OUTFILE%"

echo --- >> "%OUTFILE%"
echo ## 💰 财富/理财热点 >> "%OUTFILE%"
echo. >> "%OUTFILE%"

echo [雪球] >> "%OUTFILE%"
bb-browser site xueqiu/hot >> "%OUTFILE%" 2>nul || echo [雪球 抓取失败] >> "%OUTFILE%"
echo. >> "%OUTFILE%"

echo [东方财富] >> "%OUTFILE%"
bb-browser site eastmoney/news >> "%OUTFILE%" 2>nul || echo [东方财富 抓取失败] >> "%OUTFILE%"
echo. >> "%OUTFILE%"

echo. >> "%OUTFILE%"
echo 抓取完成: %OUTFILE%
