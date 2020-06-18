import pandas as pd
import numpy as np
import datetime
import re
import os
import xlwings as xw
import chardet
import zipfile


bot2_table_map = {'purchasing document header table': 'ekko',
                  'purchasing document item table': 'ekpo',
                  'vendor master (general section) information': 'lfa1',
                  'scheduling agreement scheduling lines': 'eket',
                  'terms of payments text table': 't052u',
                  'item category description table': 't163y',
                  'purchase requisition table': 'eban',
                  'user name/address key assignment': 'usr21',
                  'sap person/address assignment table': 'adcp',
                  'history per purchasing document table': 'ekbe',
                  'sap tax codes-text table': 't5vs5',
                  'account group names pooled table': 't077y',
                  'sap transaction code texts pooled table': 'tstct',
                  "change document header table (object class 'kred')": 'cdhdr',
                  "change document items cluster table (object class 'kred')": 'cdpos',
                  'sap accounting document header table': 'bkpf',
                  'sap accounting : secondary index for vendors (cleared items) data': 'bsak',
                  'sap accounting: secondary index for vendors table': 'bsik',
                  'sap document type text pooled table': 't003t',
                  'vendor master (bank details) table': 'lfbk',
                  'hr master record (personal)': 'pa0002',
                  'hr master record (addresses)': 'pa0006',
                  'hr master record (bank details)': 'pa0009',
                  'vendor master (company code) table': 'lfb1',
                  'vendor master excise additional data (pan details)': 'j_1imovend',
                  'payment method description': 't042zt',
                  'sap accounting segment cluster table': 'bseg',
                  'sap gl account master record': 'skat',
                  'posting key names pooled table': 'tbslt',
                  'accounting secondary index for customers': 'bsad',
                  'accounting secondary index for customers(open items)': 'bsid',
                  'customer master': 'kna1',
                  'business address services table': 'adrp',
                  'assignment of roles to tcodes': 'agr_tcodes',
                  'assignment of roles to users': 'agr_users',
                  'list of payment document type': 'payment_doc_table',
                  'list of invoice document type': 'invoice_doc_table',
                  'list of document type': 'general_doc_table',
                  'list of tcodes table': 'ref_input_tcodes',
                  'list of document type and transaction code': 'doc_trans_table'}

