import json
def test_missing_hash_to_messsage(client):
    response = client.get("/messages/bdfcba37390f1dc3d871011777098dab32c8dd9542b56291268ed950c8b58ba7")
    j = json.loads(response.data)
    assert j['error'] == "unable to find message"
    assert response.status_code == 404
    assert j['message_sha256'] == "bdfcba37390f1dc3d871011777098dab32c8dd9542b56291268ed950c8b58ba7"

def test_valid_messsage_to_hash(client):
    response = client.post("/messages",
                           data=json.dumps({"message": "this is a sample message!"}),
                           content_type='application/json'
                           )
    j = json.loads(response.data)
    assert j['digest'] == "bdfcba37390f1dc3d871011777098dab32c8dd9542b56291268ed950c8b58ba7"

def test_valid_hash_to_messsage(client):
    response = client.get("/messages/bdfcba37390f1dc3d871011777098dab32c8dd9542b56291268ed950c8b58ba7")
    j = json.loads(response.data)
    assert j['message'] == "this is a sample message!"
    assert response.status_code == 200

def test_delete_hash(client):
    response = client.delete("/messages/bdfcba37390f1dc3d871011777098dab32c8dd9542b56291268ed950c8b58ba7")
    assert response.status_code == 200

def test_delete_non_existenthash(client):
    response = client.delete("/messages/NOTEXISTENT")
    assert response.status_code == 200

def test_bad_messages_request(client):
    response = client.post("/messages",
                           data=({"message": "this is a sample message!"}),
                           )
    d = response.data
    assert d == "BAD INPUT FORMAT DETECED"

def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
