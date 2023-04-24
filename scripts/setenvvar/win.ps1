Write-Host "Setting environment variable FFD_MONGO_HOST to localhost"
[Environment]::SetEnvironmentVariable("FFD_MONGO_HOST", "localhost", "User")

Write-Host "Setting environment variable FFD_MONGO_PORT to 27017"
[Environment]::SetEnvironmentVariable("FFD_MONGO_PORT", "27017", "User")

Write-Host "Setting environment variable FFD_MONGO_USER to root"
[Environment]::SetEnvironmentVariable("FFD_MONGO_USER", "root", "User")

Write-Host "Setting environment variable FFD_MONGO_PASSWORD to root"
[Environment]::SetEnvironmentVariable("FFD_MONGO_PASSWORD", "root", "User")

Write-Host "Setting environment variable FFD_REDIS_HOST to localhost"
[Environment]::SetEnvironmentVariable("FFD_REDIS_HOST", "localhost", "User")

Write-Host "Setting environment variable FFD_REDIS_PORT to 6379"
[Environment]::SetEnvironmentVariable("FFD_REDIS_PORT", "6379", "User")

Write-Host "Setting environment variable FFD_GOSERVER_HOST to localhost"
[Environment]::SetEnvironmentVariable("FFD_GOSERVER_HOST", "localhost", "User")

Write-Host "Setting environment variable FFD_GOSERVER_PORT to 6500"
[Environment]::SetEnvironmentVariable("FFD_GOSERVER_PORT", "6500", "User")

