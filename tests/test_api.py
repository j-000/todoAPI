import unittest
import requests
import json


base_url = 'http://localhost:5000'

''' BEFORE RUNNING TESTS RUN python dbhelper.py '''

class TestEndPoints(unittest.TestCase):
  
  def test_registration_methods_allowed(self):
    ''' only POST allowed '''
    endpoint = f'{base_url}/registration'

    # GET request
    get_req = requests.get(endpoint)
    # PUT request
    put_req = requests.put(endpoint, data={})
    # DELETE request
    del_req = requests.delete(endpoint)
  
    # Assert all the above methods return 405 (method not allowed)
    self.assertEqual(get_req.status_code, 405)
    self.assertEqual(put_req.status_code, 405)
    self.assertEqual(del_req.status_code, 405)

  def test_registration_create_user(self):
    ''' Create user '''
    endpoint = f'{base_url}/registration'
    # POST request
    headers = {"Content-Type": "application/json"}
    data = {"username":"_test", "email":"_test@t.com", "password":"_pass"}
    post_req = requests.post(endpoint, headers=headers, data=json.dumps(data))
    # Assert response 200
    self.assertEqual(post_req.status_code, 200)
    # Assert response message
    self.assertEqual(json.loads(post_req.text)['message'], 'Success. User created.')
    # Assert response user matches
    self.assertEqual(json.loads(post_req.text)['username'], '_test')
    # Assert response email matches
    self.assertEqual(json.loads(post_req.text)['email'], '_test@t.com')

  def test_registration_user_exists(self):
    ''' User exists '''
    endpoint = f'{base_url}/registration'
    headers = {"Content-Type": "application/json"}
    data = {"username":"_test", "email":"_test@t.com", "password":"_pass"}
    # Repeat the request above
    post_req_repeat = requests.post(endpoint, headers=headers, data=json.dumps(data))
    # Assert response 400 (bad request)
    self.assertEqual(post_req_repeat.status_code, 400)
    # Assert response message 
    self.assertEqual(json.loads(post_req_repeat.text)['message'], '_test@t.com is already registered. If you need to reset your password, check the docs.')
  
  def test_registration_missing_parameter(self):
    ''' Missing parameters '''
    endpoint = f'{base_url}/registration'
    headers = {"Content-Type": "application/json"}
    data_missing = {"username":"_test_2", "password":"_pass"}
    post_req_missing = requests.post(endpoint, headers=headers, data=json.dumps(data_missing))
    # Assert response 400 (bad request)
    self.assertEqual(post_req_missing.status_code, 400)
    # Assert response message
    self.assertEqual(json.loads(post_req_missing.text)['message'], 'Some parameters are missing. You need \'username\', \'email\' and \'password\'.')




if __name__ == "__main__":
    unittest.main()