bot2_technical_headers = {
    'ekko': {
        'company_code': 'BUKRS__EKKO',
        'purchasing_org': 'EKORG__EKKO',
        'purchasing_group': 'EKGRP__EKKO',
        'purchasing_document': 'EBELN__EKKO',
        'purch_doc_category': 'BSTYP__EKKO',
        'created_on': 'AEDAT__EKKO',
        'document_date': 'BEDAT__EKKO',
        'created_by': 'ERNAM__EKKO',
        'vendor': 'LIFNR__EKKO',
        'terms_of_payment': 'ZTERM__EKKO',
        'currency_key': 'WAERS__EKKO',
        'exchange_rate': 'WKURS__EKKO',
        'release_status': 'FRGZU__EKKO',
        'release_amount': 'RLWRT__EKKO'
    },
    'ekpo': {
        'purchasing_document': 'EBELN__EKPO',
        'item': 'EBELP__EKPO',
        'deletion_indicator': 'LOEKZ__EKPO',
        'short_text': 'TXZ01__EKPO',
        'material': 'MATNR__EKPO',
        'plant': 'WERKS__EKPO',
        'material_group': 'MATKL__EKPO',
        'order_quantity': 'MENGE__EKPO',
        'unit_of_measure': 'MEINS__EKPO',
        'net_order_price': 'NETPR__EKPO',
        'price_unit': 'PEINH__EKPO',
        'net_order_value': 'NETWR__EKPO',
        'gross_order_value': 'BRTWR__EKPO',
        'delivery_complete': 'ELIKZ__EKPO',
        'item_category': 'PSTYP__EKPO',
        'last_changed_on': 'AEDAT__EKPO',
        'company_code': 'BUKRS__EKPO',
        'purchasing_info_ref': 'INFNR__EKPO',
        'order_unit': 'BPRME__EKPO',
        'quantity_conversion': 'BPUMZ__EKPO',
        'purchase_requisition': 'BANFN__EKPO',
        'item_of_requisition': 'BNFPO__EKPO',
        'tax_code': 'MWSKZ__EKPO'
    },
    'lfa1': {
        'vendor': 'LIFNR__LFA1',
        'vendor_name': 'NAME1__LFA1',
        'account_group': 'KTOKK__LFA1',
        'country': 'LAND1__LFA1',
        'name2': 'NAME2__LFA1',
        'created_on': 'ERDAT__LFA1',
        'created_by': 'ERNAM__LFA1',
        'central_posting_block': 'SPERR__LFA1',
        'central_purchasing_block': 'SPERM__LFA1',
        'tax_number_1': 'STCD1__LFA1',
        'tax_number_3': 'STCD3__LFA1',
        'telephone_1': 'TELF1__LFA1',
        'telephone_2': 'TELF2__LFA1',
        'city1': 'ORT01__LFA1',
        'postal_code': 'PSTLZ__LFA1',
        'address': 'ADRNR__LFA1',
        'search_term': 'MCOD1__LFA1',
        'account_number_of_alternate_paye': 'LNRZA__LFA1',
        'tax_number_2': 'STCD2__LFA1',
        'payment_block': 'SPERZ__LFA1',
        'street1': 'STRAS__LFA1',
        'telebox_number': 'TELBX__LFA1',
        'fax_number': 'TELFX__LFA1',
        'teletex_number': 'TELTX__LFA1',
        'telex_number': 'TELX1__LFA1',
        'one_time_account': 'XCPDK__LFA1'
    },
    'eket': {
        'purchasing_document': 'EBELN__EKET',
        'item': 'EBELP__EKET',
        'delivery_date': 'EINDT__EKET',
        'expected_delivery_date': 'SLFDT__EKET',
        'scheduled_quantity': 'MENGE__EKET',
        'qty_delivered': 'WEMNG__EKET'
    },
    't052u': {
        'language_key': 'SPRAS__T052U',
        'payment_terms': 'ZTERM__T052U',
        'day_limit': 'ZTAGG__T052U',
        'payment_term_description': 'TEXT1__T052U'
    },
    't163y': {
        'language_key': 'SPRAS__T163Y',
        'item_category': 'PSTYP__T163Y',
        'text_for_item_category': 'PTEXT__T163Y',
        'item_category_in_purchasing_document': 'EPSTP__T163Y'
    },
    'eban': {
        'purchase_requisition': 'BANFN__EBAN',
        'item_of_requisition': 'BNFPO__EBAN',
        'deletion_indicator': 'LOEKZ__EBAN',
        'release_indicator': 'FRGKZ__EBAN',
        'release_status': 'FRGZU__EBAN',
        'release_strategy': 'FRGST__EBAN',
        'purchasing_group': 'EKGRP__EBAN',
        'created_by': 'ERNAM__EBAN',
        'changed_on': 'ERDAT__EBAN',
        'requisitioner': 'AFNAM__EBAN',
        'short_text': 'TXZ01__EBAN',
        'material': 'MATNR__EBAN',
        'plant': 'WERKS__EBAN',
        'storage_location': 'LGORT__EBAN',
        'material_group': 'MATKL__EBAN',
        'quantity_requested': 'MENGE__EBAN',
        'requisition_date': 'BADAT__EBAN',
        'delivery_date': 'LFDAT__EBAN',
        'release_date': 'FRGDT__EBAN',
        'valuation_price': 'PREIS__EBAN',
        'price_unit': 'PEINH__EBAN',
        'item_category': 'PSTYP__EBAN',
        'purchase_order': 'EBELN__EBAN',
        'purchase_order_item': 'EBELP__EBAN',
        'purchase_order_date': 'BEDAT__EBAN',
        'quantity_ordered': 'BSMNG__EBAN'
    },
    'usr21': {
        'user_name': 'BNAME__USR21',
        'personal_number': 'PERSNUMBER__USR21',
        'address_number': 'ADDRNUMBER__USR21'
    },
    'adcp': {
        'address_number': 'ADDRNUMBER__ADCP',
        'person_number': 'PERSNUMBER__ADCP',
        'office_key': 'SO_KEY__ADCP',
        'department': 'DEPARTMENT__ADCP',
        'function': 'FUNCTION__ADCP',
        'telephone_no_1': 'TEL_NUMBER__ADCP'
    },
    'ekbe': {
        'purchasing_document': 'EBELN__EKBE',
        'item': 'EBELP__EKBE',
        'material_doc_year': 'GJAHR__EKBE',
        'material_document': 'BELNR__EKBE',
        'material_doc_item': 'BUZEI__EKBE',
        'po_history_category': 'BEWTP__EKBE',
        'movement_type': 'BWART__EKBE',
        'posting_date': 'BUDAT__EKBE',
        'quantity': 'MENGE__EKBE',
        'amount_in_lc': 'DMBTR__EKBE',
        'amount': 'WRBTR__EKBE',
        'debit_credit_ind': 'SHKZG__EKBE',
        'valuation_type': 'BWTAR__EKBE',
        'delivery_completed': 'ELIKZ__EKBE',
        'reference': 'XBLNR__EKBE',
        'reference_document': 'LFBNR__EKBE',
        'reference_doc_item': 'LFPOS__EKBE',
        'entry_date': 'CPUDT__EKBE',
        'entry_time': 'CPUTM__EKBE',
        'material': 'MATNR__EKBE',
        'plant': 'WERKS__EKBE',
        'tax_code': 'MWSKZ__EKBE',
        'created_by': 'ERNAM__EKBE'
    },
    't5vs5': {
        'language_key': 'LANGU__T5VS5',
        'tax_code': 'LTKOD__T5VS5',
        'description_of_tax_code': 'ATEXT__T5VS5'
    },
    't077y': {
        'language_key': 'SPRAS__T077Y',
        'vendor_account_group': 'KTOKK__T077Y',
        'account_group_description': 'TXT30__T077Y'
    },
    'tstct': {
        'language_key': 'SPRSL__TSTCT',
        'transaction_code': 'TCODE__TSTCT',
        'transaction_text': 'TTEXT__TSTCT'
    },
    'cdhdr': {
        'object_class': 'OBJECTCLAS__CDHDR',
        'object_value': 'OBJECTID__CDHDR',
        'document_change_number': 'CHANGENR__CDHDR',
        'user1': 'USERNAME__CDHDR',
        'creation_date': 'UDATE__CDHDR',
        'time_changed': 'UTIME__CDHDR',
        'transaction_code': 'TCODE__CDHDR',
        'planned_change_number': 'PLANCHNGNR__CDHDR',
        'change_number_of_the_document': 'ACT_CHNGNO__CDHDR',
        'flag_changes': 'WAS_PLANND__CDHDR',
        'application_object_change_flag': 'CHANGE_IND__CDHDR',
        'language_key': 'LANGU__CDHDR',
        'byte_field': 'VERSION__CDHDR'
    },
    'cdpos': {
        'object_class': 'OBJECT_CLASS__CDPOS',
        'object_value': 'OBJECTID__CDPOS',
        'document_change_number': 'CHANGENR__CDPOS',
        'table_name': 'TABNAME__CDPOS',
        'table_key': 'TABKEY__CDPOS',
        'field_name': 'FNAME__CDPOS',
        'change_type': 'CHNGIND__CDPOS',
        'text_change_flag': 'TEXT_CASE__CDPOS',
        'unit_old': 'UNIT_OLD__CDPOS',
        'unit_new': 'UNIT_NEW__CDPOS',
        'referenced_currency': 'CUKY_OLD__CDPOS',
        'referenced_currency_new': 'CUKY_NEW__CDPOS',
        'new_value': 'VALUE_NEW__CDPOS',
        'old_value': 'VALUE_OLD__CDPOS'
    },
    'bkpf': {
        'company_code': 'BUKRS__BKPF',
        'document_number': 'BELNR__BKPF',
        'fiscal_year': 'GJAHR__BKPF',
        'document_type': 'BLART__BKPF',
        'document_date': 'BLDAT__BKPF',
        'posting_date': 'BUDAT__BKPF',
        'entered_on': 'CPUDT__BKPF',
        'entered_at': 'CPUTM__BKPF',
        'changed_on': 'AEDAT__BKPF',
        'translatn_date': 'WWERT__BKPF',
        'user_name': 'USNAM__BKPF',
        'transaction_code': 'TCODE__BKPF',
        'reference_document_number': 'XBLNR__BKPF',
        'recurring_entry_doc_number': 'DBBLG__BKPF',
        'reverse_document_number': 'STBLG__BKPF',
        'reverse_document_fiscal_year': 'STJAH__BKPF',
        'document_header_text': 'BKTXT__BKPF',
        'reference_key': 'AWKEY__BKPF',
        'fiscal_period': 'MONAT__BKPF'
    },
    'bsak': {
        'company_code': 'BUKRS__BSAK',
        'vendor': 'LIFNR__BSAK',
        'special_gl_ind': 'UMSKZ__BSAK',
        'clearing_date': 'AUGDT__BSAK',
        'clearing_document': 'AUGBL__BSAK',
        'assignment': 'ZUONR__BSAK',
        'fiscal_year': 'GJAHR__BSAK',
        'document_number': 'BELNR__BSAK',
        'line_item': 'BUZEI__BSAK',
        'posting_date': 'BUDAT__BSAK',
        'document_date': 'BLDAT__BSAK',
        'entry_date': 'CPUDT__BSAK',
        'currency': 'WAERS__BSAK',
        'reference': 'XBLNR__BSAK',
        'document_type': 'BLART__BSAK',
        'posting_period': 'MONAT__BSAK',
        'posting_key': 'BSCHL__BSAK',
        'trgt_special_gl_ind': 'ZUMSK__BSAK',
        'debit_credit_ind': 'SHKZG__BSAK',
        'tax_code': 'MWSKZ__BSAK',
        'amount_in_lc': 'DMBTR__BSAK',
        'amount': 'WRBTR__BSAK',
        'lc_tax_amount': 'MWSTS__BSAK',
        'tax_amount': 'WMWST__BSAK',
        'text1': 'SGTXT__BSAK',
        'gl_account': 'SAKNR__BSAK',
        'gl_account1': 'HKONT__BSAK',
        'baseline_payment_dte': 'ZFBDT__BSAK',
        'terms_of_payment': 'ZTERM__BSAK',
        'days_1': 'ZBD1T__BSAK',
        'days_2': 'ZBD2T__BSAK',
        'invoice_reference': 'REBZG__BSAK'
    },
    'bsik': {
        'company_code': 'BUKRS__BSIK',
        'vendor': 'LIFNR__BSIK',
        'special_gl_ind': 'UMSKZ__BSIK',
        'clearing_date': 'AUGDT__BSIK',
        'clearing_document': 'AUGBL__BSIK',
        'assignment': 'ZUONR__BSIK',
        'fiscal_year': 'GJAHR__BSIK',
        'document_number': 'BELNR__BSIK',
        'line_item': 'BUZEI__BSIK',
        'posting_date': 'BUDAT__BSIK',
        'document_date': 'BLDAT__BSIK',
        'entry_date': 'CPUDT__BSIK',
        'currency': 'WAERS__BSIK',
        'reference': 'XBLNR__BSIK',
        'document_type': 'BLART__BSIK',
        'posting_period': 'MONAT__BSIK',
        'posting_key': 'BSCHL__BSIK',
        'debit_credit_ind': 'SHKZG__BSIK',
        'tax_code': 'MWSKZ__BSIK',
        'amount_in_lc': 'DMBTR__BSIK',
        'amount': 'WRBTR__BSIK',
        'lc_tax_amount': 'MWSTS__BSIK',
        'tax_amount': 'WMWST__BSIK',
        'text1': 'SGTXT__BSIK',
        'gl_account': 'SAKNR__BSIK',
        'gl_account1': 'HKONT__BSIK',
        'baseline_payment_dte': 'ZFBDT__BSIK',
        'terms_of_payment': 'ZTERM__BSIK',
        'days_1': 'ZBD1T__BSIK',
        'days_2': 'ZBD2T__BSIK',
        'invoice_reference': 'REBZG__BSIK'
    },
    't003t': {
        'language_key': 'SPRAS__T003T',
        'document_type': 'BLART__T003T',
        'document_type_text': 'LTEXT__T003T'
    },
    'lfbk': {
        'vendor': 'LIFNR__LFBK',
        'bank_country': 'BANKS__LFBK',
        'bank_key': 'BANKL__LFBK',
        'bank_account': 'BANKN__LFBK'
    },
    'pa0002': {
        'personnel_number': 'PERNR__PA0002',
        'perdetails_startdate': 'BEGDA__PA0002',
        'perdetails_enddate': 'ENDDA__PA0002',
        'initials': 'INITS__PA0002',
        'last_name': 'NACHN__PA0002',
        'name_at_birth': 'NAME2__PA0002',
        'second_name': 'NACH2__PA0002',
        'first_name': 'VORNA__PA0002',
        'middle_name': 'MIDNM__PA0002',
        'gender_key': 'GESCH__PA0002',
        'date_of_birth': 'GBDAT__PA0002',
        'state': 'GBDEP__PA0002',
        'birthplace': 'GBORT__PA0002',
        'nationality': 'NATIO__PA0002',
        'marital_status_key': 'FAMST__PA0002',
        'valid_from_date': 'FAMDT__PA0002',
        'number_of_children': 'ANZKD__PA0002',
        'personal_id': 'PERID__PA0002',
        'passport_date_of_birth': 'GBPAS__PA0002',
        'known_as': 'RUFNM__PA0002',
        'country_of_birth': 'GBLND__PA0002'
    },
    'pa0006': {
        'personnel_number': 'PERNR__PA0006',
        'empaddr_startdate': 'BEGDA__PA0006',
        'empaddr_enddate': 'ENDDA__PA0006',
        'empaddr_lockind': 'SPRPS__PA0006',
        'address_record_type': 'SUBTY__PA0006',
        'name_at_birth': 'NAME2__PA0006',
        'address': 'ANSSA__PA0006',
        'city': 'ORT01__PA0006',
        'district': 'ORT02__PA0006',
        'postal_code': 'PSTLZ__PA0006',
        'country_key': 'LAND1__PA0006',
        'telephone_number': 'TELNR__PA0006',
        'address_line2': 'LOCAT__PA0006',
        'street_2': 'ADR03__PA0006',
        'street_3': 'ADR04__PA0006'
    },
    'pa0009': {
        'personnel_number': 'PERNR__PA0009',
        'payment_currency': 'WAERS__PA0009',
        'bank_country_key': 'BANKS__PA0009',
        'bank_keys': 'BKONT__PA0009',
        'bank_account_number': 'BANKN__PA0009',
        'tax_number_1': 'STCD1__PA0009',
        'tax_number_2': 'STCD2__PA0009',
        'purpose_of_bank_transfers': 'ZWECK__PA0009'
    },
    'lfb1': {
        'vendor_code': 'LIFNR__LFB1',
        'company_code': 'BUKRS__LFB1',
        'posting_block': 'SPERR__LFB1',
        'payment_methods': 'ZWELS__LFB1',
        'block_key': 'ZAHLS__LFB1',
        'payment_terms': 'ZTERM__LFB1'
    },
    'j_1imovend': {
        'vendor': 'LIFNR__J_1IMOVEND',
        'pan_number': 'J_1IPANNO__J_1IMOVEND',
        'pan_details': 'J_1IPANREF__J_1IMOVEND'
    },
    't042zt': {
        'language_key': 'SPRAS__T042ZT',
        'country_key': 'LAND1__T042ZT',
        'payment_method': 'ZLSCH__T042ZT',
        'description_of_payment_method': 'TEXT2__T042ZT'
    },
    'bseg': {
        'company_code': 'BUKRS__BSEG',
        'accounting_document_number': 'BELNR__BSEG',
        'fiscal_year': 'GJAHR__BSEG',
        'line_item': 'BUZEI__BSEG',
        'clearing_date': 'AUGDT__BSEG',
        'clearing_entry_date': 'AUGCP__BSEG',
        'clearing_document': 'AUGBL__BSEG',
        'posting_key': 'BSCHL__BSEG',
        'account_type': 'KOART__BSEG',
        'special_gl_indicator': 'UMSKZ__BSEG',
        'special_gl_type': 'UMSKS__BSEG',
        'debit_credit_ind': 'SHKZG__BSEG',
        'tax_code': 'MWSKZ__BSEG',
        'amount_in_lc': 'DMBTR__BSEG',
        'amount_in_dc': 'WRBTR__BSEG',
        'assignment_number': 'ZUONR__BSEG',
        'item_text': 'SGTXT__BSEG',
        'group_account_number': 'ALTKT__BSEG',
        'business_key': 'VORGN__BSEG',
        'controlling_area': 'KOKRS__BSEG',
        'cost_center': 'KOSTL__BSEG',
        'gl_account_number': 'SAKNR__BSEG',
        'gl_ledger_account': 'HKONT__BSEG',
        'customer': 'KUNNR__BSEG',
        'vendor_code': 'LIFNR__BSEG'
    },
    'skat': {
        'language_key': 'SPRAS__SKAT',
        'chart_of_account': 'KTOPL__SKAT',
        'gl_account_number': 'SAKNR__SKAT',
        'gl_account_short_text': 'TXT20__SKAT',
        'gl_account_long_text': 'TXT50__SKAT',
        'search_term': 'MCOD1__SKAT'
    },
    'tbslt': {
        'language_key': 'SPRAS__TBSLT',
        'posting_key': 'BSCHL__TBSLT',
        'special_gl_indicator': 'UMSKZ__TBSLT',
        'posting_key_description': 'LTEXT__TBSLT'
    },
    'bsad': {
        'company_code': 'BUKRS__BSAD',
        'customer_number': 'KUNNR__BSAD',
        'special_gl_trans_type': 'UMSKS__BSAD',
        'special_gl_indicator': 'UMSKZ__BSAD',
        'clearing_date': 'AUGDT__BSAD',
        'clearing_document': 'AUGBL__BSAD',
        'assignment_number': 'ZUONR__BSAD',
        'fiscal_year': 'GJAHR__BSAD',
        'accounting_document_number': 'BELNR__BSAD',
        'item_number': 'BUZEI__BSAD',
        'posting_date': 'BUDAT__BSAD',
        'document_date': 'BLDAT__BSAD',
        'entry_date': 'CPUDT__BSAD',
        'currency': 'WAERS__BSAD',
        'invoice_reference': 'XBLNR__BSAD',
        'document_type': 'BLART__BSAD',
        'posting_key': 'BSCHL__BSAD',
        'special_gl_ind': 'ZUMSK__BSAD',
        'debit_credit_ind': 'SHKZG__BSAD',
        'business_area': 'GSBER__BSAD',
        'tax_code': 'MWSKZ__BSAD',
        'amount_in_lc': 'DMBTR__BSAD',
        'amount_in_dc': 'WRBTR__BSAD',
        'tax_in_lc': 'MWSTS__BSAD',
        'tax_in_dc': 'WMWST__BSAD',
        'valuation_difference': 'BDIFF__BSAD',
        'item_text': 'SGTXT__BSAD',
        'gl_account_number': 'SAKNR__BSAD',
        'gl_ledger_account': 'HKONT__BSAD',
        'baseline_payment_date': 'ZFBDT__BSAD',
        'days_1': 'ZBD1T__BSAD',
        'payment_terms': 'ZTERM__BSAD',
        'payment_method': 'ZLSCH__BSAD'
    },
    'bsid': {
        'company_code': 'BUKRS__BSID',
        'customer_number': 'KUNNR__BSID',
        'special_gl_trans_type': 'UMSKS__BSID',
        'special_gl_indicator': 'UMSKZ__BSID',
        'clearing_date': 'AUGDT__BSID',
        'clearing_document': 'AUGBL__BSID',
        'assignment_number': 'ZUONR__BSID',
        'fiscal_year': 'GJAHR__BSID',
        'accounting_document_number': 'BELNR__BSID',
        'item_number': 'BUZEI__BSID',
        'posting_date': 'BUDAT__BSID',
        'document_date': 'BLDAT__BSID',
        'entry_date': 'CPUDT__BSID',
        'currency': 'WAERS__BSID',
        'invoice_reference': 'XBLNR__BSID',
        'document_type': 'BLART__BSID',
        'posting_key': 'BSCHL__BSID',
        'special_gl_ind': 'ZUMSK__BSID',
        'debit_credit_ind': 'SHKZG__BSID',
        'tax_code': 'MWSKZ__BSID',
        'amount_in_lc': 'DMBTR__BSID',
        'amount_in_dc': 'WRBTR__BSID',
        'tax_in_lc': 'MWSTS__BSID',
        'tax_in_dc': 'WMWST__BSID',
        'valuation_difference': 'BDIFF__BSID',
        'item_text': 'SGTXT__BSID',
        'gl_account_number': 'SAKNR__BSID',
        'gl_ledger_account': 'HKONT__BSID',
        'baseline_payment_date': 'ZFBDT__BSID',
        'days_1': 'ZBD1T__BSID',
        'payment_terms': 'ZTERM__BSID',
        'payment_method': 'ZLSCH__BSID'
    },
    'kna1': {
        'customer_number': 'KUNNR__KNA1',
        'country': 'LAND1__KNA1',
        'customer_name': 'NAME1__KNA1',
        'city': 'ORT01__KNA1',
        'postal_code': 'PSTLZ__KNA1',
        'address': 'STRAS__KNA1'
    },
    'adrp': {
        'person_number': 'PERSNUMBER__ADRP',
        'first_name': 'NAME_FIRST__ADRP',
        'last_name': 'NAME_LAST__ADRP',
        'name2': 'NAME2__ADRP',
        'name_text': 'NAME_TEXT__ADRP'
    },
    'agr_tcodes': {
        'user_name': 'AGR_NAME__AGR_TCODES',
        'type': 'TYPE__AGR_TCODES',
        'transaction_code': 'TCODE__AGR_TCODES',
        'exclude': 'EXCLUDE__AGR_TCODES',
        'direct': 'DIRECT__AGR_TCODES'
    },
    'agr_users': {
        'group_name': 'AGR_NAME__AGR_USERS',
        'user_name': 'UNAME__AGR_USERS'
    }}


