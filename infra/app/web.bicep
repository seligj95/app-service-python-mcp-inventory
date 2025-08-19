param name string
param location string = resourceGroup().location
param tags object = {}

param appServicePlanId string
param pythonVersion string = '3.11'
param appSettings object = {}

resource web 'Microsoft.Web/sites@2024-04-01' = {
  name: name
  location: location
  tags: tags
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlanId
    reserved: true
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|${pythonVersion}'
      alwaysOn: true
      ftpsState: 'FtpsOnly'
      appSettings: [
        for setting in items(appSettings): {
          name: setting.key
          value: setting.value
        }
      ]
    }
  }
}

output id string = web.id
output name string = web.name
output uri string = 'https://${web.properties.defaultHostName}'
