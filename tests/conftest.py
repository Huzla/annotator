import pytest

from src import create_app_and_db
from src.models import Domain, Annotation

@pytest.fixture
def app():
    [app, db] = create_app_and_db()

    # Create test data
    yle_domain = Domain(name="yle.fi", index_page="https://yle.fi/", groups=3)
    test_domain = Domain(name="test.com", index_page="https://test.com/index", groups=0)
    kauppa_domain = Domain(name="kauppa.fi", index_page="https://kauppa.fi/home", groups=1)

    db.session.add(yle_domain)
    db.session.add(test_domain)
    db.session.add(kauppa_domain)

    db.session.commit()

    db.session.add(Annotation(url="https://yle.fi/1/test1", group=1, classes="article,article-author" ,domain=yle_domain))
    db.session.add(Annotation(url="https://yle.fi/1/test2", group=1, classes="article,article-author" , domain=yle_domain))
    db.session.add(Annotation(url="https://yle.fi/1/test3", group=1, classes="article" ,domain=yle_domain))
    db.session.add(Annotation(url="https://yle.fi/2/test4", group=2, classes="comments,sports-stuff,stats" , domain=yle_domain))
    db.session.add(Annotation(url="https://yle.fi/2/test5", group=2, classes="comments,sports-stuff,stats" , domain=yle_domain))
    db.session.add(Annotation(url="https://yle.fi/3/test6", group=3, classes="table-of-stats" , domain=yle_domain))
    db.session.add(Annotation(url="https://kauppa.fi/products/phones/123456", group=1, classes="product-name,product-description,price-value", domain=kauppa_domain))

    db.session.commit()

    yield app

    db.session.delete(yle_domain)
    db.session.delete(test_domain)
    db.session.delete(kauppa_domain)

    db.session.commit()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner() 