datatype_dict = {
    'BUKRS__EKKO': 'String',
    'EKORG__EKKO': 'String',
    'EKGRP__EKKO': 'String',
    'EBELN__EKKO': 'String',
    'BSTYP__EKKO': 'String',
    'AEDAT__EKKO': 'Date',
    'BEDAT__EKKO': 'Date',
    'ERNAM__EKKO': 'String',
    'LIFNR__EKKO': 'String',
    'ZTERM__EKKO': 'String',
    'WAERS__EKKO': 'String',
    'WKURS__EKKO': 'Numeric',
    'FRGZU__EKKO': 'String',
    'RLWRT__EKKO': 'Numeric',
    'EBELN__EKPO': 'String',
    'EBELP__EKPO': 'String',
    'LOEKZ__EKPO': 'String',
    'TXZ01__EKPO': 'String',
    'MATNR__EKPO': 'String',
    'WERKS__EKPO': 'String',
    'MATKL__EKPO': 'String',
    'MENGE__EKPO': 'Numeric',
    'MEINS__EKPO': 'String',
    'NETPR__EKPO': 'Numeric',
    'PEINH__EKPO': 'String',
    'NETWR__EKPO': 'Numeric',
    'BRTWR__EKPO': 'Numeric',
    'ELIKZ__EKPO': 'String',
    'PSTYP__EKPO': 'String',
    'LIFNR__LFA1': 'String',
    'NAME1__LFA1': 'String',
    'EBELN__EKET': 'String',
    'EBELP__EKET': 'String',
    'EINDT__EKET': 'Date',
    'SLFDT__EKET': 'Date',
    'MENGE__EKET': 'Numeric',
    'WEMNG__EKET': 'Numeric',
    'SPRAS__T052U': 'String',
    'ZTERM__T052U': 'String',
    'ZTAGG__T052U': 'String',
    'TEXT1__T052U': 'String',
    'SPRAS__T163Y': 'String',
    'PSTYP__T163Y': 'String',
    'PTEXT__T163Y': 'String',
    'EPSTP__T163Y': 'String',
    'KTOKK__LFA1': 'String',
    'AEDAT__EKPO': 'Date',
    'BUKRS__EKPO': 'String',
    'INFNR__EKPO': 'String',
    'BPRME__EKPO': 'String',
    'BPUMZ__EKPO': 'String',
    'BANFN__EKPO': 'String',
    'BNFPO__EKPO': 'String',
    'BANFN__EBAN': 'String',
    'BNFPO__EBAN': 'String',
    'LOEKZ__EBAN': 'String',
    'FRGKZ__EBAN': 'String',
    'FRGZU__EBAN': 'String',
    'FRGST__EBAN': 'String',
    'EKGRP__EBAN': 'String',
    'ERNAM__EBAN': 'String',
    'ERDAT__EBAN': 'Date',
    'AFNAM__EBAN': 'String',
    'TXZ01__EBAN': 'String',
    'MATNR__EBAN': 'String',
    'WERKS__EBAN': 'String',
    'LGORT__EBAN': 'String',
    'MATKL__EBAN': 'String',
    'MENGE__EBAN': 'Numeric',
    'BADAT__EBAN': 'Date',
    'LFDAT__EBAN': 'Date',
    'FRGDT__EBAN': 'Date',
    'PREIS__EBAN': 'Numeric',
    'PEINH__EBAN': 'String',
    'PSTYP__EBAN': 'String',
    'EBELN__EBAN': 'String',
    'EBELP__EBAN': 'String',
    'BEDAT__EBAN': 'Date',
    'BSMNG__EBAN': 'Numeric',
    'BNAME__USR21': 'String',
    'PERSNUMBER__USR21': 'String',
    'ADDRNUMBER__USR21': 'String',
    'ADDRNUMBER__ADCP': 'String',
    'PERSNUMBER__ADCP': 'String',
    'SO_KEY__ADCP': 'Date',
    'DEPARTMENT__ADCP': 'String',
    'FUNCTION__ADCP': 'String',
    'TEL_NUMBER__ADCP': 'String',
    'EBELN__EKBE': 'String',
    'EBELP__EKBE': 'String',
    'GJAHR__EKBE': 'String',
    'BELNR__EKBE': 'String',
    'BUZEI__EKBE': 'String',
    'BEWTP__EKBE': 'String',
    'BWART__EKBE': 'String',
    'BUDAT__EKBE': 'Date',
    'MENGE__EKBE': 'Numeric',
    'DMBTR__EKBE': 'Numeric',
    'WRBTR__EKBE': 'Numeric',
    'SHKZG__EKBE': 'String',
    'BWTAR__EKBE': 'String',
    'ELIKZ__EKBE': 'String',
    'XBLNR__EKBE': 'String',
    'LFBNR__EKBE': 'String',
    'LFPOS__EKBE': 'String',
    'CPUDT__EKBE': 'Date',
    'CPUTM__EKBE': 'Time',
    'MATNR__EKBE': 'String',
    'WERKS__EKBE': 'String',
    'MWSKZ__EKBE': 'String',
    'ERNAM__EKBE': 'String',
    'MWSKZ__EKPO': 'String',
    'LANGU__T5VS5': 'String',
    'LTKOD__T5VS5': 'String',
    'ATEXT__T5VS5': 'String',
    'LAND1__LFA1': 'String',
    'NAME2__LFA1': 'String',
    'ERDAT__LFA1': 'Date',
    'ERNAM__LFA1': 'String',
    'SPERR__LFA1': 'String',
    'SPERM__LFA1': 'String',
    'STCD1__LFA1': 'String',
    'STCD3__LFA1': 'String',
    'TELF1__LFA1': 'String',
    'TELF2__LFA1': 'String',
    'SPRAS__T077Y': 'String',
    'KTOKK__T077Y': 'String',
    'TXT30__T077Y': 'String',
    'SPRSL__TSTCT': 'String',
    'TCODE__TSTCT': 'String',
    'TTEXT__TSTCT': 'String',
    'OBJECTCLAS__CDHDR': 'String',
    'OBJECTID__CDHDR': 'String',
    'CHANGENR__CDHDR': 'String',
    'USERNAME__CDHDR': 'String',
    'UDATE__CDHDR': 'Date',
    'UTIME__CDHDR': 'String',
    'TCODE__CDHDR': 'String',
    'PLANCHNGNR__CDHDR': 'String',
    'ACT_CHNGNO__CDHDR': 'String',
    'WAS_PLANND__CDHDR': 'Numeric',
    'CHANGE_IND__CDHDR': 'String',
    'LANGU__CDHDR': 'String',
    'VERSION__CDHDR': 'String',
    'OBJECTCLAS__CDPOS': 'String',
    'OBJECTID__CDPOS': 'String',
    'CHANGENR__CDPOS': 'String',
    'TABNAME__CDPOS': 'String',
    'TABKEY__CDPOS': 'String',
    'FNAME__CDPOS': 'String',
    'CHNGIND__CDPOS': 'Numeric',
    'TEXT_CASE__CDPOS': 'String',
    'UNIT_OLD__CDPOS': 'Numeric',
    'UNIT_NEW__CDPOS': 'Numeric',
    'CUKY_OLD__CDPOS': 'String',
    'CUKY_NEW__CDPOS': 'String',
    'VALUE_NEW__CDPOS': 'String',
    'VALUE_OLD__CDPOS': 'String',
    'BUKRS__BKPF': 'String',
    'BELNR__BKPF': 'String',
    'GJAHR__BKPF': 'String',
    'BLART__BKPF': 'String',
    'BLDAT__BKPF': 'Date',
    'BUDAT__BKPF': 'Date',
    'CPUDT__BKPF': 'Date',
    'CPUTM__BKPF': 'Date',
    'AEDAT__BKPF': 'Date',
    'WWERT__BKPF': 'Date',
    'USNAM__BKPF': 'String',
    'TCODE__BKPF': 'String',
    'XBLNR__BKPF': 'String',
    'DBBLG__BKPF': 'String',
    'STBLG__BKPF': 'String',
    'STJAH__BKPF': 'String',
    'BKTXT__BKPF': 'String',
    'AWKEY__BKPF': 'String',
    'BUKRS__BSAK': 'String',
    'LIFNR__BSAK': 'String',
    'UMSKZ__BSAK': 'String',
    'AUGDT__BSAK': 'Date',
    'AUGBL__BSAK': 'String',
    'ZUONR__BSAK': 'String',
    'GJAHR__BSAK': 'String',
    'BELNR__BSAK': 'String',
    'BUZEI__BSAK': 'String',
    'BUDAT__BSAK': 'Date',
    'BLDAT__BSAK': 'Date',
    'CPUDT__BSAK': 'Date',
    'WAERS__BSAK': 'String',
    'XBLNR__BSAK': 'String',
    'BLART__BSAK': 'String',
    'MONAT__BSAK': 'String',
    'BSCHL__BSAK': 'String',
    'ZUMSK__BSAK': 'String',
    'SHKZG__BSAK': 'String',
    'MWSKZ__BSAK': 'String',
    'DMBTR__BSAK': 'Numeric',
    'WRBTR__BSAK': 'Numeric',
    'MWSTS__BSAK': 'Numeric',
    'WMWST__BSAK': 'Numeric',
    'SGTXT__BSAK': 'String',
    'SAKNR__BSAK': 'String',
    'HKONT__BSAK': 'String',
    'ZFBDT__BSAK': 'Date',
    'ZTERM__BSAK': 'String',
    'ZBD1T__BSAK': 'String',
    'ZBD2T__BSAK': 'String',
    'BUKRS__BSIK': 'String',
    'LIFNR__BSIK': 'String',
    'UMSKZ__BSIK': 'String',
    'AUGDT__BSIK': 'Date',
    'AUGBL__BSIK': 'String',
    'ZUONR__BSIK': 'String',
    'GJAHR__BSIK': 'String',
    'BELNR__BSIK': 'String',
    'BUZEI__BSIK': 'String',
    'BUDAT__BSIK': 'Date',
    'BLDAT__BSIK': 'Date',
    'CPUDT__BSIK': 'Date',
    'WAERS__BSIK': 'String',
    'XBLNR__BSIK': 'String',
    'BLART__BSIK': 'String',
    'MONAT__BSIK': 'String',
    'BSCHL__BSIK': 'String',
    'SHKZG__BSIK': 'String',
    'MWSKZ__BSIK': 'String',
    'DMBTR__BSIK': 'Numeric',
    'WRBTR__BSIK': 'Numeric',
    'MWSTS__BSIK': 'Numeric',
    'WMWST__BSIK': 'Numeric',
    'SGTXT__BSIK': 'String',
    'SAKNR__BSIK': 'String',
    'HKONT__BSIK': 'String',
    'ZFBDT__BSIK': 'Date',
    'ZTERM__BSIK': 'String',
    'ZBD1T__BSIK': 'String',
    'ZBD2T__BSIK': 'String',
    'SPRAS__T003T': 'String',
    'BLART__T003T': 'String',
    'LTEXT__T003T': 'String',
    'ORT01__LFA1': 'String',
    'PSTLZ__LFA1': 'String',
    'ADRNR__LFA1': 'String',
    'MCOD1__LFA1': 'String',
    'LNRZA__LFA1': 'String',
    'STCD2__LFA1': 'String',
    'SPERZ__LFA1': 'String',
    'LIFNR__LFBK': 'String',
    'CTRY__LFBK': 'String',
    'BANKS__LFBK': 'String',
    'BANKL__LFBK': 'String',
    'BANKN__LFBK': 'String',
    'PERNR__PA0002': 'String',
    'BEGDA__PA0002': 'Date',
    'ENDDA__PA0002': 'Date',
    'INITS__PA0002': 'String',
    'NACHN__PA0002': 'String',
    'NAME2__PA0002': 'String',
    'NACH2__PA0002': 'String',
    'VORNA__PA0002': 'String',
    'MIDNM__PA0002': 'String',
    'GESCH__PA0002': 'String',
    'GBDAT__PA0002': 'Date',
    'GBDEP__PA0002': 'String',
    'GBORT__PA0002': 'String',
    'NATIO__PA0002': 'String',
    'FAMST__PA0002': 'String',
    'FAMDT__PA0002': 'Date',
    'ANZKD__PA0002': 'String',
    'PERID__PA0002': 'String',
    'GBPAS__PA0002': 'Date',
    'RUFNM__PA0002': 'String',
    'GBLND__PA0002': 'String',
    'PERNR__PA0006': 'String',
    'BEGDA__PA0006': 'Date',
    'ENDDA__PA0006': 'Date',
    'SPRPS__PA0006': 'String',
    'SUBTY__PA0006': 'String',
    'NAME2__PA0006': 'String',
    'ANSSA__PA0006': 'String',
    'ORT01__PA0006': 'String',
    'ORT02__PA0006': 'String',
    'PSTLZ__PA0006': 'String',
    'LAND1__PA0006': 'String',
    'TELNR__PA0006': 'String',
    'LOCAT__PA0006': 'Date',
    'ADR03__PA0006': 'Date',
    'ADR04__PA0006': 'Date',
    'PERNR__PA0009': 'String',
    'WAERS__PA0009': 'String',
    'BANKS__PA0009': 'String',
    'BKONT__PA0009': 'String',
    'BANKN__PA0009': 'String',
    'STCD1__PA0009': 'String',
    'STCD2__PA0009': 'String',
    'ZWECK__PA0009': 'String',
    'REBZG__BSAK': 'String',
    'REBZG__BSIK': 'String',
    'STRAS__LFA1': 'String',
    'TELBX__LFA1': 'String',
    'TELFX__LFA1': 'String',
    'TELTX__LFA1': 'String',
    'TELX1__LFA1': 'String',
    'LIFNR__LFB1': 'String',
    'BUKRS__LFB1': 'String',
    'SPERR__LFB1': 'String',
    'ZWELS__LFB1': 'String',
    'ZAHLS__LFB1': 'String',
    'LIFNR__J_1IMOVEND': 'String',
    'J_1IPANNO__J_1IMOVEND': 'String',
    'J_1IPANREF__J_1IMOVEND': 'String',
    'SPRAS__T042ZT': 'String',
    'LAND1__T042ZT': 'String',
    'ZLSCH__T042ZT': 'String',
    'TEXT2__T042ZT': 'String',
    'BUKRS__BSEG': 'String',
    'BELNR__BSEG': 'String',
    'GJAHR__BSEG': 'String',
    'BUZEI__BSEG': 'String',
    'AUGDT__BSEG': 'Date',
    'AUGCP__BSEG': 'Date',
    'AUGBL__BSEG': 'String',
    'BSCHL__BSEG': 'String',
    'KOART__BSEG': 'String',
    'UMSKZ__BSEG': 'String',
    'UMSKS__BSEG': 'String',
    'SHKZG__BSEG': 'String',
    'MWSKZ__BSEG': 'String',
    'DMBTR__BSEG': 'Numeric',
    'WRBTR__BSEG': 'Numeric',
    'ZUONR__BSEG': 'String',
    'SGTXT__BSEG': 'String',
    'ALTKT__BSEG': 'String',
    'VORGN__BSEG': 'String',
    'KOKRS__BSEG': 'String',
    'KOSTL__BSEG': 'String',
    'SAKNR__BSEG': 'String',
    'HKONT__BSEG': 'String',
    'KUNNR__BSEG': 'String',
    'LIFNR__BSEG': 'String',
    'SPRAS__SKAT': 'String',
    'KTOPL__SKAT': 'String',
    'SAKNR__SKAT': 'String',
    'TXT20__SKAT': 'String',
    'TXT50__SKAT': 'String',
    'MCOD1__SKAT': 'String',
    'SPRAS__TBSLT': 'String',
    'BSCHL__TBSLT': 'String',
    'UMSKZ__TBSLT': 'String',
    'LTEXT__TBSLT': 'String',
    'BUKRS__BSAD': 'String',
    'KUNNR__BSAD': 'String',
    'UMSKS__BSAD': 'String',
    'UMSKZ__BSAD': 'String',
    'AUGDT__BSAD': 'Date',
    'AUGBL__BSAD': 'String',
    'ZUONR__BSAD': 'String',
    'GJAHR__BSAD': 'String',
    'BELNR__BSAD': 'String',
    'BUZEI__BSAD': 'String',
    'BUDAT__BSAD': 'Date',
    'BLDAT__BSAD': 'Date',
    'CPUDT__BSAD': 'Date',
    'WAERS__BSAD': 'String',
    'XBLNR__BSAD': 'String',
    'BLART__BSAD': 'String',
    'BSCHL__BSAD': 'String',
    'ZUMSK__BSAD': 'String',
    'SHKZG__BSAD': 'String',
    'GSBER__BSAD': 'String',
    'MWSKZ__BSAD': 'String',
    'DMBTR__BSAD': 'Numeric',
    'WRBTR__BSAD': 'Numeric',
    'MWSTS__BSAD': 'Numeric',
    'WMWST__BSAD': 'Numeric',
    'BDIFF__BSAD': 'String',
    'SGTXT__BSAD': 'String',
    'SAKNR__BSAD': 'String',
    'HKONT__BSAD': 'String',
    'ZFBDT__BSAD': 'Date',
    'ZBD1T__BSAD': 'String',
    'ZTERM__BSAD': 'String',
    'ZLSCH__BSAD': 'String',
    'BUKRS__BSID': 'String',
    'KUNNR__BSID': 'String',
    'UMSKS__BSID': 'String',
    'UMSKZ__BSID': 'String',
    'AUGDT__BSID': 'Date',
    'AUGBL__BSID': 'String',
    'ZUONR__BSID': 'String',
    'GJAHR__BSID': 'String',
    'BELNR__BSID': 'String',
    'BUZEI__BSID': 'String',
    'BUDAT__BSID': 'Date',
    'BLDAT__BSID': 'Date',
    'CPUDT__BSID': 'Date',
    'WAERS__BSID': 'String',
    'XBLNR__BSID': 'String',
    'BLART__BSID': 'String',
    'BSCHL__BSID': 'Date',
    'ZUMSK__BSID': 'String',
    'SHKZG__BSID': 'String',
    'MWSKZ__BSID': 'String',
    'DMBTR__BSID': 'Numeric',
    'WRBTR__BSID': 'Numeric',
    'MWSTS__BSID': 'Numeric',
    'WMWST__BSID': 'Numeric',
    'BDIFF__BSID': 'String',
    'SGTXT__BSID': 'String',
    'SAKNR__BSID': 'String',
    'HKONT__BSID': 'String',
    'ZFBDT__BSID': 'Date',
    'ZBD1T__BSID': 'String',
    'ZTERM__BSID': 'String',
    'ZLSCH__BSID': 'String',
    'KUNNR__KNA1': 'String',
    'LAND1__KNA1': 'String',
    'NAME1__KNA1': 'String',
    'ORT01__KNA1': 'String',
    'PSTLZ__KNA1': 'String',
    'STRAS__KNA1': 'String',
    'PERSNUMBER__ADRP': 'String',
    'NAME_FIRST__ADRP': 'String',
    'NAME_LAST__ADRP': 'String',
    'NAME2__ADRP': 'String',
    'NAME_TEXT__ADRP': 'String',
    'AGR_NAME__AGR_TCODES': 'String',
    'TYPE__AGR_TCODES': 'String',
    'TCODE__AGR_TCODES': 'String',
    'EXCLUDE__AGR_TCODES': 'String',
    'DIRECT__AGR_TCODES': 'String',
    'AGR_NAME__AGR_USERS': 'String',
    'UNAME__AGR_USERS': 'String',
    'ZTERM__LFB1': 'String',
    'OBJECT_CLASS__CDPOS': 'String',
    'MONAT__BKPF': 'String',
    'XCPDK__LFA1': 'String'}


