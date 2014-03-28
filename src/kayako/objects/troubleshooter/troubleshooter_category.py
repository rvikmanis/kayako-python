# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Feb 11, 2014

@author: Ravi Sharma
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError


class TroubleshooterCategory(KayakoObject):
	'''
	Troubleshooter Category API Object.

	id                      The unique numeric identifier of the category.
	title                   The title of the Category.
	staffid                 The staff ID.
	displayorder            The display order.
	description             The category description.
	uservisibilitycustom    The user visibility custom. 0 or 1.
	usergroupidlist         The restricted user group ID list. Multiple values comma separated like 1,2,3.
	staffvisibilitycustom   The staff visibility custom. 0 or 1.
	staffgroupidlist        The restricted staff group ID list. Multiple values comma separated like 1,2,3.
	categorytype            The category type. Global: 1, public: 2, private: 3.
	views                   The views.
	visibilitytype          The visibility type.
	'''

	controller = '/Troubleshooter/Category'

	__parameters__ = ['id', 'staffid', 'staffname', 'title', 'description', 'categorytype', 'displayorder', 'views', 'uservisibilitycustom', 'usergroupidlist', 'staffvisibilitycustom',
	                  'staffgroupidlist', 'newsitemcount', 'visibilitytype']

	__required_add_parameters__ = ['title', 'categorytype', 'staffid']
	__add_parameters__ = ['title', 'categorytype', 'staffid', 'displayorder', 'description', 'uservisibilitycustom', 'usergroupidlist', 'staffvisibilitycustom', 'staffgroupidlist']

	__required_save_parameters__ = ['title', 'categorytype', 'staffid']
	__save_parameters__ = ['title', 'categorytype', 'staffid', 'displayorder', 'description', 'uservisibilitycustom', 'usergroupidlist', 'staffvisibilitycustom', 'staffgroupidlist']


	@classmethod
	def _parse_troubleshooter_category(cls, api, troubleshooter_category_tree):

		usergroupids = []
		usergroupids_node = troubleshooter_category_tree.find('usergroupidlist')
		if usergroupids_node is not None:
			for id_node in usergroupids_node.findall('usergroupidlist'):
				id = cls._get_int(id_node)
				usergroupids.append(id)

		staffgroupids = []
		staffgroup_node = troubleshooter_category_tree.find('staffgroupidlist')
		if staffgroup_node is not None:
			for id_node in staffgroup_node.findall('staffgroupidlist'):
				id = cls._get_int(id_node)
				staffgroupids.append(id)

		params = dict(
			id=cls._get_int(troubleshooter_category_tree.find('id')),
			staffid=cls._get_int(troubleshooter_category_tree.find('staffid')),
			staffname=cls._get_string(troubleshooter_category_tree.find('staffname')),
			title=cls._get_string(troubleshooter_category_tree.find('title')),
			description=cls._get_string(troubleshooter_category_tree.find('description')),
			categorytype=cls._get_int(troubleshooter_category_tree.find('categorytype')),
			displayorder=cls._get_int(troubleshooter_category_tree.find('displayorder')),
			views=cls._get_int(troubleshooter_category_tree.find('views')),
			uservisibilitycustom=cls._get_boolean(troubleshooter_category_tree.find('uservisibilitycustom')),
			usergroupidlist=usergroupids,
			staffvisibilitycustom=cls._get_boolean(troubleshooter_category_tree.find('staffvisibilitycustom')),
			staffgroupidlist=staffgroupids,
		)
		return params

	def _update_from_response(self, troubleshooter_category_tree):

		for int_node in ['id', 'staffid', 'categorytype', 'displayorder', 'views']:
			node = troubleshooter_category_tree.find(int_node)
			if node is not None:
				setattr(self, int_node, self._get_int(node, required=False))

		for str_node in ['staffname', 'title', 'description']:
			node = troubleshooter_category_tree.find(str_node)
			if node is not None:
				setattr(self, str_node, self._get_string(node))

		for bool_node in ['uservisibilitycustom', 'staffvisibilitycustom']:
			node = troubleshooter_category_tree.find(bool_node)
			if node is not None:
				setattr(self, bool_node, self._get_boolean(node, required=False))

	@classmethod
	def get_all(cls, api):
		response = api._request('%s/' % (cls.controller), 'GET')
		tree = etree.parse(response)
		return [TroubleshooterCategory(api, **cls._parse_troubleshooter_category(api, troubleshooter_category_tree)) for troubleshooter_category_tree in tree.findall('troubleshootercategory')]

	@classmethod
	def get(cls, api, id):
		response = api._request('%s/%s/' % (cls.controller, id), 'GET')
		tree = etree.parse(response)
		node = tree.find('troubleshootercategory')
		if node is None:
			return None
		params = cls._parse_troubleshooter_category(api, node)
		return TroubleshooterCategory(api, **params)

	def add(self):
		'''
		Add this TroubleshooterCategory.
			displayorder            The display order.
			description             The category description.
			uservisibilitycustom    The user visibility custom. 0 or 1
			usergroupidlist         The restricted user group ID list. Multiple values comma separated like 1,2,3.
			staffvisibilitycustom   The staff visibility custom. 0 or 1
			staffgroupidlist        The restricted staff group ID list. Multiple values comma separated like 1,2,3.

		Requires:
			title                   The category title.
			categorytype            The category type. Global: 1, public: 2, private: 3
			staffid                 The staff ID.
		'''
		response = self._add(self.controller)
		tree = etree.parse(response)
		node = tree.find('troubleshootercategory')
		self._update_from_response(node)

	def save(self):
		response = self._save('%s/%s/' % (self.controller, self.id))
		tree = etree.parse(response)
		node = tree.find('troubleshootercategory')
		self._update_from_response(node)

	def delete(self):
		self._delete('%s/%s/' % (self.controller, self.id))

	def __str__(self):
		return '<TroubleshooterCategory (%s): %s>' % (self.id, self.title)