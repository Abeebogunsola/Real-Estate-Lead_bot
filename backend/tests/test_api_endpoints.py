"""Unit tests for FastAPI endpoints used by n8n and frontend."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base, get_db

# SQLite in-memory database for fast isolated unit testing
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_health_check(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"


def test_chat_creation_and_get_message_flow(client):
    """Test full cycle: send chat -> get message by ID -> get conversation -> get lead."""
    # 1. Customer sends chat message
    chat_payload = {
        "content": "I want to buy a 3 bedroom duplex in Lekki for 80m",
        "name": "Abeeb",
        "email": "abeeb@example.com",
        "phone": "+2348012345678",
    }
    chat_res = client.post("/api/v1/chat", json=chat_payload)
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    msg_id = chat_data["customer_message"]["id"]
    conv_id = chat_data["conversation_id"]
    lead_id = chat_data["lead_id"]

    # 2. n8n "Get Message" node calls GET /api/v1/messages/{message_id}
    msg_res = client.get(f"/api/v1/messages/{msg_id}")
    assert msg_res.status_code == 200
    msg_data = msg_res.json()
    assert msg_data["id"] == msg_id
    assert msg_data["content"] == chat_payload["content"]

    # 3. n8n "Get Conversation" node calls GET /api/v1/conversations/{conversation_id}
    conv_res = client.get(f"/api/v1/conversations/{conv_id}")
    assert conv_res.status_code == 200
    conv_data = conv_res.json()
    assert conv_data["id"] == conv_id
    assert conv_data["lead_id"] == lead_id

    # 4. n8n "Get Lead" node calls GET /api/v1/leads/{lead_id}
    lead_res = client.get(f"/api/v1/leads/{lead_id}")
    assert lead_res.status_code == 200
    lead_data = lead_res.json()
    assert lead_data["id"] == lead_id
    assert lead_data["name"] == "Abeeb"

    # 5. n8n "Update Lead" node calls PATCH /api/v1/leads/{lead_id}
    update_payload = {
        "transaction_type": "BUY",
        "property_type": "DUPLEX",
        "bedrooms": 3,
        "location": "Lekki",
        "budget_max": 80000000.0,
        "currency": "NGN",
        "timeline": "IMMEDIATE",
    }
    patch_res = client.patch(f"/api/v1/leads/{lead_id}", json={"lead_update": update_payload})
    assert patch_res.status_code == 200
    updated_lead = patch_res.json()
    assert updated_lead["transaction_type"] == "BUY"
    assert updated_lead["bedrooms"] == 3
    assert updated_lead["score"] is not None
    assert updated_lead["score"] > 0
    assert updated_lead["classification"] in ("HOT", "WARM", "COLD")

    # 6. n8n "Trigger Qualification" calls POST /api/v1/leads/{lead_id}/qualify
    qualify_res = client.post(f"/api/v1/leads/{lead_id}/qualify")
    assert qualify_res.status_code == 200
    qual_data = qualify_res.json()
    assert qual_data["status"] == "QUALIFIED"

    # 7. n8n "Save Bot Response" calls POST /api/v1/conversations/{conversation_id}/messages
    bot_payload = {
        "content": "Hello Abeeb, we have matching 3-bedroom duplexes in Lekki. Our agent will contact you.",
        "sender_type": "BOT",
    }
    bot_res = client.post(f"/api/v1/conversations/{conv_id}/messages", json=bot_payload)
    assert bot_res.status_code == 200
    bot_data = bot_res.json()
    assert bot_data["sender_type"] == "BOT"
    assert bot_data["status"] == "PROCESSED"

    # 8. n8n "Mark Message Processed" calls PATCH /api/v1/messages/{message_id}
    patch_msg_res = client.patch(f"/api/v1/messages/{msg_id}", json={"processing_status": "PROCESSED"})
    assert patch_msg_res.status_code == 200
    assert patch_msg_res.json()["status"] == "PROCESSED"

    # 9. n8n "Record Activity" calls POST /api/v1/leads/{lead_id}/activities
    act_res = client.post(f"/api/v1/leads/{lead_id}/activities", json={"actor_type": "SYSTEM"})
    assert act_res.status_code == 200
    assert act_res.json()["ok"] is True
