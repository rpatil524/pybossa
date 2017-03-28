# -*- coding: utf8 -*-
# This file is part of PYBOSSA.
#
# Copyright (C) 2017 Scifabric LTD.
#
# PYBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PYBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PYBOSSA.  If not, see <http://www.gnu.org/licenses/>.
import json
from default import db, with_context
from nose.tools import assert_equal
from test_api import TestAPI

from factories import TaskFactory, UserFactory

from pybossa.repositories import TaskRepository

task_repo = TaskRepository(db)

class TestFavoritesAPI(TestAPI):

    url = '/api/favorites'

    @with_context
    def test_query_favorites_anon(self):
        """Test API Favorites works for anon."""
        user = UserFactory.create()
        TaskFactory.create(fav_user_ids=[user.id])
        res = self.app.get(self.url)
        data = json.loads(res.data)
        assert res.status_code == 401
        assert data['status_code'] == 401

    @with_context
    def test_query_get_favorites_auth(self):
        """Test API GET Favorites works for user."""
        user = UserFactory.create()
        user2 = UserFactory.create()
        task = TaskFactory.create(fav_user_ids=[user.id])
        TaskFactory.create(fav_user_ids=[user2.id])
        res = self.app.get(self.url + '?api_key=%s' % user.api_key)
        data = json.loads(res.data)
        assert res.status_code == 200, res.status_code
        assert len(data) == 1, data
        data = data[0]
        assert data['id'] == task.id, (data, task)
        assert data['fav_user_ids'] == [user.id], data
        assert len(data['fav_user_ids']) == 1, data

    @with_context
    def test_query_put_favorites_auth(self):
        """Test API PUT Favorites works for user."""
        user = UserFactory.create()
        user2 = UserFactory.create()
        TaskFactory.create(fav_user_ids=[user.id])
        TaskFactory.create(fav_user_ids=[user2.id])
        res = self.app.put(self.url + '/1?api_key=%s' % user.id)
        data = json.loads(res.data)
        assert res.status_code == 405, res.status_code
        assert data['status_code'] == 405, data

        res = self.app.put(self.url + '?api_key=%s' % user.id)
        assert res.status_code == 405, res.status_code

    @with_context
    def test_query_put_favorites_anon(self):
        """Test API PUT Favorites works for anon."""
        user = UserFactory.create()
        user2 = UserFactory.create()
        TaskFactory.create(fav_user_ids=[user.id])
        TaskFactory.create(fav_user_ids=[user2.id])
        res = self.app.put(self.url + '/1')
        data = json.loads(res.data)
        assert res.status_code == 405, res.status_code
        assert data['status_code'] == 405, data

        res = self.app.put(self.url)
        assert res.status_code == 405, res.status_code
