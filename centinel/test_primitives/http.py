import ConfigParser
import os
import utils.http as http
import base64

from centinel.experiment import Experiment

class ConfigurableHTTPRequestExperiment(Experiment):
    name = "config_http"

    def __init__(self, input_file):
        self.input_file  = input_file
        self.results = []
        self.host = None
        self.path = "/"
	self.args = dict()

    def run(self):
	parser = ConfigParser.ConfigParser()
	parser.read([self.input_file,])
	if not parser.has_section('HTTP'):
	    return

	self.args.update(parser.items('HTTP'))
	
	self.headers = {}
	self.addHeaders = False

	if 'browser' in self.args.keys():
	    self.browser = self.args['browser']
	    self.addHeaders = True
	    if self.browser == "ie" or self.browser == "Internet Explorer":
		 self.headers["user-agent"] = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)"
	    elif self.browser == "Firefox":
		 self.headers["user-agent"] = "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"
	    elif self.browser == "Chrome" or self.browser == "Google Chrome":
		 self.headers["user-agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17"
	url_list = parser.items('URLS')
	for url in url_list[0][1].split():
	    self.host = url
	    self.http_request()

    def http_request(self):
	if self.addHeaders:
            result = http.get_request(self.host, self.path, self.headers)
	else:
            result = http.get_request(self.host, self.path)            
	
	result["response"]["body"] = base64.b64encode(result["response"]["body"])
        self.results.append(result)