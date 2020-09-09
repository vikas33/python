triggerNameMapping = [

    {
        "condition": "import consus.resources.DiagnosticOrderResource\n\n/*\n * Checks for order status and makes it not visible whenever it's Cancelled.\n*/\n\nprop = new Properties()\n//Value is then retrieved from properties file\ndebug = false\ntriggerName = \"***** ORDER CREATE - CHECK CANCELLED STATUS (Condition Code): \"\n\n/*\n * Logs entries according to the level provided.\n */\ndef logme(String entry, String level = \"info\") {\n    switch(level) {\n        case \"info\":\n            log.info(triggerName + entry)\n            break\n        case \"error\":\n            log.error(triggerName + entry)\n            break\n        case \"warning\":\n            log.warning(triggerName + entry)\n            break\n        case \"debug\":\n            log.debug(triggerName + entry)\n            break\n        default:\n            log.info(triggerName + entry)\n    }\n}\n\n\n/*\n * Loads properties file from path provided as argument.\n * If not provided, a default path is used.\n * If properties cannot be loaded, prop is null.\n */\ndef loadProp(String propFilePath = null, Properties prop) {\n\tif(propFilePath == null)\n\t\tpropFilePath = \"/etc/customer/icas.properties\"\n\ttry {\n\t\tInputStream input = new FileInputStream(propFilePath)\n\t\tprop.load(input)\n\t\tString sDebug = prop.getProperty(\"debug\")\n\t\tlogme(\"Debug level from properties file ${propFilePath}: ${sDebug}\", \"info\")\n\n\t\tif(sDebug)\n\t\t\tdebug = Boolean.parseBoolean(sDebug)\n\t\tif(debug)\n\t\t\tlogme(\"Properties: \" + prop, \"info\")\n\n\t} catch (IOException ex) {\n\t\tex.printStackTrace();\n\t\tprop = null\n\t}\n}\n\nlogme(\"Condition code start\", \"info\")\nloadProp(prop)\nlogme(\"Debug: ${debug}\", \"info\")\n\nif(debug)\n\tlogme(\"inputMap.obj: \" + inputMap.obj)\n\nhideOrder = prop.getProperty(\"hideCanceledOrders\")\nif(hideOrder && hideOrder.trim().length() > 0) {\n    bHideOrder = Boolean.parseBoolean(hideOrder)\n    if(bHideOrder) {\n        logme(\"Cancelled orders to be hidden, going ahead with action code\", \"info\")\n        returnMap.runTrigger = true\n        return\n    }\n} else {\n    logme(\"Cannot retrieve any information on property file\", \"info\")\n    logme(\"Trigger will not run\", \"info\")\n    returnMap.runTrigger = false\n    return\n}",
        "actionCode": "import consus.resources.DiagnosticOrderResource\n\n/*\n * Checks for order status and makes it not visible whenever it's Cancelled.\n*/\n\nprop = new Properties()\n//Value is then retrieved from properties file\ndebug = false\ntriggerName = \"***** ORDER CREATE - CHECK CANCELLED STATUS (Action Code): \"\n\n/*\n * Logs entries according to the level provided.\n */\ndef logme(String entry, String level = \"info\") {\n    switch(level) {\n        case \"info\":\n            log.info(triggerName + entry)\n            break\n        case \"error\":\n            log.error(triggerName + entry)\n            break\n        case \"warning\":\n            log.warning(triggerName + entry)\n            break\n        case \"debug\":\n            log.debug(triggerName + entry)\n            break\n        default:\n            log.info(triggerName + entry)\n    }\n}\n\n\n/*\n * Loads properties file from path provided as argument.\n * If not provided, a default path is used.\n * If properties cannot be loaded, prop is null.\n */\ndef loadProp(String propFilePath = null, Properties prop) {\n\tif(propFilePath == null)\n\t\tpropFilePath = \"/etc/customer/icas.properties\"\n\ttry {\n\t\tInputStream input = new FileInputStream(propFilePath)\n\t\tprop.load(input)\n\t\tString sDebug = prop.getProperty(\"debug\")\n\t\tlogme(\"Debug level from properties file ${propFilePath}: ${sDebug}\", \"info\")\n\n\t\tif(sDebug)\n\t\t\tdebug = Boolean.parseBoolean(sDebug)\n\t\tif(debug)\n\t\t\tlogme(\"Properties: \" + prop, \"info\")\n\n\t} catch (IOException ex) {\n\t\tex.printStackTrace();\n\t\tprop = null\n\t}\n}\n\nlogme(\"Action code start\", \"info\")\nloadProp(prop)\nlogme(\"Debug: ${debug}\", \"info\")\n\nif(debug)\n\tlogme(\"inputMap.obj: \" + inputMap.obj)\n\nDiagnosticOrderResource dor = new DiagnosticOrderResource().getPersistedObject(inputMap.obj.id)\nif(dor) {\n    logme(\"Order retrieved. going to check the status...\", \"info\")\n    logme(\"Order status: \" + dor.status?.value)\n    if(dor.status?.value == \"Cancelled\" || dor.status?.value == \"Canceled\") {\n        logme(\"Order is canceled and must be hidden\", \"info\")\n        dor.globalVisible = false\n        if(dor.update()) {\n            logme(\"Order updated, no more visible\", \"info\")\n            returnMap.triggerSuccess = true\n            return\n        } else {\n            logme(\"Cannot update the order !!!\", \"info\")\n            returnMap.triggerSuccess = false\n            return\n        }\n    } else {\n        logme(\"Order status is not Cancelled or Canceled, nothing to do\", \"info\")\n        returnMap.triggerSuccess = true\n        return\n    }\n} else {\n    logme(\"Cannot retrieve order data\", \"info\")\n    returnMap.triggerSuccess = false\n    return\n}",
        "enabled": True,
        "triggerName": "[Agfa Triggers 2.0] Hide canceled order",
        "triggerType": "CREATE",
        "description": "[Agfa Triggers 2.0] Hide canceled order",
        "triggerResource": "DiagnosticOrder"
    }

]


