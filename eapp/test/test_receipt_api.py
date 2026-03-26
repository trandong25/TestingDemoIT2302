from eapp.test.test_base import test_client, test_app

def test_add_receipt_success(test_client, mocker):
     class FakeUser():
        is_authenticated = True

     mocker.patch("flask_login.utils._get_user", return_value=FakeUser())
     mocker.patch("saleappv1.eapp.dao.current_user", new=FakeUser())

     with test_client.session_transaction() as sess:
         sess['cart'] = {
             "1": {
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

     mock_add = mocker.patch("saleappv1.eapp.dao.add_receipt")

     response = test_client.post("/api/pay")

     assert response.status_code == 200

     with test_client.session_transaction() as sess:
        assert 'cart' not in sess
     mock_add.assert_called_once()


def test_add_receipt_exception(test_client, mocker):
    class FakeUser():
        is_authenticated = True

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser())
    mocker.patch("saleappv1.eapp.dao.current_user", new=FakeUser())

    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
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

    mock_add = mocker.patch("saleappv1.eapp.dao.add_receipt", side_effect = Exception('DB error'))

    response = test_client.post("/api/pay")
    data = response.get_json()

    assert data['status'] == 400
    assert data['err_msg'] == 'DB error'

    mock_add.assert_called_once()