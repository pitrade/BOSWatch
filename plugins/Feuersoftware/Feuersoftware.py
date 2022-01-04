#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Feuersoftware-Plugin to send POCSAG-messages to Feuersoftware

@author: Marc Hinterthaner

@requires: Feuersoftware-Configuration has to be set in the config.ini
@requires: module requests
"""

#
# Imports
#
import logging # Global logger
from includes import globalVars  # Global variables

# Helper function, uncomment to use
#from includes.helper import timeHandler
from includes.helper import wildcardHandler
from includes.helper import configHandler

# for Feuersoftware API-call
import requests
from requests.structures import CaseInsensitiveDict

def alarm(alarmData):
	"""
	@type    poc_id: string
	@param   poc_id: JSON formatted parameters

	@requires: Feuersoftware-Configuration has to be set in the config.ini
    @requires: module requests

	@return:    nothing
	"""
    logging.debug("Feuersoftware alarm")
	apiKey = globalVars.config.get("Feuersoftware", "accesskey")
    logging.debug("API-Key   : %s", facts)

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + apiKey
    headers["Content-Type"] = "application/json"

    resp = requests.post(url, headers=headers, data=alarmData)
    logging.debug("Status Code   : %s", resp.status_code)

##
#
# onLoad (init) function of Feuersoftware-plugin
# will be called one time by the pluginLoader on start
#
def onLoad():
	"""
	While loading the plugins by pluginLoader.loadPlugins()
	this onLoad() routine is called one time for initialize the plugin
	@requires:  nothing
	@return:    nothing
	"""
	logging.debug("Feuersoftware onLoad")
    return

##
#
# Main function of Feuersoftware-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the Feuersoftware-Plugin.
	@type    typ:  string (POC)
	@param   typ:  Typ of the dataset
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter for dispatch
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires: Feuersoftware-Configuration has to be set in the config.ini
    @requires: module requests

	@return:    nothing
	"""
    logging.debug("Feuersoftware run")

	try:
		if configHandler.checkConfig("Feuersoftware"): #read and debug the config

			#logging.debug(globalVars.config.get("template", "test1"))

			if typ == "POC":
                
                start = datetime.utcnow().isoformat()[:-3]+'Z'
                logging.debug("Start   : %s", start)
                
                keyword = globalVars.config.get("Feuersoftware", "keyword")
                keyword = wildcardHandler.replaceWildcards(keyword, data)
                logging.debug("Keyword   : %s", keyword)
                
                facts = globalVars.config.get("Feuersoftware", "facts")
                facts = wildcardHandler.replaceWildcards(facts, data)
                logging.debug("Facts   : %s", facts)
                
                ric = globalVars.config.get("Feuersoftware", "ric")
                ric = wildcardHandler.replaceWildcards(ric, data)
                logging.debug("RIC   : %s", ric)
                
                city = globalVars.config.get("Feuersoftware", "city")
                city = wildcardHandler.replaceWildcards(city, data)
                logging.debug("City   : %s", city)

                alarmData = """
                {{
                "Start": "{0}",
                "Status": "new",
                "AlarmEnabled": true,
                "Keyword": "{1}",
                "Facts": "{2}",
                "Ric": "{3}",
                "Address": {{
                    "City": "{4}"
                }}
                }}
                """.format(start, keyword, facts, ric, city)

                alarm(alarmData)
			else:
				logging.warning("%s not supported or invalid", typ)

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)