import json
from .utils import make_json_post, check_error, array_check, check_dict_field
from src.models import Domain

# GET /domains returns a list of available domains.
def test_get_domains(client):
    res = client.get("/domains")

    assert res.status_code == 200
    
    json_arr = json.loads(res.data.decode("utf8"))
    assert isinstance(json_arr, list)

    def domain_check(target, name, index_page, groups):
        return check_dict_field(target, "name", name) and check_dict_field(target, "index_page", index_page) and check_dict_field(target, "groups", groups)

    assert array_check(json_arr, lambda obj: domain_check(obj, "yle.fi", "https://yle.fi/", 3))
    assert array_check(json_arr, lambda obj: domain_check(obj, "test.com", "https://test.com/index", 0))
    assert array_check(json_arr, lambda obj: domain_check(obj, "kauppa.fi", "https://kauppa.fi/home", 1))

# POST /domains creates a new domain instance
def test_post_domains(client):
    yle_domain = {
        "name": "yle.fi",
        "index_page": "https://yle.fi/"
    }
    
    new_domain = {
        "name": "teppo.fi",
        "index_page": "https://teppo.fi/testaaja"
    }

    def post_to_domains(domain):
        return make_json_post(client, "/domains", domain)

    res = post_to_domains(yle_domain)

    # Existing domain added during test setup should have a unique constraint.
    assert res.status_code == 400
    check_error(res.data.decode("utf8"), "The domain already exists")

    res = post_to_domains(new_domain)

    assert res.status_code == 200

    res = post_to_domains(new_domain)

    # The inserted domain should have a unique constraint.
    assert res.status_code == 400
    assert check_error(res.data.decode("utf8"), "The domain already exists")

# GET /domains/:id returns the domain instance and a list of annotations.
def test_get_domains_instance(client):
    def get_domain_annotations(id):
        return client.get(f"/domains/{ id }")

    # Get yle annotations
    yle_domain = Domain.query.filter_by(name="yle.fi").first()
    res = get_domain_annotations(yle_domain.id)

    assert res.status_code == 200

    json_dict = json.loads(res.data.decode("utf8"))
    assert isinstance(json_dict, dict)
    assert check_dict_field(json_dict, "name", "yle.fi")
    assert check_dict_field(json_dict, "groups", 3)

    def annotation_check(target, max_group):
        return ("group" in target 
            and target["group"] >= 0 
            and target["group"] <= max_group
            and "url" in target
            and "classes" in target
            and isinstance(target["classes"], list)
            and "domain" not in target
            and "id" in target)

    assert "annotations" in json_dict and isinstance(json_dict["annotations"], list)
    assert array_check(json_dict["annotations"], lambda item: annotation_check(item, 3))
    assert len(json_dict["annotations"]) == 6

    # Get test.com annotations
    test_domain = Domain.query.filter_by(name="test.com").first()
    res = get_domain_annotations(test_domain.id)

    assert res.status_code == 200

    json_dict = json.loads(res.data.decode("utf8"))
    assert isinstance(json_dict, dict)
    assert check_dict_field(json_dict, "name", "test.com")
    assert check_dict_field(json_dict, "groups", 0)


    assert len(json_dict["annotations"]) == 0

    # Get annotations for domain that doesn't exist.
    res = get_domain_annotations(10000)

    assert res.status_code == 404

# POST /domains/:id creates a new annotation for the targeted domain.
# Can increase the groups value of the domain. (This is why there is no PATCH /domains/:id)
def test_post_domains_instance(client):
    new_annotation = {
        "url": "https://yle/1/news1",
        "group": 1,
        "classes": ["article-body"]
    }

    yle_domain = Domain.query.filter_by(name="yle.fi").first()

    def post_to_yle(annotation):
        return make_json_post(client, f"/domains/{ yle_domain.id }", annotation)

    def get_yle_annotations():
        return client.get(f"/domains/{ yle_domain.id }")

    res = post_to_yle(new_annotation)

    assert res.status_code == 200

    res = get_yle_annotations()

    json_dict = json.loads(res.data.decode("utf8"))

    assert array_check(json_dict["annotations"], lambda item: item["url"] == new_annotation["url"] and item["group"] == 1)

    new_annotation["group"] = 2
    new_annotation["classes"] = ["article-body" ,"article-author"]

    res = post_to_yle(new_annotation)

    assert res.status_code == 200

    res = get_yle_annotations()

    json_dict = json.loads(res.data.decode("utf8"))

    assert array_check(json_dict["annotations"], lambda item: item["url"] == new_annotation["url"] and item["group"] == 2 and item["classes"] == new_annotation["classes"])

    new_annotation = {
        "url": "",
        "group": 0,
        "classes": ""
    }

    res = post_to_yle(new_annotation)

    assert res.status_code == 400

    assert check_error(res.data.decode("utf8"), "Please provide values for: url, classes")

    new_annotation = {
        "url": "https://yle.fi/urheilu/123",
        "group": 4,
        "classes": "sports-body"
    }

    res = post_to_yle(new_annotation)

    assert res.status_code == 200

    res = get_yle_annotations()
    json_dict = json.loads(res.data.decode("utf8"))
    
    assert json_dict["groups"] == 4


# GET /domains/:id/:id returns an annotation instance
def test_get_annotation(client):
    def get_domain_annotation(domain, anno):
        return client.get(f"/domains/{ domain }/{ anno }")

    yle_domain = Domain.query.filter_by(name="yle.fi").first()
    target_anno = yle_domain.annotations[0]

    yle_domain_json = {
        "name": "yle.fi",
        "index_page": "https://yle.fi/",
        "groups": 3
    }
    res = get_domain_annotation(yle_domain.id, target_anno.id)

    assert res.status_code == 200

    def check_annotation(anno, url, group, classes, domain):
        return (check_dict_field(anno, "url", url)
            and check_dict_field(anno, "group", group)
            and check_dict_field(anno, "classes", classes)
            and check_dict_field(anno, "domain", domain))

    json_dict = json.loads(res.data.decode("utf8"))

    assert check_annotation(json_dict, target_anno.url, target_anno.group, target_anno.classes.split(","), yle_domain_json)
