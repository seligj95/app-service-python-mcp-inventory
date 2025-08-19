param name string
param location string = resourceGroup().location
param tags object = {}

param sku object = {
  name: 'P0V3'
  tier: 'Premium0V3'
}
param reserved bool = true

resource appServicePlan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: name
  location: location
  tags: tags
  sku: sku
  properties: {
    reserved: reserved
  }
}

output id string = appServicePlan.id
output name string = appServicePlan.name
