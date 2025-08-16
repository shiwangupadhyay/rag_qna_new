import requests

# API URL
url = "https://rag-qna-api-fhava8fqb7e0aea7.centralindia-01.azurewebsites.net/hackrx/run"

# Replace this with your actual token from .env
bearer_token = "5669aef1cb6e11718a9ea91c23074b21b9234233bec8da60d0b71a28eebcdc5e"

# Sample payload
payload = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
    ]
}

# Headers with authorization
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}

# Make the request
response = requests.post(url, json=payload, headers=headers)

# Print results
print(f"Status Code: {response.status_code}")
try:
    print("Response JSON:", response.json())
except Exception as e:
    print("Failed to parse JSON. Raw response:")
    print(response.text)
