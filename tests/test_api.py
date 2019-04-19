import unittest
import requests
import json
import random

class TestEndPoints(unittest.TestCase):
  
  def test_registration_get(self):
    ''' get request not allowerd -> 405 '''
    endpoint = 'http://localhost:5000/registration'
    get_req = requests.get(endpoint)
    self.assertEqual(get_req.status_code, 405)

  def test_registration_post_no_data(self):
    ''' post request with no data or only one parameter'''
    endpoint = 'http://localhost:5000/registration'
    post_req = requests.post(endpoint, data=None)
    self.assertEqual(post_req.status_code, 400)
    post_req = requests.post(endpoint, data={"username" : "joao"})
    self.assertEqual(post_req.status_code, 400)

  def test_registration_post_data(self):
    ''' post request with data but user exists '''
    endpoint = 'http://localhost:5000/registration'
    post_req = requests.post(endpoint, data={"username" : "joao", "password" : "password"})
    self.assertEqual(post_req.status_code, 200)
    self.assertEqual('That username already exists.', json.loads(post_req.text)['message'])
    
    ''' post request with data and new user '''
    endpoint = 'http://localhost:5000/registration'
    abcs = 'abcdefghijklmonpqrstuvwxzy'
    randusername = random.choice(abcs) * 5
    post_req = requests.post(endpoint, data={"username" : randusername, "password" : "password"})  
    self.assertEqual(randusername, json.loads(post_req.text)['username'])

  def test_login_get(self):
    ''' get request not allowed -> 405 '''
    endpoint = 'http://localhost:5000/login'
    get_req = requests.get(endpoint)
    self.assertEqual(get_req.status_code, 405)
  



if __name__ == "__main__":
    unittest.main()