# We strongly recommend using the required_providers block to set the
# Azure Provider source and version being used
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
    features {}
}

# Create a resource group
resource "azurerm_resource_group" "ffd-rg" {
  name     = "ffd-rg"
  location = "West Europe"
}

resource "azurerm_virtual_network" "ffd-vnet" {
  name                = "ffd-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.ffd-rg.location
  resource_group_name = azurerm_resource_group.ffd-rg.name

  subnet {
    name           = "ffd-subnet"
    address_prefix = "10.0.1.0/24"
  }
}

resource "azurerm_network_security_group" "ffd-nsg" {
  name                = "ffd-nsg"
  location            = azurerm_resource_group.ffd-rg.location
  resource_group_name = azurerm_resource_group.ffd-rg.name

  security_rule {
    name                       = "allow-all-inbound"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "allow-all-outbound"
    priority                   = 200
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "ffd-sga" {
  for_each = { for subnet in azurerm_virtual_network.ffd-vnet.subnet : subnet.name => subnet }

  subnet_id                 = each.value.id
  network_security_group_id = azurerm_network_security_group.ffd-nsg.id
}