from eapp.test.test_base import test_client,test_app

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


def test_update_success(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "aaa",
                "price": 30,
                "quantity": 2
            }
        }

    res = test_client.put('/api/carts/1',json = {
        "quantity" : 8
    })

    assert res.status_code == 200

    data = res.get_json()
    assert data['total_quantity'] == 10
    assert data['total_amount'] == 240

    with test_client.session_transaction() as sess:
        cart = sess['cart']
        assert cart['1']['quantity'] ==10


def test_update_fail(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "aaa",
                "price": 30,
                "quantity": 2
            }
        }
    res = test_client.put('/api/carts/99', json={
        'quantity': 8
    })

    assert res.status_code == 200

    data = res.get_json()
    assert data['total_quantity'] == 2
    assert data['total_amount'] == 60

    with test_client.session_transaction() as sess:
        cart = sess['cart']
        assert len(cart) == 1

def test_delete(test_client):
    test_client.delete('api/carts/1')
    with test_client.session_transaction() as sess:
        assert sess.get('cart') is None

def test_delete_success(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1":{
                "id": 1,
                "name": "aaa",
                "price": 30,
                "quantity": 2
            },
            "2": {
                "id": 2,
                "name": "Iphone",
                "price": 30,
                "quantity": 2
            }
        }
    res = test_client.delete('/api/carts/1')

    assert res.status_code == 200
    with test_client.session_transaction() as sess:
        cart = sess.get('cart')
        assert cart is not None
        assert '1' not in cart
        assert len(cart) == 1