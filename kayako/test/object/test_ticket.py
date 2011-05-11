# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the GNU General Public License (GPL)
#-----------------------------------------------------------------------------
'''
Created on May 9, 2011

@author: evan
'''
from kayako.test import KayakoAPITest

class TestTicket(KayakoAPITest):

    def test_get_all(self):
        from kayako.objects import Department, Ticket

        depts = self.api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        result = self.api.get_all(Ticket, dept.id)
        assert isinstance(result, list)

    def test_get_all_with_kwargs(self):
        from kayako.objects import Department, Ticket

        depts = self.api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        ticket = self.api.create(Ticket)
        ticket.subject = 'DELETE_ME'
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

        result = self.api.get_all(Ticket, dept.id, ticketstatusid=[1], ownerstaffid=[1], userid=[1])
        assert isinstance(result, list)

        #ticket.delete()

    def test_get_ticket(self):
        from kayako.objects import Department, Ticket

        depts = self.api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        ticket = self.api.create(Ticket)
        ticket.subject = 'DELETE_ME'
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

        get_ticket = self.api.get(Ticket, ticket.id)
        self.assertEqual(get_ticket.id, ticket.id)


        assert 'Ticket ' in str(get_ticket)

        ticket.delete()

    def test_add_missing_subject(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Ticket

        ticket = self.api.create(Ticket)

        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = 1
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1

        ticket.userid = 1

        ticket.ownerstaffid = 1
        ticket.type = 'default'

        self.assertRaises(KayakoRequestError, ticket.add)

    def test_add_missing_fullname(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Ticket

        ticket = self.api.create(Ticket)

        ticket.subject = 'TEST TICKET'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = 1
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1

        ticket.userid = 1

        ticket.ownerstaffid = 1
        ticket.type = 'default'

        self.assertRaises(KayakoRequestError, ticket.add)

    def test_add_missing_email(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Ticket

        ticket = self.api.create(Ticket)

        ticket.subject = 'TEST TICKET'
        ticket.fullname = 'Unit Test'
        ticket.contents = 'test'
        ticket.departmentid = 1
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1

        ticket.userid = 1

        ticket.ownerstaffid = 1
        ticket.type = 'default'

        self.assertRaises(KayakoRequestError, ticket.add)

    def test_add_missing_contents(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Ticket

        ticket = self.api.create(Ticket)

        ticket.subject = 'TEST TICKET'
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.departmentid = 1
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1

        ticket.userid = 1

        ticket.ownerstaffid = 1
        ticket.type = 'default'

        self.assertRaises(KayakoRequestError, ticket.add)

    def test_add_missing_departmentid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Ticket

        ticket = self.api.create(Ticket)

        ticket.subject = 'TEST TICKET'
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1

        ticket.userid = 1

        ticket.ownerstaffid = 1
        ticket.type = 'default'

        self.assertRaises(KayakoRequestError, ticket.add)

    def test_add_missing_ticketstatusid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Ticket

        ticket = self.api.create(Ticket)

        ticket.subject = 'TEST TICKET'
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1

        ticket.userid = 1

        ticket.ownerstaffid = 1
        ticket.type = 'default'

        self.assertRaises(KayakoRequestError, ticket.add)

    def test_add_missing_ticketpriorityid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Ticket

        ticket = self.api.create(Ticket)

        ticket.subject = 'TEST TICKET'
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = 1
        ticket.ticketstatusid = 1
        ticket.tickettypeid = 1

        ticket.userid = 1

        ticket.ownerstaffid = 1
        ticket.type = 'default'

        self.assertRaises(KayakoRequestError, ticket.add)

    def test_add_missing_tickettypeid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Ticket

        ticket = self.api.create(Ticket)

        ticket.subject = 'TEST TICKET'
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = 1
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1

        ticket.userid = 1

        ticket.ownerstaffid = 1
        ticket.type = 'default'

        self.assertRaises(KayakoRequestError, ticket.add)

    def test_add_missing_staffid_and_userid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Ticket

        ticket = self.api.create(Ticket)

        ticket.subject = 'TEST TICKET'
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = 1
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1

        ticket.ownerstaffid = 1
        ticket.type = 'default'

        self.assertRaises(KayakoRequestError, ticket.add)

    def test_add_with_both_staffid_and_userid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Ticket

        ticket = self.api.create(Ticket)

        ticket.subject = 'TEST TICKET'
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = 1
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1

        ticket.userid = 1
        ticket.staffid = 1

        ticket.ownerstaffid = 1
        ticket.type = 'default'

        self.assertRaises(KayakoRequestError, ticket.add)


    def test_add_save_delete(self):
        from kayako.core.lib import UnsetParameter
        from kayako.objects import Department, Ticket

        depts = self.api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        ticket = self.api.create(Ticket)
        ticket.subject = 'DELETE_ME'
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
        assert ticket.id is not UnsetParameter
        ticket.subject = 'DELETE_ME2'
        ticket.save()
        ticket.delete()

        found_error = False
        all = self.api.get_all(Ticket, 1, ticketstatusid=1, ownerstaffid=1, userid=1)
        for obj in all:
            if obj.subject == 'DELETE_ME' or obj.subject == 'DELETE_ME2':
                obj.delete()
                found_error = True
        if found_error:
            assert False, 'Found an error, Tickets did not delete correctly.'

    def test_delete_unadded(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Ticket
        ticket = self.api.create(Ticket)
        self.assertRaises(KayakoRequestError, ticket.delete)

