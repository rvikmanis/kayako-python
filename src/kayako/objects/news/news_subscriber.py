# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Feb 6, 2014

@isvalidated: Ravi Sharma
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError


class NewsSubscriber(KayakoObject):
	'''
	News Item API Object.

	id                    The unique numeric identifier of the news item.
	tgroupid              The template group id.
	userid                The user id of a subscriber.
	email                 The email of a subscriber.
	isvalidated           The subscriber is validated. 0 or 1.
	usergroupid           The user group id.
	'''

	controller = '/News/Subscriber'

	__parameters__ = ['id', 'tgroupid', 'userid', 'email', 'isvalidated', 'usergroupid']

	__required_add_parameters__ = ['email']
	__add_parameters__ = ['isvalidated', 'email']

	__required_save_parameters__ = ['email']
	__save_parameters__ = ['isvalidated', 'email']

	@classmethod
	def _parse_news_subscriber(cls, api, news_subscriber_tree):

		params = dict(
			id=cls._get_int(news_subscriber_tree.find('id')),
			tgroupid=cls._get_int(news_subscriber_tree.find('tgroupid')),
			userid=cls._get_int(news_subscriber_tree.find('userid')),
			email=cls._get_string(news_subscriber_tree.find('email')),
			isvalidated=cls._get_boolean(news_subscriber_tree.find('isvalidated')),
			usergroupid=cls._get_int(news_subscriber_tree.find('usergroupid')),
		)
		return params


	def _update_from_response(self, news_subscriber_tree):

		for int_node in ['id', 'tgroupid', 'userid', 'usergroupid']:
			node = news_subscriber_tree.find(int_node)
			if node is not None:
				setattr(self, int_node, self._get_int(node, required=False))

		for str_node in ['email']:
			node = news_subscriber_tree.find(str_node)
			if node is not None:
				setattr(self, str_node, self._get_string(node))

		for bool_node in ['isvalidated']:
			node = news_subscriber_tree.find(bool_node)
			if node is not None:
				setattr(self, bool_node, self._get_boolean(node, required=False))

	@classmethod
	def get_all(cls, api):
		response = api._request('%s' % (cls.controller), 'GET')
		tree = etree.parse(response)
		return [NewsSubscriber(api, **cls._parse_news_subscriber(api, news_subscriber_tree)) for news_subscriber_tree in tree.findall('newssubscriber')]


	@classmethod
	def get(cls, api, id):
		response = api._request('%s/%s/' % (cls.controller, id), 'GET')
		tree = etree.parse(response)
		node = tree.find('newssubscriber')
		if node is None:
			return None
		params = cls._parse_news_subscriber(api, node)
		return NewsSubscriber(api, **params)

	def add(self):
		parameters = self.add_parameters

		for required_parameter in self.__required_add_parameters__:
			if required_parameter not in parameters:
				raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

		response = self.api._request(self.controller, 'POST', **parameters)
		tree = etree.parse(response)
		node = tree.find('newssubscriber')
		self._update_from_response(node)

	def save(self):
		response = self._save('%s/%s/' % (self.controller, self.id))
		tree = etree.parse(response)
		node = tree.find('newssubscriber')
		self._update_from_response(node)


	def delete(self):
		self._delete('%s/%s/' % (self.controller, self.id))


	def __str__(self):
		return '<NewsSubscriber (%s): %s>' % (self.id, self.email)