# Parsing the zip folder files
def for_zip_folder(input_file, delimiter):
    folder_name = os.path.basename(input_file).split('.zip')[0]
    zip_file = []

    for f in os.listdir(os.path.join(os.path.dirname(__file__), folder_name)):
        file_path = os.path.join(os.path.dirname(__file__), folder_name, f)
        print('Reading', os.path.basename(file_path), 'from', os.path.basename(input_file))
        df = parse_files(file_path, delimiter=delimiter)
        df.columns = df.iloc[0]
        df = df[1:]
        zip_file.append(df)

    if len(zip_file) > 0:
        final_df = pd.concat(zip_file, ignore_index=True)
        last_row = final_df[-1:]
        final_df = final_df.shift(periods=1, axis=0)
        final_df.iloc[0] = final_df.columns
        final_df = final_df.append(last_row, ignore_index=True)
        final_df.columns = list(range(final_df.shape[1]))
        return final_df
    else:
        pass
    return None


# Parse different format files
def parse_files(input_file, delimiter=False):
    # Now input file can be .zip, .xlsx, .xlsb, .xls, .csv, .txt, .del
    if '.xlsx' in input_file:
        df = pd.read_excel(io=input_file, na_filter=False, header=None, skip_blank_lines=True)

    elif '.xlsb' in input_file:
        app = xw.App()
        book = xw.Book(input_file)
        sheet = book.sheets(book.sheets(1).name)
        df = sheet.range('A1').options(pd.DataFrame, expand='table').value.reset_index()
        df.fillna(value=pd.np.nan, inplace=True)
        df = df.replace([pd.np.nan, '-'], '', regex=False)
        last_row = df[-1:]
        df = df.shift(periods=1, axis=0)
        df.iloc[0] = df.columns
        df = df.append(last_row, ignore_index=True)
        df.columns = list(range(df.shape[1]))
        book.close()
        app.kill()

    elif '.xls' in input_file:
        df = pd.read_excel(io=input_file, na_filter=False, header=None, skip_blank_lines=True)

    elif '.csv' in input_file:
        print('Reading', os.path.basename(input_file), ' with delimiter', delimiter)
        with open(input_file, 'rb') as f:
            # Join binary lines for specified number of lines
            rawdata = f.read()

        encoding = chardet.detect(rawdata)['encoding']
        df = pd.read_csv(input_file, na_filter=False, header=None, skip_blank_lines=True, encoding=encoding, low_memory=False, sep=delimiter, skipinitialspace=True)

    elif '.txt' in input_file:
        print('Reading', os.path.basename(input_file), ' with delimiter', delimiter)
        with open(input_file, 'rb') as f:
            # Join binary lines for specified number of lines
            rawdata = f.read()

        encoding = chardet.detect(rawdata)['encoding']
        df = pd.read_csv(input_file, sep=delimiter, na_filter=False, header=None, skip_blank_lines=True, encoding=encoding, low_memory=False, skipinitialspace=True)

    elif '.del' in input_file:
        print('Reading', os.path.basename(input_file), ' with delimiter', delimiter)
        with open(input_file, 'rb') as f:
            # Join binary lines for specified number of lines
            rawdata = f.read()

        encoding = chardet.detect(rawdata)['encoding']
        df = pd.read_csv(input_file, sep=delimiter, na_filter=False, header=None, skip_blank_lines=True, encoding=encoding, low_memory=False, skipinitialspace=True)

    else:
        print('Cannot upload', input_file)
        raise ValueError('Cannot upload', input_file)
    return df


