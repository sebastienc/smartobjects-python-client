import unittest
import ConfigParser
import time

from smartobjects import SmartObjectsClient
from smartobjects import Environments

class TestHelper(object):
    timeout = 240
    delay = 5

    @staticmethod
    def getClient():
        Config = ConfigParser.ConfigParser()
        Config.read("ittests/resources/creds.ini")
        key = Config.get("Credentials", "key")
        secret = Config.get("Credentials", "secret")
        return SmartObjectsClient(key, secret, Environments.Sandbox)

    @staticmethod
    def searchEventQuery(eventId):
        return {
          "from": "event",
          "select": [
            {
              "value": "event_id"
            },
            {
              "value": "ts_text_attribute"
            }
          ],
          "where": {
            "event_id": {
              "eq": eventId.lower()
            }
          }
        }

    @staticmethod
    def searchObjectByOwnerQuery(username):
        return {
          "from": "object",
          "select": [
            {
              "value": "x_device_id"
            },
            {
              "value": "object_text_attribute"
            }
          ],
          "where": {
            "x_owner.username": {
              "eq": username.lower()
            }
          }
        }

    @staticmethod
    def searchOwnerQuery(username): 
        return {
            "from": "owner",
            "select": [
                {
                  "value": "username"
                },
                {
                  "value": "owner_text_attribute"
                }
            ],
            "where": {
                "username": {
                  "eq": username.lower()
                }
            }
        }

    @staticmethod
    def searchObjectQuery(deviceId): 
        return {
          "from": "object",
          "select": [
            {
              "value": "x_device_id"
            },
            {
              "value": "object_text_attribute"
            }
          ],
          "where": {
            "x_device_id": {
              "eq": deviceId
            }
          }
        }

    @staticmethod
    def eventuallyAssert(myAssert):
        TestHelper.eventuallyAssertWithDelay(myAssert, TestHelper.timeout, TestHelper.delay)

    @staticmethod
    def eventuallyAssertWithDelay(myAssert, timeout, delay):
        if (timeout < delay):
            raise Exception("timeout should be bigger than delay")

        current_time = lambda: int(round(time.time()))

        stopper = current_time() + timeout
        lastAssertException = None

        while current_time() < stopper:
            try:
                myAssert()
                return
            except AssertionError as e:
                lastAssertException = e
                print "Assert failed: {}. Will retry".format(e)
            except Exception as e:
                raise e
            time.sleep(delay)

        if lastAssertException != None:
            print "Final tentative failed."
            raise lastAssertException