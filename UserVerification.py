import logging
from django.http import JsonResponse
import json
from urllib.parse import parse_qs
from usermanagement.models import Users


class CheckToken:
	def __init__(self, get_response):
		self.get_response = get_response
		# One-time configuration and initialization.

	def __call__(self, request):
		try:
			if request.META["URL"].strip("/") not in ["loginapi","register-user","reset-password","logout","update-password"] and request.META["REQUEST_METHOD"] == "POST":
				if "application/x-www-form-urlencoded" in request.META["HTTP_CONTENT_TYPE"]:
					# logging.info(getattr(request, '_body', request.body))
					request_data = parse_qs(getattr(request, '_body', request.body).decode("utf-8"))
				elif "application/json" in request.META["HTTP_CONTENT_TYPE"]:
					# logging.info(getattr(request, '_body', request.body))
					request_data = json.loads(getattr(request, '_body', request.body).decode("utf-8"))
				elif "multipart/form-data;" in request.META["HTTP_CONTENT_TYPE"]:
					# logging.info("~3~")
					temp_arr = str(request.body).split("------WebKitFormBoundary")
					for x in temp_arr:
						if "token" in x:
							temp_str = x
							break		
					# logging.info(str(temp_str))
					request_data = {"token":[temp_str.split("name=")[1].split("\\r")[-2].strip("\\n")]}
					# logging.info(str(request_data["token"]))
				else:
					# logging.info("!!!!!!!!!@!@!@@@@@@@@@@@@@")
					pass
				if request_data.get("token",0) == 0:
					# logging.info("~1~")
					# logging.info(str(request_data).split("WebKitFormBoundary")[-1])
					return JsonResponse({"statuscode":403})
				else:
					try:
						curr_user = Users.objects.filter(token=request_data["token"][0])[0]
						if curr_user.user_validated is None or curr_user.user_validated == 0 or curr_user.active == 0:
							return JsonResponse({"statuscode":403})
						else:
							"""
							Only in this case the response will pass this middleware
							"""
							pass
					except Exception as e:#Token did not match
						logging.info("ERROR1->"+str(e))
						return JsonResponse({"statuscode":403})   
			#Checks if the user is verified for Login API
			elif request.META["URL"].strip("/") == "loginapi" and request.META["REQUEST_METHOD"] == "POST":
				if "application/x-www-form-urlencoded" in request.META["HTTP_CONTENT_TYPE"]:
					# logging.info("Login API")
					# logging.info(getattr(request, '_body', request.body))
					request_data = parse_qs(getattr(request, '_body', request.body).decode("utf-8"))
					# logging.info(str(request_data))
				elif "application/json" in request.META["HTTP_CONTENT_TYPE"]:
					# logging.info(getattr(request, '_body', request.body).decode("utf-8") )
					request_data = json.loads(getattr(request, '_body', request.body))
				else:
					# logging.info("LoginAPI content type error")     
					pass
				try:
					logging.info(request_data["email"])
					curr_user = Users.objects.filter(email=request_data["email"][0])[0]
					logging.info(curr_user.user_validated)
					if curr_user.user_validated is None or curr_user.user_validated == 0 or curr_user.active == 0:
						return JsonResponse({"statuscode":400,"message":"Your account is not active. Please click on the link sent to your email at the time of Registration."})
					else:
						"""
						Only in this case the response will pass this middleware
						"""
						pass
				except Exception as e:#Email ID did not exist in record
					logging.info("Email does not exists "+str(e))
					return JsonResponse({"statuscode":403})   
			#Only verfied users will be able to use download file APIs.
			#This middleware only checks getfile GET API request, all other GET APIs are passed
			elif (request.META["URL"].strip("/") == "getfile" and request.META["REQUEST_METHOD"] == "GET"):      
				try:
					token = request.META["HTTP_TOKEN"]
					curr_user = Users.objects.filter(token=token)[0]
					if curr_user.user_validated is None or curr_user.user_validated == 0 or curr_user.active == 0::
						return JsonResponse({"statuscode":403})
					else:
						"""
						Only in this case the response will pass this middleware
						"""
						pass
				except:#Token did not match
					return JsonResponse({"statuscode":403})                         
		except Exception as e:
			logging.info("###2####")
			logging.info(e)
			return JsonResponse({"statuscode":403})
		response = self.get_response(request)
		return response        