# For logging of Messages
def logMessage(logging, msg, isLog=False):
    if isLog:
        logging.log(msg)
        logging.debug(msg)
    else:
        logging.debug(msg)


# Initial logs wrote into outlog file
def log_inputs(logging, dataFields, fileFields, ThirdParameter, api):
    logging.debug("DataFields:-" + str(dataFields))
    logging.debug("FileFields:-" + str(fileFields))
    logging.debug("ThirdParameter:-" + str(ThirdParameter))
    logging.debug("API botFileName :-" + str(api.botFileName))
    logging.debug("API inputFiles :-" + str(api.inputFiles))
    logging.debug("API jobDirectoryPath :-" + str(api.jobDirectoryPath))

final_dict = {}


# Functional to technical mapping function
def functional_technical_map(data, logging, isLog=False):
    logMessage(logging, 'Performing Mapping', isLog)
    if data:
        try:
            for key, value in data.items():
                new_dict = {
                    'data': value['data'],
                    'date_format': value['date_format'],
                    'num_format': value['num_format']
                }

                final_dict[bot2_table_map[key.strip().lower()].strip().lower()] = new_dict
        except Exception as e:
            print('Functional to technical mapping error:', e)
    else:
        pass

    logMessage(logging, 'Mapping Done', isLog)
    return final_dict


