# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Feb 5, 2014

@author: Ravi Sharma
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError


class NewsItem(KayakoObject):
	'''
	News Item API Object.

	id                    The unique numeric identifier of the news item.
	staffid               The creator staff ID.
	newstype              The type of the News.
	newsstatus            The news status. Draft: 1, published: 2.
	fromname              The custom from name used in email notification.
	email                 The custom from email used in email notification.
	customemailsubject    The custom subject used in email notification.
	sendemail             Whether to send email notification. 0 or 1.
	allowcomments         Allow comments. 0 or 1.
	uservisibilitycustom  The user visibility custom. 0 or 1.
	usergroupidlist       The user group ID list. Multiple values comma separated like 1,2,3
	staffvisibilitycustom The staff visibility custom. 0 or 1.
	staffgroupidlist      The staff group id list. Multiple values comma separated like 1,2,3.
	expiry                The expiry date in m/d/Y format.
	newscategoryidlist    The category ID list. Multiple values comma separated like 1,2,3.
	'''

	controller = '/News/NewsItem'

	__parameters__ = ['id', 'staffid', 'newstype', 'newsstatus', 'author', 'email', 'subject', 'emailsubject', 'dateline', 'expiry', 'issynced', 'totalcomments', 'uservisibilitycustom',
	                  'usergroupidlist', 'staffvisibilitycustom', 'staffgroupidlist', 'allowcomments', 'contents', 'categories', 'fromname', 'customemailsubject', 'sendemail', 'newscategoryidlist']

	__required_add_parameters__ = ['subject', 'contents', 'staffid']
	__add_parameters__ = ['subject', 'contents', 'staffid', 'newstype', 'newsstatus', 'fromname', 'email', 'customemailsubject', 'sendemail', 'allowcomments', 'uservisibilitycustom',
	                      'usergroupidlist', 'staffvisibilitycustom', 'staffgroupidlist', 'expiry', 'newscategoryidlist']

	__required_save_parameters__ = ['subject', 'contents', 'staffid']
	__save_parameters__ = ['subject', 'contents', 'staffid', 'newstype', 'newsstatus', 'fromname', 'email', 'customemailsubject', 'sendemail', 'allowcomments', 'uservisibilitycustom',
	                       'usergroupidlist', 'staffvisibilitycustom', 'staffgroupidlist', 'expiry', 'newscategoryidlist']

	@classmethod
	def _parse_news_item(cls, api, news_item_tree):
		usergroups = []
		usergroup_node = news_item_tree.find('usergroupidlist')
		if usergroup_node is not None:
			for id_node in usergroup_node.findall('usergroupid'):
				id = cls._get_int(id_node)
				usergroups.append(id)

		staffgroups = []
		staffgroup_node = news_item_tree.find('staffgroupidlist')
		if staffgroup_node is not None:
			for id_node in staffgroup_node.findall('staffgroupid'):
				id = cls._get_int(id_node)
				staffgroups.append(id)

		categorylist = []
		category_node = news_item_tree.find('categories')
		if category_node is not None:
			for id_node in category_node.findall('categoryid'):
				id = cls._get_int(id_node)
				categorylist.append(id)

		params = dict(
			id=cls._get_int(news_item_tree.find('id')),
			staffid=cls._get_int(news_item_tree.find('staffid')),
			newstype=cls._get_int(news_item_tree.find('newstype')),
			newsstatus=cls._get_int(news_item_tree.find('newsstatus')),
			author=cls._get_string(news_item_tree.find('author')),
			email=cls._get_string(news_item_tree.find('email')),
			subject=cls._get_string(news_item_tree.find('subject')),
			emailsubject=cls._get_string(news_item_tree.find('emailsubject')),
			dateline=cls._get_date(news_item_tree.find('dateline')),
			expiry=cls._get_boolean(news_item_tree.find('expiry')),
			issynced=cls._get_boolean(news_item_tree.find('issynced')),
			totalcomments=cls._get_int(news_item_tree.find('totalcomments')),
			uservisibilitycustom=cls._get_int(news_item_tree.find('uservisibilitycustom')),
			usergroupidlist=usergroups,
			staffvisibilitycustom=cls._get_int(news_item_tree.find('staffvisibilitycustom')),
			staffgroupidlist=staffgroups,
			allowcomments=cls._get_boolean(news_item_tree.find('allowcomments')),
			contents=cls._get_string(news_item_tree.find('contents')),
			categories=categorylist,
		)
		return params


	def _update_from_response(self, news_item_tree):
		usergroups = []
		usergroup_node = news_item_tree.find('usergroupidlist')
		if usergroup_node is not None:
			for id_node in usergroup_node.findall('usergroupid'):
				id = cls._get_int(id_node)
				usergroups.append(id)

		staffgroups = []
		staffgroup_node = news_item_tree.find('staffgroupidlist')
		if staffgroup_node is not None:
			for id_node in staffgroup_node.findall('staffgroupid'):
				id = cls._get_int(id_node)
				staffgroups.append(id)

		categorylist = []
		category_node = news_item_tree.find('categories')
		if category_node is not None:
			for id_node in category_node.findall('categoryid'):
				id = cls._get_int(id_node)
				categorylist.append(id)

		for int_node in ['id', 'staffid', 'newstype', 'newsstatus', 'totalcomments', 'uservisibilitycustom', 'staffvisibilitycustom']:
			node = news_item_tree.find(int_node)
			if node is not None:
				setattr(self, int_node, self._get_int(node, required=False))

		for str_node in ['author', 'email', 'subject', 'emailsubject', 'contents']:
			node = news_item_tree.find(str_node)
			if node is not None:
				setattr(self, str_node, self._get_string(node))

		for bool_node in ['expiry', 'issynced', 'allowcomments']:
			node = news_item_tree.find(bool_node)
			if node is not None:
				setattr(self, bool_node, self._get_boolean(node, required=False))

		for date_node in ['dateline']:
			node = news_item_tree.find(date_node)
			if node is not None:
				setattr(self, date_node, self._get_date(node, required=False))


	@classmethod
	def get_all(cls, api, categoryid):
		response = api._request('%s/ListAll/%s' % (cls.controller, categoryid), 'GET')
		tree = etree.parse(response)
		return [NewsItem(api, **cls._parse_news_item(api, news_item_tree)) for news_item_tree in tree.findall('newsitem')]


	@classmethod
	def get(cls, api, id):
		response = api._request('%s/%s/' % (cls.controller, id), 'GET')
		tree = etree.parse(response)
		node = tree.find('newsitem')
		if node is None:
			return None
		params = cls._parse_news_item(api, node)
		return NewsItem(api, **params)

	def add(self):
		parameters = self.add_parameters

		for required_parameter in self.__required_add_parameters__:
			if required_parameter not in parameters:
				raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

		response = self.api._request(self.controller, 'POST', **parameters)
		tree = etree.parse(response)
		node = tree.find('newsitem')
		self._update_from_response(node)

	def save(self):
		response = self._save('%s/%s/' % (self.controller, self.id))
		tree = etree.parse(response)
		node = tree.find('newsitem')
		self._update_from_response(node)


	def delete(self):
		self._delete('%s/%s/' % (self.controller, self.id))


	def __str__(self):
		return '<NewsItem (%s): %s>' % (self.id, self.contents)