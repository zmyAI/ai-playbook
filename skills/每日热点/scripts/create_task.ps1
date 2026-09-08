$REPO_ROOT = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$action = New-ScheduledTaskAction -Execute "$REPO_ROOT\每日热点\scripts\fetch_hot.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -TaskName "每日热点" -Action $action -Trigger $trigger -Force