# Technical to functional mapping function
def technical_functional_map(data, logging, isLog=False):
    logMessage(logging, 'Performing Reverse Mapping', isLog)
    try:
        df_columns = list(data.columns)
        for i in df_columns:
            if re.search("__", i.strip()):
                if len(i.strip().split('__')) == 2:
                    tech_name, file = i.strip().split('__')
                    new_dict = {v: k for k, v in bot2_technical_headers[file.strip().lower()].items()}
                    if new_dict[i.strip().upper()]:
                        data.rename(columns={i: new_dict[i.strip().upper()]}, inplace=True)
                    else:
                        pass

                elif len(i.strip().split('__')) == 3:
                    doc_type, tech_name, file = i.strip().split('__')
                    new_dict = {v: k for k, v in bot2_technical_headers[file.strip().lower()].items()}
                    search_name = '__'.join([tech_name, file])
                    if new_dict[search_name]:
                        data.rename(columns={i: doc_type.lower() + '_' + new_dict[search_name]}, inplace=True)
                    else:
                        pass

            else:
                pass

    except Exception as e:
        print('Technical to Functional mapping error:', e)
        exit()
    logMessage(logging, 'Reverse Mapping Done', isLog)
    return data


# Cleaning the excel data before processing the bot computation
def cleaning_data(dict, logging, isLog=False):
    print('Cleaning data')
    logMessage(logging, 'Cleaning data', isLog)
    tables_list = list(dict.keys())
    for i in tables_list:
        get_table = dict[i]
        get_table.rename(columns=lambda x: x.strip(), inplace=True)
        get_table = get_table.applymap(lambda x: x.strip() if type(x) == str else x)
        get_table = get_table.replace([np.nan, '-', '='], '', regex=False)
        dict[i] = get_table
    print('Data cleaned!!')
    logMessage(logging, 'Data cleaned!!', isLog)
    return dict


