# Copyright (C) 2025 All rights reserved.
# This file is part of the Delve project, which is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the root of this repository for details.

"""This test module is meant to test the limit search
command, located at events.search_commands.qs.limit.
"""
import json
from unittest.mock import MagicMock

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import (
    APITestCase,
    APIRequestFactory,
    APIClient,
)

from events.models import (
    Event,
    Query,
)


TEST_USER = "testuser"
TEST_USER_PASS = "testuser"
TEST_ADMIN = "testadmin"
TEST_ADMIN_PASS = "testadmin"

class LimitTests(APITestCase):
    def setUp(self, *args, **kwargs):
        """For preparation, we are going to setup a user and
        an APIClient and add ten Events.
        """
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testuser',
        )
        self.user.save()
        self.events = []
        for i in range(10):
            event = Event.objects.create(
                index="test",
                host="127.0.0.1",
                source="test",
                sourcetype="json",
                user=self.user,
                text=json.dumps(
                    {
                        "foo": i,
                        "bar": i % 2,
                    }
                )
            )
            event.extract_fields()
            event.process()
            event.save()
            self.events.append(event)
        super().setUp(*args, **kwargs)

    def test_limit(self):
        """Test the limit command to ensure it correctly limits
        the number of records in the QuerySet.
        """
        query = Query(
            name="test",
            text="search index=test | qs_limit 5",
            user=self.user,
        )
        results = query.resolve(
            request=MagicMock(user=self.user),
        )
        self.assertEqual(len(results), 5)

    def test_limit_with_offset(self):
        """Test the limit command with offset to ensure it correctly limits
        the number of records in the QuerySet after skipping the specified number of records.
        """
        query = Query(
            name="test",
            text="search index=test | qs_limit 5 --offset 3",
            user=self.user,
        )
        results = query.resolve(
            request=MagicMock(user=self.user),
        )
        self.assertEqual(len(results), 5)
        self.assertEqual(results[0]['extracted_fields']['foo'], 3)
        self.assertEqual(results[1]['extracted_fields']['foo'], 4)
        self.assertEqual(results[2]['extracted_fields']['foo'], 5)
