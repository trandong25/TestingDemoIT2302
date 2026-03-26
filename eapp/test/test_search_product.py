import pytest
from eapp.dao import load_products
from eapp.models import Product
from eapp.test.test_base import test_app, test_session


@pytest.fixture()
def sample_products(test_session):
    p1 = Product(name = "IP 17", price = 30, category_id=1)
    p2 = Product(name="IP .. 17", price=30, category_id=1)
    p3 = Product(name="Galaxy 17", price=30, category_id=2)
    p4 = Product(name="IP ... abc", price=30, category_id=2)
    p5 = Product(name="IP ... abc13", price=30, category_id=3)

    test_session.add_all([p1, p2, p3, p4, p5])
    test_session.commit()

    return [p1,p2,p3,p4,p5]

def test_all(sample_products):
    actual_products = load_products()
    assert len(actual_products) == len(sample_products)

def test_paging(test_app, sample_products):
    actual_products = load_products(page=1)
    assert len(actual_products) == test_app.config['PAGE_SIZE']

    actual_products = load_products(page=3)
    assert len(actual_products) == 1

def test_cate_id(test_app, sample_products):
    actual_products = load_products(cate_id=1)
    assert len(actual_products) == 2

    actual_products = load_products(cate_id=2)
    assert len(actual_products) == 2

    actual_products = load_products(cate_id=3)
    assert len(actual_products) == 1


def test_kw(test_app, sample_products):
    actual_products = load_products(kw="IP")
    assert len(actual_products) == 4

    actual_products = load_products(kw="ip")
    assert len(actual_products) == 4

    actual_products = load_products(kw="17")
    assert len(actual_products) == 3

    actual_products = load_products(kw="abc")
    assert len(actual_products) == 2

    actual_products = load_products(kw="13")
    assert len(actual_products) == 1

    actual_products = load_products(kw="..")
    assert len(actual_products) == 3

    actual_products = load_products(kw=".")
    assert len(actual_products) == 3

    actual_products = load_products(kw="...")
    assert len(actual_products) == 2

    actual_products = load_products(kw="Galaxy")
    assert len(actual_products) == 1

    actual_products = load_products(kw="galaxy")
    assert len(actual_products) == 1

    actual_products = load_products(kw="ga")
    assert len(actual_products) == 1

    actual_products = load_products(kw="la")
    assert len(actual_products) == 1

    actual_products = load_products(kw="xy")
    assert len(actual_products) == 1

    actual_products = load_products(kw="")
    assert len(actual_products) == 5