# Renaming of BSIK columns into BSAK columns names
def renaming_bsik_columns(bsak, bsik):
    bsak_columns = list(bsak.columns)
    bsik_columns = list(bsik.columns)
    bsak_first = []

    name1, file1 = bsak_columns[0].split('__')

    for j in bsak_columns:
        name1, file1 = j.split('__')
        bsak_first.append(name1)

    for i in bsik_columns:
        name2, file2 = i.split('__')

        if name2 in bsak_first:
            bsik.rename(columns={name2 + '__' + file2: name2 + '__' + file1}, inplace=True)
        else:
            pass

    return bsik


# Filtering the data on the basis of English only
def language_key_filter(table_name, field_name, language, starting_letter):
    lang_list = list(table_name[field_name].unique())
    modified_language_list = []
    language = language.strip().upper()
    starting_letter = starting_letter.strip().upper()
    for i in lang_list:
        if type(i) == str:
            modified_language_list.append(i.strip().upper())
        else:
            pass
    table_name[field_name] = table_name[field_name].apply(lambda x: x.strip().upper() if type(x) == str else x)
    if language in modified_language_list:
        table_name = table_name[table_name[field_name] == language].drop(columns=field_name, axis=1)
    else:
        table_name = table_name[table_name[field_name].str.startswith(starting_letter, na=False)].drop(columns=field_name, axis=1)

    return table_name


# Function checking the DATAISSUE
def checkPoint(df, msg):
    if df.shape[0] == 0:
        raise ValueError(msg)
    else:
        pass


# Change the columns values into their specific datatypes
def change_data_types(dict, bot2_req_fields, logging, isLog):
    print('Changing Data Types')
    logMessage(logging, 'Changing Data Types', isLog)
    tables_list = list(dict.keys())
    for i in tables_list:
        get_table = dict[i]['data']
        get_table_columns = list(get_table.columns)
        for j in get_table_columns:
            if j in bot2_req_fields:
                get_column_type = datatype_dict[j]
                print('Changing data type of', j, ' into', get_column_type)
                logMessage(logging, 'Changing data type of ' + str(j) + ' into ' + str(get_column_type), isLog)
                if get_column_type == 'String':
                    get_table[j] = get_table[j].apply(convert_field_string)
                elif get_column_type == 'Numeric':
                    get_table[j] = get_table[j].apply(lambda x: convert_field_num(x, dict[i]['num_format']))
                    get_table = get_table.replace([np.nan], '')
                    get_table = get_table[get_table[j].apply(type).isin([int, float])]
                elif get_column_type == 'Date':
                    get_table[j] = get_table[j].apply(lambda x: convert_field_date(x, dict[i]['date_format']))
                    get_table = get_table[get_table[j].apply(type).isin([datetime.date])]
                elif get_column_type == 'Time':
                    get_table[j] = get_table[j].apply(convert_field_time)
                    get_table = get_table[get_table[j].apply(type).isin([datetime.time])]
                elif get_column_type == 'DateTime':
                    get_table[j] = get_table[j].apply(convert_field_datetime)
                    get_table = get_table[get_table[j].apply(type).isin([datetime.datetime])]
                else:
                    pass
            else:
                pass

        dict[i] = get_table
    print('Data Types Changed!')
    logMessage(logging, 'Data Types Changed!', isLog)
    return dict


def convert_field_string(value):
    try:
        if type(value) not in [str, datetime.datetime, datetime.date]:
            return str(value)
        elif type(value) in [datetime.datetime, datetime.date]:
            return value.strftime('%d.%m.%Y')
        elif type(value) in [datetime.time]:
            return value.strftime('%H:%M:%S')
        else:
            return value.strip()
    except ValueError as e:
        print('Unable to convert', value, ' into time.')
        return value


def convert_field_num(value, num_format=False):
    try:
        if num_format in [False, '', None]:
            if type(value) == str:
                value = value.replace(',', '')
                return float(pd.to_numeric(value))

            elif type(value) in [int, float]:
                return float(pd.to_numeric(value))

            else:
                raise ValueError
        else:
            if type(value) == str:
                if num_format == '1,23,456.67':
                    value = value.replace(',', '')
                    return float(pd.to_numeric(value))

                elif num_format == '1.23.456,67':
                    value = value.replace('.', '')
                    value = value.replace(',', '.')
                    return float(pd.to_numeric(value))

                elif num_format == '123456.67':
                    return float(pd.to_numeric(value))

                else:
                    raise ValueError

            elif type(value) in [int, float]:
                return float(pd.to_numeric(value))

            else:
                raise ValueError

    except ValueError as e:
        print('Unable to convert ', value, ' into numeric format.', e)
        return ''

    except Exception as e:
        print('Exception raised ', e)
        return ''


def convert_field_date(value, date_format=False):
    try:
        if date_format in [False, '', None]:
            if type(value) == str:
                return datetime.datetime.strptime(value, '%d.%m.%Y').date()
            elif type(value) == datetime.datetime:
                return value.date()
            elif type(value) == datetime.date:
                return value
            else:
                raise ValueError

        else:
            if type(value) == str:
                if date_format == 'DD.MM.YYYY':
                    return datetime.datetime.strptime(value, '%d.%m.%Y').date()
                elif date_format == 'DD/MM/YYYY':
                    return datetime.datetime.strptime(value, '%d/%m/%Y').date()
                elif date_format == 'DD-MM-YYYY':
                    return datetime.datetime.strptime(value, '%d-%m-%Y').date()
                elif date_format == 'DD-Mon-YYYY':
                    return datetime.datetime.strptime(value, '%d-%b-%Y').date()
                elif date_format == 'DD-MM-YY':
                    return datetime.datetime.strptime(value, '%d-%m-%y').date()
                elif date_format == 'MM/DD/YYYY':
                    return datetime.datetime.strptime(value, '%m/%d/%Y').date()
                elif date_format == 'MM-DD-YYYY':
                    return datetime.datetime.strptime(value, '%m-%d-%Y').date()
                elif date_format == 'MM/DD/YY':
                    return datetime.datetime.strptime(value, '%m/%d/%y').date()
                elif date_format == 'YYYY-MM-DD':
                    return datetime.datetime.strptime(value, '%Y-%m-%d').date()
                elif date_format == 'YYYY/MM/DD':
                    return datetime.datetime.strptime(value, '%Y/%m/%d').date()
                elif date_format == 'YYYY/DD/MM':
                    return datetime.datetime.strptime(value, '%Y/%d/%m').date()
                elif date_format == 'YYYY-DD-MM':
                    return datetime.datetime.strptime(value, '%Y-%d-%m').date()
                else:
                    raise ValueError

            elif type(value) == datetime.datetime:
                return value.date()
            elif type(value) == datetime.date:
                return value
            else:
                raise ValueError

    except ValueError as e:
        print('Unable to convert', value, ' into date format.', date_format)
        return ''


def convert_field_time(value):
    try:
        if type(value) == str:
            return datetime.datetime.strptime(value, format='%H:%M:%S').time()
        elif type(value) == datetime.datetime:
            return value.time()
        elif type(value) == datetime.time():
            return value
        else:
            pass
    except ValueError as e:
        print('Unable to convert', value, ' into time format.')
        return value


