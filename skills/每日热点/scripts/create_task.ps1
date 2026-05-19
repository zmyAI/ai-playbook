$env:REPO_ROOT = "D:\github\zmyAI\ai-playbook\skills"
$action = New-ScheduledTaskAction -Execute "$env:REPO_ROOT\每日热点\scripts\fetch_hot.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -TaskName "每日热点" -Action $action -Trigger $trigger -Force
