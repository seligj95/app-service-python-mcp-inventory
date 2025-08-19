param name string
param location string = resourceGroup().location
param tags object = {}

param appServicePlanId string
param pythonVersion string = '3.11'

resource web 'Microsoft.Web/sites@2024-04-01' = {
  name: name
  location: location
  tags: union(tags, {
    'azd-service-name': 'web'
  })
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlanId
    reserved: true
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|${pythonVersion}'
      alwaysOn: true
      ftpsState: 'FtpsOnly'
      appCommandLine: 'python -m uvicorn main:app --host 0.0.0.0 --port 8000'
      appSettings: [
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
        {
          name: 'ENABLE_ORYX_BUILD'
          value: 'true'
        }
        {
          name: 'PYTHONPATH'
          value: '/home/site/wwwroot'
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
      ]
      cors: {
        allowedOrigins: ['*']
        supportCredentials: false
      }
      healthCheckPath: '/health'
    }
  }
}

output id string = web.id
output name string = web.name
output uri string = 'https://${web.properties.defaultHostName}'
