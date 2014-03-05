# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Feb 26, 2014

@author: ravi
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError


class CustomField(KayakoObject):
	'''
    Kayako Custom Field API Object.

    customfieldid         The custom field ID.
    customfieldgroupid    The custom field group id.
    title                 The title of the custom field.
    fieldtype             The type of the custom field.
    fieldname             The field name of custom field.
    defaultvalue          The default value of custom field.
    isrequired            1 or 0 boolean that controls whether or not field required.
    usereditable          1 or 0 boolean that controls whether or not to edit the field by user.
    staffeditable         1 or 0 boolean that controls whether or not to edit the field by staff.
    regexpvalidate        A regex string for validate.
    displayorder          The display order of the custom field.
    encryptindb           1 or 0 boolean that controls whether or not field is encrypted.
    description           The description of the custom field.
    '''

	controller = '/Base/CustomField'

	__parameters__ = [
		'id',
		'customfieldid',
		'customfieldgroupid',
		'title',
		'fieldtype',
		'fieldname',
		'defaultvalue',
		'isrequired',
		'usereditable',
		'staffeditable',
		'regexpvalidate',
		'displayorder',
		'encryptindb',
		'description',
	]

	@classmethod
	def _parse_custom_field(cls, custom_field_tree):
		params = dict(
			id=custom_field_tree.get('customfieldid'),
			customfieldid=id,
			customfieldgroupid=cls._parse_int(custom_field_tree.get('customfieldgroupid')),
			title=custom_field_tree.get('title'),
			fieldtype=cls._parse_int(custom_field_tree.get('fieldtype')),
			fieldname=custom_field_tree.get('fieldname'),
			defaultvalue=custom_field_tree.get('defaultvalue'),
			isrequired=cls._parse_int(custom_field_tree.get('isrequired')),
			usereditable=cls._parse_int(custom_field_tree.get('usereditable')),
			staffeditable=cls._parse_int(custom_field_tree.get('staffeditable')),
			regexpvalidate=custom_field_tree.get('regexpvalidate'),
			displayorder=cls._parse_int(custom_field_tree.get('displayorder')),
			encryptindb=cls._parse_int(custom_field_tree.get('encryptindb')),
			description=custom_field_tree.get('description'),
		)
		return params

	@classmethod
	def get_all(cls, api):
		response = api._request('%s' % (cls.controller), 'GET')
		tree = etree.parse(response)
		return [CustomField(api, **cls._parse_custom_field(custom_field_tree)) for custom_field_tree in tree.findall('customfield')]

	@classmethod
	def get(cls, api, customfieldid):
		response = api._request('%s/ListOptions/%s/' % (cls.controller, customfieldid), 'GET')
		tree = etree.parse(response)
		node = tree.find('option')
		if node is None:
			return None
		params = cls._parse_custom_field(node)
		return CustomField(api, **params)

	def __str__(self):
		return '<CustomField (%s): %s>' % (self.id, self.fieldname)
