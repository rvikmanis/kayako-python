# -*- coding: utf-8 -*-
'''
Created on May 10, 2011

@author: evan
'''

from kayako.tests import KayakoAPITest

class TestTicketAttachment(KayakoAPITest):

    SUBJECT = 'DELETEME'

    def tearDown(self):
        from kayako.objects import Department, Ticket
        dept = self.api.first(Department, module='tickets')
        test_tickets = self.api.filter(Ticket, args=(dept.id,), subject=self.SUBJECT)
        for ticket in test_tickets:
            ticket.delete()
        super(TestTicketAttachment, self).tearDown()

    def test_get_nonexistant(self):
        from kayako.objects import Department, Ticket, TicketAttachment
        api = self.api

        dept = api.first(Department, module='tickets')

        ticket = api.create(Ticket)
        ticket.subject = self.SUBJECT
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = dept.id
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1
        ticket.userid = 1
        ticket.ownerstaffid = 1
        ticket.type = 'default'
        ticket.add()

        obj = api.get(TicketAttachment, ticket.id, 'abc123')

        ticket.delete()

        assert obj is None

    def test_add_get(self):
        from kayako.objects import Department, Ticket, TicketAttachment, TicketPost, User

        api = self.api

        depts = api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        user = api.get(User, 0)

        ticket = api.create(Ticket)
        ticket.subject = self.SUBJECT
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = dept.id
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1
        ticket.userid = user.id
        ticket.ownerstaffid = user.id
        ticket.type = 'default'
        ticket.add()

        ticket_post = api.create(TicketPost)
        ticket_post.ticketid = ticket.id
        ticket_post.subject = 'test_post'
        ticket_post.contents = 'testing a post'
        ticket_post.userid = user.id
        ticket_post.add()

        ticket_attachment = api.create(TicketAttachment)
        ticket_attachment.ticketid = ticket.id
        ticket_attachment.ticketpostid = ticket_post.id
        ticket_attachment.filename = 'test_file.txt'
        ticket_attachment.set_contents('this is just a test')
        ticket_attachment.add()

        obj2 = api.get(TicketAttachment, ticket.id, ticket_attachment.id)

        ticket_attachment.delete()
        ticket_post.delete()
        ticket.delete()
        assert obj2 is not None


    def test_get_all(self):
        from kayako.objects import Department, Ticket, TicketAttachment, TicketPost, User

        api = self.api

        depts = api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        user = api.get(User, 0)

        ticket = api.create(Ticket)
        ticket.subject = self.SUBJECT
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = dept.id
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1
        ticket.userid = user.id
        ticket.ownerstaffid = user.id
        ticket.type = 'default'
        ticket.add()

        ticket_post = api.create(TicketPost)
        ticket_post.ticketid = ticket.id
        ticket_post.subject = 'test_post'
        ticket_post.contents = 'testing a post'
        ticket_post.userid = user.id
        ticket_post.add()

        ticket_attachment = api.create(TicketAttachment)
        ticket_attachment.ticketid = ticket.id
        ticket_attachment.ticketpostid = ticket_post.id
        ticket_attachment.filename = 'test_file.txt'
        ticket_attachment.set_contents('this is just a test')
        ticket_attachment.add()

        result = self.api.get_all(TicketAttachment, ticket.id)
        assert isinstance(result, list)
        assert result[0].get_contents() is None # Contents don't load w/ get_all

        ticket_attachment.delete()
        ticket_post.delete()
        ticket.delete()

    def test_get_ticket_attachment(self):
        from kayako.objects import Department, Ticket, TicketAttachment, TicketPost, User

        api = self.api

        depts = api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        user = api.get(User, 0)

        ticket = api.create(Ticket)
        ticket.subject = self.SUBJECT
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = dept.id
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1
        ticket.userid = user.id
        ticket.ownerstaffid = user.id
        ticket.type = 'default'
        ticket.add()

        ticket_post = api.create(TicketPost)
        ticket_post.ticketid = ticket.id
        ticket_post.subject = 'test_post'
        ticket_post.contents = 'testing a post'
        ticket_post.userid = user.id
        ticket_post.add()

        ticket_attachment = api.create(TicketAttachment)
        ticket_attachment.ticketid = ticket.id
        ticket_attachment.ticketpostid = ticket_post.id
        ticket_attachment.filename = 'test_file.txt'
        ticket_attachment.set_contents('this is just a test')
        ticket_attachment.add()

        result = self.api.get(TicketAttachment, ticket.id, ticket_attachment.id)
        assert result.id == ticket_attachment.id
        assert result.get_contents() == 'this is just a test'

        assert 'TicketAttachment ' in str(result)

        ticket_attachment.delete()
        ticket_post.delete()
        ticket.delete()

    def test_add_missing_ticketid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketAttachment

        ticket_attachment = self.api.create(TicketAttachment)

        ticket_attachment.ticketpostid = 1
        ticket_attachment.filename = 'test_file.txt'
        ticket_attachment.set_contents('this is just a test')

        self.assertRaises(KayakoRequestError, ticket_attachment.add)

    def test_add_missing_ticketpostid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketAttachment

        ticket_attachment = self.api.create(TicketAttachment)

        ticket_attachment.ticketid = 1
        ticket_attachment.filename = 'test_file.txt'
        ticket_attachment.set_contents('this is just a test')

        self.assertRaises(KayakoRequestError, ticket_attachment.add)

    def test_add_missing_filename(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketAttachment

        ticket_attachment = self.api.create(TicketAttachment)

        ticket_attachment.ticketid = 1
        ticket_attachment.ticketpostid = 1
        ticket_attachment.set_contents('this is just a test')

        self.assertRaises(KayakoRequestError, ticket_attachment.add)

    def test_add_missing_contents(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketAttachment

        ticket_attachment = self.api.create(TicketAttachment)

        ticket_attachment.ticketid = 1
        ticket_attachment.ticketpostid = 1
        ticket_attachment.filename = 'test_file.txt'

        self.assertRaises(KayakoRequestError, ticket_attachment.add)


    def test_add_delete(self):
        from kayako.core.lib import UnsetParameter
        from kayako.objects import Department, Ticket, TicketAttachment, TicketPost, User

        api = self.api

        depts = api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        user = api.get(User, 0)

        ticket = api.create(Ticket)
        ticket.subject = self.SUBJECT
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = dept.id
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1
        ticket.userid = user.id
        ticket.ownerstaffid = user.id
        ticket.type = 'default'
        ticket.add()

        ticket_post = api.create(TicketPost)
        ticket_post.ticketid = ticket.id
        ticket_post.subject = 'DELETE_ME'
        ticket_post.contents = 'testing a post'
        ticket_post.userid = user.id
        ticket_post.add()

        ticket_attachment = api.create(TicketAttachment)
        ticket_attachment.ticketid = ticket.id
        ticket_attachment.ticketpostid = ticket_post.id
        ticket_attachment.filename = 'test_file.txt'
        ticket_attachment.set_contents('this is just a test')
        ticket_attachment.add()
        assert ticket_attachment.id is not UnsetParameter
        ticket_attachment.delete()
        ticket_post.delete()
        ticket.delete()

    def test_delete_unadded(self):
        from kayako.core.lib import UnsetParameter
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketAttachment
        ticket_attachment = self.api.create(TicketAttachment)
        ticket_attachment.id = UnsetParameter
        ticket_attachment.ticketid = 1
        self.assertRaises(KayakoRequestError, ticket_attachment.delete)
        ticket_attachment.id = 1
        ticket_attachment.ticketid = UnsetParameter
        self.assertRaises(KayakoRequestError, ticket_attachment.delete)
