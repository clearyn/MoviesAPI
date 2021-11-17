import pytest, json
from config import connex_app
from models import Directors

connex_app.add_api("swagger.yml")

@pytest.fixture(scope='module')
def client():
    with connex_app.app.test_client() as c:
        yield c

##Enpoint Directors
def test_directors_read_all(client):
	"""
	Test API read_all directors module
	"""
	url = 'api/directors?limit=1'
	response = client.get(url)
	assert response.status_code == 200, f"directors.read_all: expected 200. status code: {response.status_code}"

def test_directors_read_one(client):
	"""
	Test API read_one directors module
	"""
	url = 'api/director/7000'
	response = client.get(url)
	assert response.status_code == 200, f"directors.read_one: expected 200. status code: {response.status_code}"

# def test_director_create(client):
# 		"""
# 		Test API create directors module
# 		"""
# 		url = 'api/director'

# 		mock_request_data = {
# 			'payload': {
# 				'department': 'TestDepartment1',
# 				'gender': 2,
# 				'name': 'Test1',
# 				'uid': 1
# 			}
# 		}

# 		response = client.post(url, data=json.dumps(mock_request_data))
# 		assert response.status_code == 201, f"directors.create: expected 201. status code: {response.status_code}"

##Endpoint Movies
def test_movies_read_all(client):
	"""
	Test API read_all movies module
	"""
	url = 'api/movies?limit=1'
	response = client.get(url)
	assert response.status_code == 200, f"movies.read_one: expected 200. status code: {response.status_code}"

def test_movies_read_one(client):
	"""
	Test API read_one movies module
	"""
	url = 'api/directors/7000/movies/48238'
	response = client.get(url)
	assert response.status_code == 200, f"directors.read_one: expected 200. status code: {response.status_code}"