def convert_field_datetime(value):
    try:
        if type(value) == str:
            return datetime.datetime.strptime(value, format='%d.%m.%Y %H:%M:%S')
        elif type(value) == datetime.datetime:
            return value
        else:
            pass
    except ValueError as e:
        print('Unable to convert', value, ' into datetime format.')
        return value


# Checks if the two columns of dataframes are compatilble for merging
def mergeChecker(df_A, df_B, list_fields):
    for i in list_fields:
        if df_A[i].dtype != df_B[i].dtype:
            if (df_A[i].dtype.kind == 'O') or (df_B[i].dtype.kind == 'O'):
                df_A = df_A.astype({i: 'object'})
                df_B = df_B.astype({i: 'object'})
            else:
                df_B = df_B.astype({i: df_A[i].dtype})
        else:
            pass
    return df_A, df_B


# Validates the filesData dictionary according to the bot
def validate_files(dict, mandatory, logging, isLog=False):
    print('Validating Files...')
    logMessage(logging, 'Validating Files', isLog)
    mandatory_tables = list(mandatory.keys())
    input_tables = list(dict.keys())

    optional_present = []

    for l in input_tables:
        if l not in mandatory_tables:
            optional_present.append(l)
        else:
            pass

    print('Validation done...')
    logMessage(logging, 'Validating done', isLog)
    return optional_present


# Convert the int or float back to number_format '1.23.456,67'
def num_format_a(value):
    try:
        is_negative = False
        if value < 0:
            is_negative = True
        else:
            is_negative = False

        a = str(abs(round(value, 2))).split('.')
        new_list = []
        if len(a) == 1:
            int_part = a[0]
            if len(int_part) > 3:
                new_list = [int_part[-3:]] + new_list
                int_part = a[0][:-3]

                while len(int_part) > 2:
                    new_list = [int_part[-2:]] + new_list
                    int_part = int_part[:-2]

                new_list = [int_part] + new_list

                if is_negative:
                    return '-' + '.'.join(new_list)

                else:
                    return '.'.join(new_list)
            else:
                if is_negative:
                    return '-' + ','.join(new_list)

                else:
                    return ','.join(new_list)

        elif len(a) == 2:
            int_part = a[0]
            if len(int_part) > 3:
                new_list = [int_part[-3:]] + new_list
                int_part = a[0][:-3]

                while len(int_part) > 2:
                    new_list = [int_part[-2:]] + new_list
                    int_part = int_part[:-2]

                new_list = [int_part] + new_list
                int_conv = '.'.join(new_list)

                if is_negative:
                    return '-' + ','.join([int_conv, a[1]])
                else:
                    return ','.join([int_conv, a[1]])

            else:
                if is_negative:
                    return '-' + ','.join(a)
                else:
                    return ','.join(a)

    except Exception as e:
        print('Unable to convert', value, ' back to number format 1.23.456,67')
        return value


# Convert the int or float back to number_format '1,23,456.67'
def num_format_b(value):
    try:
        is_negative = False
        if value < 0:
            is_negative = True
        else:
            is_negative = False

        a = str(abs(round(value, 2))).split('.')
        new_list = []
        if len(a) == 1:
            int_part = a[0]
            if len(int_part) > 3:
                new_list = [int_part[-3:]] + new_list
                int_part = a[0][:-3]

                while len(int_part) > 2:
                    new_list = [int_part[-2:]] + new_list
                    int_part = int_part[:-2]

                new_list = [int_part] + new_list

                if is_negative:
                    return '-' + ','.join(new_list)

                else:
                    return ','.join(new_list)
            else:
                if is_negative:
                    return '-' + '.'.join(new_list)

                else:
                    return '.'.join(new_list)

        elif len(a) == 2:
            int_part = a[0]
            if len(int_part) > 3:
                new_list = [int_part[-3:]] + new_list
                int_part = a[0][:-3]

                while len(int_part) > 2:
                    new_list = [int_part[-2:]] + new_list
                    int_part = int_part[:-2]

                new_list = [int_part] + new_list
                int_conv = ','.join(new_list)

                if is_negative:
                    return '-' + '.'.join([int_conv, a[1]])
                else:
                    return '.'.join([int_conv, a[1]])

            else:
                if is_negative:
                    return '-' + '.'.join(a)
                else:
                    return '.'.join(a)

    except Exception as e:
        print('Unable to convert', value, ' back to number format 1,23,456.67')
        return value


# Preparing the output which includes removing duplicates, output sequence, convert all DateTime format to string format
def prepare_output_file(output, output_sequence_columns, output_incode_columns, not_required_columns, date_format, num_format, logging, drop_duplicates=False, isLog=False):
    # Convert all datetime format into string format
    logMessage(logging, 'Preparing Output file', isLog)
    if date_format in [False, '', None]:
        date_format = '%d.%m.%Y'
    elif date_format == 'DD/MM/YYYY':
        date_format = '%d/%m/%Y'
    elif date_format == 'DD-MM-YYYY':
        date_format = '%d-%m-%Y'
    elif date_format == 'DD-Mon-YYYY':
        date_format = '%d-%b-%Y'
    elif date_format == 'DD-MM-YY':
        date_format = '%d-%m-%y'
    elif date_format == 'MM/DD/YYYY':
        date_format = '%m/%d/%Y'
    elif date_format == 'MM-DD-YYYY':
        date_format = '%m-%d-%Y'
    elif date_format == 'MM/DD/YY':
        date_format = '%m/%d/%y'
    elif date_format == 'YYYY-MM-DD':
        date_format = '%Y-%m-%d'
    elif date_format == 'YYYY/MM/DD':
        date_format = '%Y/%m/%d'
    elif date_format == 'YYYY/DD/MM':
        date_format = '%Y/%d/%m'
    elif date_format == 'YYYY-DD-MM':
        date_format = '%Y-%d-%m'
    else:
        date_format = '%d.%m.%Y'

    final_output = output.applymap(lambda x: x.strftime(date_format) if type(x) in [datetime.datetime, datetime.date, pd.Timestamp] else x)

    final_output = final_output.replace([np.nan], '')

    if num_format == '1.23.456,67':
        final_output = final_output.applymap(lambda x: num_format_a(x) if type(x) in [int, float] else x)
    elif num_format == '1,23,456.67':
        final_output = final_output.applymap(lambda x: num_format_b(x) if type(x) in [int, float] else x)
    else:
        pass

    output_columns = list(final_output.columns)
    final_column_sequence = []
    not_present = []
    for i in output_sequence_columns:
        if i not in not_required_columns:
            if i in output_columns:
                final_column_sequence.append(i)
            else:
                not_present.append(i)
        else:
            pass

    column_seq = final_column_sequence + output_incode_columns
    final_output_seq = final_output[column_seq]

    if drop_duplicates:
        final_output_seq.drop_duplicates(inplace=True)
    else:
        pass

    final_output_seq = final_output_seq.replace([np.nan, '-', '='], '', regex=False)
    logMessage(logging, 'Output file prepared', isLog)
    return final_output_seq


# Write output to directory
def write_output(output, output_file_name, logging, isLog=False):
    logMessage(logging, 'Writting Output File', isLog)
    script_dir = os.path.dirname(output_file_name)
    output_files = []
    if output.shape[0] > 50000:
        count = 0
        output_name = os.path.basename(output_file_name)
        num_of_chunks = (output.shape[0] // 50000) + 1
        list_dfs = np.array_split(output, num_of_chunks)
        for i in list_dfs:
            count += 1
            fullname = output_name + '_' + str(count) + '.xlsx'
            writer = pd.ExcelWriter(os.path.join(script_dir, fullname), engine='xlsxwriter')
            i.to_excel(excel_writer=writer, index=False, sheet_name="sheet_1", engine='xlsxwriter')
            output_files.append(os.path.join(script_dir, fullname))
            writer.save()
            writer.close()
    else:
        # Write output to output.xlsx file
        output_name = os.path.basename(output_file_name)
        fullname = output_name + '.xlsx'
        writer = pd.ExcelWriter(os.path.join(script_dir, fullname), engine='xlsxwriter')
        output.to_excel(excel_writer=writer, index=False, sheet_name="sheet_1", engine='xlsxwriter')
        output_files.append(os.path.join(script_dir, fullname))
        writer.save()
        writer.close()

    return output_files


# Zipping the folder
def zipping_folder(output_files, output_file_name, logging, isLog=False):
    logMessage(logging, 'Zipping Folder', isLog)
    script_dir = os.path.dirname(output_file_name)
    output_name = os.path.basename(output_file_name)
    zipObj = zipfile.ZipFile(os.path.join(script_dir, output_name + '.zip'), mode='w')
    for i in output_files:
        zipObj.write(i)
    zipObj.close()

    for i in output_files:
        os.remove(i)

    return output_file_name + '.zip'
