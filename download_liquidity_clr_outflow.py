import ast
import logging
import os
import re
import shutil
import sys
from datetime import datetime as dt 
import time
import ast
import xlsxwriter
import numpy as np
import pandas as pd
from django.conf import settings
base_dir=getattr(settings,'BASE_DIR')	
media_root=getattr(settings,'MEDIA_ROOT')
from datetime import datetime
from usermanagement.models import Users,Activity,Module
from stress_testing.models import StressClrLiquidityMaster,StressClrLiquidityAmount


def func_download_liquidity_clr_outflow(request_data,token):
	response={}
	try:
		curr_user = Users.objects.get(token=token)
		try:
			curr_activity=Activity.objects.filter(Activity_id=request_data['activity_id'])[0]
			column=['id','Particulars','Amount']
			master=StressClrLiquidityMaster.objects.all()
			stress=StressClrLiquidityAmount.objects.filter(Activity=curr_activity)
			#This is to identify the sub sub data
			sub_sub=['Credit'
					,'Liquidity'
					,'Trade Finance'
					,'Customer Short Positions covered by Other Customers’ Collateral']
			if len(stress)==0:
				# col_mapping={'Particular':'Particulars'}
				data=[]
				#This is for in flow sheet
				temp_master=master.filter(Scenario__iexact='Cash Inflow').values('Particular','id','Flag')
				for obj in temp_master:
					#This is to add space for indentation in the xlsx file 
					if int(obj.get('Flag'))==1 and obj.get('Particular').strip() in sub_sub:
						temp_dict={'id':obj['id'],'Particulars':'        '+obj.get('Particular'),'Amount':''}
					#This is to add space for indentation in the xlsx file 
					elif int(obj.get('Flag'))==1:
						temp_dict={'id':obj['id'],'Particulars':'    '+obj.get('Particular'),'Amount':''}
					elif int(obj.get('Flag'))==0:
						temp_dict={'id':obj['id'],'Particulars':obj.get('Particular'),'Amount':''}
					data.append(temp_dict)
				df1=pd.DataFrame(data,columns=column)
				# df1.rename(columns=col_mapping)
				df1=df1.replace(np.nan,' ')
				data=[]
				#This is for Out flow sheet
				temp_master=master.filter(Scenario__iexact='Cash Outflow').values('Particular','id','Flag')
				for obj in temp_master:
					#This is to add space for indentation in the xlsx file 
					if int(obj.get('Flag'))==1 and obj.get('Particular').strip() in sub_sub:
						temp_dict={'id':obj['id'],'Particulars':'        '+obj.get('Particular'),'Amount':''}
					#This is to add space for indentation in the xlsx file 
					elif int(obj.get('Flag'))==1:
						temp_dict={'id':obj['id'],'Particulars':'    '+obj.get('Particular'),'Amount':''}
					elif int(obj.get('Flag'))==0:
						temp_dict={'id':obj['id'],'Particulars':obj.get('Particular'),'Amount':''}
					data.append(temp_dict)
				df2=pd.DataFrame(data,columns=column)
				# logging.info('DF2-->'+str(data))
				# df2.rename(columns=col_mapping)
				df2=df2.replace(np.nan,' ')
			else:
				# col_mapping={'Particular':'Particulars'}
				#This is for in flow sheet
				temp_stress=stress.filter(Master__Scenario__iexact='Cash Inflow').values('Master_id','Amount')
				data=[]
				try:
					#This is to get selected by user proviously
					id=[obj.get('Master_id') for obj in temp_stress]
					for obj in temp_stress:
						particular=StressClrLiquidityMaster.objects.get(id=obj['Master_id']).Particular
						flag=StressClrLiquidityMaster.objects.get(id=obj['Master_id']).Flag
						if int(flag)==1 and particular.strip() in sub_sub:
							temp_dict={'id':obj['Master_id'],'Particulars':'       '+particular,'Amount':obj['Amount']}
						elif int(flag)==1:
							temp_dict={'id':obj['Master_id'],'Particulars':'    '+particular,'Amount':obj['Amount']}
						elif int(flag)==0:
							temp_dict={'id':obj['Master_id'],'Particulars':particular,'Amount':obj['Amount']}
						data.append(temp_dict)

					#This is to get unselected by user proviously
					temp_stress=master.filter(Scenario__iexact='Cash Inflow').exclude(id__in=id).values('Particular','id','Flag')
					for obj in temp_stress:
						particular=StressClrLiquidityMaster.objects.get(id=obj['Master_id']).Particular
						flag=StressClrLiquidityMaster.objects.get(id=obj['Master_id']).Flag
						if int(flag)==1 and particular.strip() in sub_sub:
							temp_dict={'id':obj['Master_id'],'Particulars':'       '+particular,'Amount':obj['Amount']}
						elif int(flag)==1:
							temp_dict={'id':obj['Master_id'],'Particulars':'    '+particular,'Amount':obj['Amount']}
						elif int(flag)==0:
							temp_dict={'id':obj['Master_id'],'Particulars':particular,'Amount':obj['Amount']}
						data.append(temp_dict)
					df1=pd.DataFrame(data,columns=column)
					# df1.rename(columns=col_mapping)
					df1=df1.replace(np.nan,' ')
				except Exception as e:
					exc_type, exc_obj, exc_tb = sys.exc_info()
					fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
					logging.info(str(str(exc_type) + " " +	str(fname) + " " + str(exc_tb.tb_lineno)))	
					logging.info("Error at-> " + str(e))
					response['message'] = 'Something went wrong please try again'
					response["statuscode"] = 400 
					return response
				try:
					#This is for Out flow sheet
					temp_stress=stress.filter(Master__Scenario__iexact='Cash Outflow').values('Master_id','Amount')
					data=[]
					#This is to get selected by user proviously
					id=[obj.get('Master_id') for obj in temp_stress]
					for obj in temp_stress:
						particular=StressClrLiquidityMaster.objects.get(id=obj['Master_id']).Particular
						flag=StressClrLiquidityMaster.objects.get(id=obj['Master_id']).Flag
						if int(flag)==1 and particular.strip() in sub_sub:
							temp_dict={'id':obj['Master_id'],'Particulars':'       '+particular,'Amount':obj['Amount']}
						elif int(flag)==1:
							temp_dict={'id':obj['Master_id'],'Particulars':'    '+particular,'Amount':obj['Amount']}
						elif int(flag)==0:
							temp_dict={'id':obj['Master_id'],'Particulars':particular,'Amount':obj['Amount']}
						data.append(temp_dict)
					#This is to get unselected by user proviously
					temp_stress=master.filter(Scenario__iexact='Cash Outflow').exclude(id__in=id).values('Particular','id','Flag')
					for obj in temp_stress:
						if int(obj['Flag'])==1 and obj['Particular'].strip() in sub_sub:
							temp_dict={'id':obj['id'],'Particulars':'       '+obj['Particular'],'Amount':obj.get('Amount','')}
						elif int(obj['Flag'])==1:
							temp_dict={'id':obj['id'],'Particulars':'    '+obj['Particular'],'Amount':obj.get('Amount','')}
						elif int(obj['Flag'])==0:
							temp_dict={'id':obj['id'],'Particulars':obj['Particular'],'Amount':obj.get('Amount','')}
						data.append(temp_dict)
					df2=pd.DataFrame(data,columns=column)
					# df2.rename(columns=col_mapping)
					df2=df2.replace(np.nan,' ')
				except Exception as e:
					exc_type, exc_obj, exc_tb = sys.exc_info()
					fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
					logging.info(str(str(exc_type) + " " +	str(fname) + " " + str(exc_tb.tb_lineno)))	
					logging.info("Error at-> " + str(e))
					response['message'] = 'Something went wrong please try again'
					response["statuscode"] = 400 
					return response
			temp_time=str(time.time()).split('.')[0].replace(' ','-') + ".xlsx"

			if not os.path.exists(media_root + "/" + curr_user.hashkey + "/templates"):
				os.makedirs(media_root + "/" + curr_user.hashkey + "/templates")

			file_name = media_root + "/" + curr_user.hashkey + "/templates/" + temp_time
			# logging.info('Dataframe-->'+str(df1.columns))
			# All sheets in one excel file
			writer = pd.ExcelWriter(file_name)
			# df1.to_excel(writer,index=False,columns=col_mapping,sheet_name='Cash Inflow')
			# df2.to_excel(writer,index=False,columns=col_mapping,sheet_name='Cash Outflow')
			df1.to_excel(writer,index=False,sheet_name='Cash Inflow')
			df2.to_excel(writer,index=False,sheet_name='Cash Outflow')
			""" Excel Formatting """
			workbook = writer.book
			worksheet = writer.sheets['Cash Inflow']
			worksheet.set_column('A:A',10)
			worksheet.set_column('B:B',70)
			worksheet.set_column('C:Z', 20)
			border_fmt = workbook.add_format({'bottom':1, 'top':1, 'left':1, 'right':1,'text_wrap': True})
			format = workbook.add_format({'bg_color': '#0e175c'})
			font_format = workbook.add_format({'font_color': '#ffffff','text_wrap': True})
			worksheet.conditional_format(xlsxwriter.utility.xl_range(0, 0, len(df1), len(df1.columns)-1), {'type': 'no_errors', 'format': border_fmt})
			worksheet.conditional_format(xlsxwriter.utility.xl_range(0, 0, 0, len(df1.columns)-1), {'type': 'no_errors', 'format': format})
			worksheet.conditional_format(xlsxwriter.utility.xl_range(0, 0, 0, len(df1.columns)-1), {'type': 'no_errors', 'format': font_format})
			worksheet = writer.sheets['Cash Outflow']
			worksheet.set_column('A:A',10)
			worksheet.set_column('B:B',70)
			worksheet.set_column('C:Z',20)
			border_fmt = workbook.add_format({'bottom':1, 'top':1, 'left':1, 'right':1,'text_wrap': True})
			format = workbook.add_format({'bg_color': '#0e175c'})
			font_format = workbook.add_format({'font_color': '#ffffff','text_wrap': True})
			worksheet.conditional_format(xlsxwriter.utility.xl_range(0, 0, len(df2), len(df2.columns)-1), {'type': 'no_errors', 'format': border_fmt})
			worksheet.conditional_format(xlsxwriter.utility.xl_range(0, 0, 0, len(df2.columns)-1), {'type': 'no_errors', 'format': format})
			worksheet.conditional_format(xlsxwriter.utility.xl_range(0, 0, 0, len(df2.columns)-1), {'type': 'no_errors', 'format': font_format})
			""" end """	
			writer.save()
			for dirpath, dirnames, filenames in os.walk( media_root + "/" + curr_user.hashkey + "/templates/"):
				if filenames == "Liquidity_Lcr_CashFlow.xlsx":
					os.remove(media_root + "/" + curr_user.hashkey + "/templates/" + filenames)

			shutil.move(file_name,media_root + "/" + curr_user.hashkey + "/templates/Liquidity_Lcr_CashFlow.xlsx")	
			response['file_name']="templates/Liquidity_Lcr_CashFlow.xlsx"

			# response['file_name']="Liquidity_Clr_CashFlow.xlsx"
			response['statuscode']=200
			return response
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			logging.info(str(str(exc_type) + " " +	str(fname) + " " + str(exc_tb.tb_lineno)))	
			logging.info("Error at-> " + str(e))
			response['message'] = 'The data sent is not correct'
			response["statuscode"] = 400 
			return response
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logging.info(str(str(exc_type) + " " +	str(fname) + " " + str(exc_tb.tb_lineno)))		
		logging.info("Login API error1-> " + str(e))	
		response['message'] = 'Invalid session'
		response["statuscode"] = 500
		return response