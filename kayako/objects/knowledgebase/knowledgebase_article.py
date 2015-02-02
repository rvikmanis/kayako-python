# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ravi Sharma
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Jan 28, 2014

@author: Ravi Sharma
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError


class KnowledgebaseArticle(KayakoObject):
	'''
	Knowledgebase Article API Object.

	contents              The content of the Article.
	contentstext          The contentstext of the Article.
	categories            The categories of the Article.
	creator               The creator staff.
	creatorid             The creator staff ID.
	author                The author of the Article.
	email                 The email of the Article creator.
	subject               The subject of the Article.
	isedited              1 or 0 boolean that controls whether or not to content of this article is edited.
	editeddateline        The edit timestamp of the Article.
	editedstaffid         Edited staff ID.
	views                 The views of the Article.
	isfeatured            1 or 0 boolean that controls whether or not to this article is a featured.
	allowcomments         1 or 0 boolean that controls whether or not comments are enable to this article.
	totalcomments         The number of comments on this article.
	hasattachments        1 or 0 boolean that controls whether or not article has attachments.
	attachments           The attachments of the Article.
	dateline              The creation time of the Article.
	articlestatus         The status of Article, 1 for published, 2 for draft..
	articlerating         The rating for the Article.
	ratinghits            The rating hits for the Article.
	ratingcount           The rating count for the Article.
	'''

	controller = '/Knowledgebase/Article'

	__parameters__ = ['id', 'kbarticleid', 'contents', 'contentstext', 'categories', 'creator', 'creatorid', 'author', 'email', 'subject', 'isedited', 'editeddateline', 'editedstaffid', 'views',
	                  'isfeatured', 'allowcomments', 'totalcomments', 'hasattachments', 'attachments', 'dateline', 'articlestatus', 'articlerating', 'ratinghits', 'ratingcount', 'categoryid']

	__required_add_parameters__ = ['subject', 'contents', 'creatorid']
	__add_parameters__ = ['subject', 'contents', 'creatorid', 'articlestatus', 'isfeatured', 'allowcomments', 'categoryid']

	__required_save_parameters__ = ['subject', 'contents', 'creatorid']
	__save_parameters__ = ['subject', 'contents', 'creatorid', 'articlestatus', 'isfeatured', 'allowcomments', 'categoryid']

	@classmethod
	def _parse_knowledgebase_article(cls, api, knowledgebase_article_tree):
		categories = []
		categories_node = knowledgebase_article_tree.find('categories')
		if categories_node is not None:
			for id_node in categories_node.findall('categoryid'):
				id = cls._get_int(id_node)
				categories.append(id)

		attachments = []
		attachments_node = knowledgebase_article_tree.find('attachments')
		if attachments_node is not None:
			for id_node in attachments_node.findall('attachment'):
				attachment_id = id_node.find('id');
				id = cls._get_string(attachment_id)
				attachments.append(id)

		params = dict(
			id=cls._get_int(knowledgebase_article_tree.find('kbarticleid')),
			kbarticleid=cls._get_int(knowledgebase_article_tree.find('kbarticleid')),
			contents=cls._get_string(knowledgebase_article_tree.find('contents')),
			contentstext=cls._get_string(knowledgebase_article_tree.find('contentext')),
			creator=cls._get_string(knowledgebase_article_tree.find('creator')),
			creatorid=cls._get_int(knowledgebase_article_tree.find('creatorid')),
			author=cls._get_string(knowledgebase_article_tree.find('author')),
			email=cls._get_string(knowledgebase_article_tree.find('email')),
			subject=cls._get_string(knowledgebase_article_tree.find('subject')),
			isedited=cls._get_boolean(knowledgebase_article_tree.find('isedited')),
			categories=categories,
			editeddateline=cls._get_date(knowledgebase_article_tree.find('editeddateline')),
			editedstaffid=cls._get_int(knowledgebase_article_tree.find('editedstaffid')),
			views=cls._get_int(knowledgebase_article_tree.find('views')),
			isfeatured=cls._get_boolean(knowledgebase_article_tree.find('isfeatured')),
			allowcomments=cls._get_boolean(knowledgebase_article_tree.find('allowcomments')),
			totalcomments=cls._get_boolean(knowledgebase_article_tree.find('totalcomments')),
			hasattachments=cls._get_boolean(knowledgebase_article_tree.find('hasattachments')),
			attachments=attachments,
			dateline=cls._get_date(knowledgebase_article_tree.find('dateline')),
			articlestatus=cls._get_boolean(knowledgebase_article_tree.find('articlestatus')),
			articlerating=cls._get_int(knowledgebase_article_tree.find('articlerating')),
			ratinghits=cls._get_int(knowledgebase_article_tree.find('ratinghits')),
			ratingcount=cls._get_int(knowledgebase_article_tree.find('ratingcount')),
		)
		return params

	def _update_from_response(self, knowledgebase_article_tree):
		categories_node = knowledgebase_article_tree.find('categories')
		if categories_node is not None:
			categories = []
			for id_node in categories_node.findall('categoryid'):
				id = self._get_int(id_node)
				categories.append(id)
			self.categories = categories

		for int_node in ['kbarticleid', 'creatorid', 'editedstaffid', 'articlerating', 'ratinghits', 'ratingcount', 'views']:
			node = knowledgebase_article_tree.find(int_node)
			if node is not None:
				setattr(self, int_node, self._get_int(node, required=False))

		for str_node in ['contents', 'contentext', 'creator', 'author', 'email', 'subject']:
			node = knowledgebase_article_tree.find(str_node)
			if node is not None:
				setattr(self, str_node, self._get_string(node))

		for bool_node in ['isedited', 'isfeatured', 'allowcomments', 'totalcomments', 'hasattachments', 'articlestatus']:
			node = knowledgebase_article_tree.find(bool_node)
			if node is not None:
				setattr(self, bool_node, self._get_boolean(node, required=False))

	@classmethod
	def get_all(cls, api, categoryid, count=100, start=0):
		response = api._request('%s/ListAll/%s/%s/%s' % (cls.controller, categoryid, count, start), 'GET')
		tree = etree.parse(response)
		return [KnowledgebaseArticle(api, **cls._parse_knowledgebase_article(api, knowledgebase_article_tree)) for knowledgebase_article_tree in tree.findall('kbarticle')]

	@classmethod
	def get(cls, api, id):
		response = api._request('%s/%s/' % (cls.controller, id), 'GET')
		tree = etree.parse(response)
		node = tree.find('kbarticle')
		if node is None:
			return None
		params = cls._parse_knowledgebase_article(api, node)
		return KnowledgebaseArticle(api, **params)

	def add(self):
		'''
		Add this article.

		Requires:
			contents         The content of the Article.
			subject          The subject of the Article.
			creatorid        The creator staff ID.
		Optional:
			contentstext          The contentstext of the Article.
			categories            The categories of the Article.
			creator               The creator staff.
			author                The author of the Article.
			email                 The email of the Article creator.
			isedited              1 or 0 boolean that controls whether or not to content of this article is edited.
			editeddateline        The edit timestamp of the Article.
			editedstaffid         Edited staff ID.
			views                 The views of the Article.
			isfeatured            1 or 0 boolean that controls whether or not to this article is a featured.
			allowcomments         1 or 0 boolean that controls whether or not comments are enable to this article.
			totalcomments         The number of comments on this article.
			hasattachments        1 or 0 boolean that controls whether or not article has attachments.
			attachments           The attachments of the Article.
			dateline              The creation time of the Article.
			articlestatus         The status of Article, 1 for published, 2 for draft..
			articlerating         The rating for the Article.
			ratinghits            The rating hits for the Article.
			ratingcount           The rating count for the Article.
		'''
		if self.id is not UnsetParameter:
			raise KayakoRequestError('Cannot add a pre-existing %s. Use save instead. (id: %s)' % (self.__class__.__name__, self.id))

		parameters = self.add_parameters
		for required_parameter in self.__required_add_parameters__:
			if required_parameter not in parameters:
				raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

		response = self.api._request(self.controller, 'POST', **parameters)
		tree = etree.parse(response)
		node = tree.find('kbarticle')
		self._update_from_response(node)

	def save(self):
		response = self._save('%s/%s/' % (self.controller, self.id))
		tree = etree.parse(response)
		node = tree.find('kbarticle')
		self._update_from_response(node)

	def delete(self):
		self._delete('%s/%s/' % (self.controller, self.id))

	def __str__(self):
		return '<KnowledgebaseArticle (%s): %s>' % (self.kbarticleid, self.contents)