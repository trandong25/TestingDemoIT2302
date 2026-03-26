from saleappv1.eapp.test.test_base import test_client,test_app

def test_add_to_cart_first_time(test_client):
  response = test_client.post("/api/carts", json={
     "id": 1,
     "name": "Laptop",
     "price": 1000
  })
  assert response.status_code == 200
  data = response.get_json()
  assert data["total_quantity"] == 1

def test_add_to_cart(test_client):
  res = test_client.post('/api/carts', json = {
     "id": 1,
     "name": "Iphone 17",
     "price": 50
  })
  assert res.status_code == 200
  data = res.get_json()

  assert data['total_quantity'] == 1
  assert data['total_amount'] == 50

def test_add_to_cart_increase_item(test_client):
  test_client.post('/api/carts', json = {
    "id": 1,
    "name": "Iphone 17",
    "price": 50
 })
  res = test_client.post('/api/carts', json={
   "id": 2,
   "name": "Iphone 17",
   "price": 30
  })

  assert res.status_code == 200
  data = res.get_json()

  assert data['total_quantity'] == 2
  assert data['total_amount'] == 80

def test_add_to_cart_existing_item(test_client):
  with test_client.session_transaction() as sess:
    sess['cart'] = {
     "1": {
      "id": 1,
      "name": "aaa",
      "price": 30,
      "quantity" : 2
     }
    }

  res = test_client.post('/api/carts', json = {
     "id": 1,
      "name": "Iphone 17",
     "price": 30,
    })

  assert res.status_code == 200
  data = res.get_json()

  assert data['total_quantity'] == 3
  assert data['total_amount'] == 90

  with test_client.session_transaction() as session:
   cart = session['cart']

   assert len(cart)==1
   assert "1" in cart
