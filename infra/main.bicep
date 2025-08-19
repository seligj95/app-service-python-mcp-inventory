targetScope = 'resourceGroup'

@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention, the name of the resource group for your application will use this name, prefixed with rg-')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Id of the user or app to assign application roles')
param principalId string = ''

// Optional parameters to override the default ASP settings
@description('The language worker runtime to load in the function app')
param pythonVersion string = '3.11'

@description('The SKU of the App Service plan')
param appServicePlanName string = ''

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = {
  'azd-env-name': environmentName
}

// The application backend is hosted in Azure App Service
module web './app/web.bicep' = {
  name: 'web'
  params: {
    name: '${abbrs.webSitesAppService}web-${resourceToken}'
    location: location
    tags: tags
    appServicePlanId: appServicePlan.outputs.id
    pythonVersion: pythonVersion
  }
}

// Create an App Service Plan to group applications under the same payment plan and SKU
module appServicePlan './shared/app-service-plan.bicep' = {
  name: 'app-service-plan'
  params: {
    name: !empty(appServicePlanName) ? appServicePlanName : '${abbrs.webServerFarms}${resourceToken}'
    location: location
    tags: tags
    sku: {
      name: 'P0V3'
      tier: 'Premium0V3'
    }
    reserved: true
  }
}

// App outputs
output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output WEB_URI string = web.outputs.uri
