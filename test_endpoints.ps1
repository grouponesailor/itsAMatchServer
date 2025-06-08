# Test GET endpoint
Write-Host "`nTesting GET /user/preferences/user1:"
Invoke-WebRequest -Uri "http://localhost:8000/user/preferences/user1" -Method GET -Headers @{"accept"="application/json"} | Select-Object -ExpandProperty Content

# Test POST endpoint (create new user)
Write-Host "`nTesting POST /user/preferences/:"
$body = @{
    user_id = 'user6'
    preferences = @{
        theme = 'dark'
        notifications_enabled = $true
        language = 'jp'
    }
    settings = @{
        timezone = 'Asia/Tokyo'
        location = 'JP'
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/user/preferences/" -Method POST -Body $body -Headers @{"Content-Type"="application/json"} | Select-Object -ExpandProperty Content

# Test PUT endpoint (update user)
Write-Host "`nTesting PUT /user/preferences/user1:"
$updateBody = @{
    preferences = @{
        theme = 'light'
        notifications_enabled = $false
        language = 'en'
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/user/preferences/user1" -Method PUT -Body $updateBody -Headers @{"Content-Type"="application/json"} | Select-Object -ExpandProperty Content

# Test GET after update
Write-Host "`nTesting GET after update /user/preferences/user1:"
Invoke-WebRequest -Uri "http://localhost:8000/user/preferences/user1" -Method GET -Headers @{"accept"="application/json"} | Select-Object -ExpandProperty Content

# Test DELETE endpoint
Write-Host "`nTesting DELETE /user/preferences/user6:"
Invoke-WebRequest -Uri "http://localhost:8000/user/preferences/user6" -Method DELETE -Headers @{"accept"="application/json"} | Select-Object -ExpandProperty Content

# Verify deletion
Write-Host "`nVerifying deletion (should return 404):"
try {
    Invoke-WebRequest -Uri "http://localhost:8000/user/preferences/user6" -Method GET -Headers @{"accept"="application/json"} | Select-Object -ExpandProperty Content
} catch {
    Write-Host "Expected 404 Error: User6 was successfully deleted"
} 