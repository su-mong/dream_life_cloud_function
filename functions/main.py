# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import firestore_fn, https_fn

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore
import google.cloud.firestore
import json

app = initialize_app()


@https_fn.on_request()
def getAllPosts(req: https_fn.Request) -> https_fn.Response:
    firestore_client: google.cloud.firestore.Client = firestore.client()

    # Push the new message into Cloud Firestore using the Firebase Admin SDK.
    docs = firestore_client.collection("post").stream()

    # 도큐먼트를 담을 리스트 초기화
    documents_list = []

    for doc in docs:
        # 도큐먼트 데이터를 dict로 변환하고 ID를 함께 저장
        doc_data = doc.to_dict()
        doc_data['id'] = doc.id  # 도큐먼트 ID를 포함할 수도 있음
        documents_list.append(doc_data)

    # Send back a message that we've successfully written the message
    return https_fn.Response(json.dumps(documents_list, indent="\t", ensure_ascii=False))


@https_fn.on_request()
def addMessage(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection."""
    # Grab the text parameter.
    original = req.args.get("text")
    if original is None:
        return https_fn.Response("No text parameter provided", status=400)

    firestore_client: google.cloud.firestore.Client = firestore.client()

    # Push the new message into Cloud Firestore using the Firebase Admin SDK.
    _, doc_ref = firestore_client.collection("messages").add(
        {"original": original}
    )

    # Send back a message that we've successfully written the message
    return https_fn.Response(f"Message with ID {doc_ref.id} added.")