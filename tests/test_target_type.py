from utils.target_type import classify_target

def test_email():
    assert classify_target("user@example.com") == "email"

def test_domain():
    assert classify_target("google.com") == "domain"

def test_ip():
    assert classify_target("8.8.8.8") == "ip"