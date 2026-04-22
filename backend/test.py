import requests

# Lien de votre API
url = "http://127.0.0.1:5000/search"

# Liste des tests
tests = [
    {"query": "I want a healthy and protein-rich recipe"},
    {"query": "I want a vegan dinner recipe"},
    {"query": "I want a dessert with chocolate and nuts"},
    {"query": "Give me a quick pasta recipe"},
    {"query": "Recipes with chicken and broccoli"},
    {"query": "I want a spicy Indian curry"},
    {"query": "I want a soup without meat"},
    {"query": "Healthy breakfast ideas with eggs and avocado"},
    {"query": ""},
    {"query": "Unicorn-flavored ice cream"}
]

# Exécuter les tests
for i, test in enumerate(tests, 1):
    response = requests.post(url, json=test)
    print(f"Test {i}: {test['query']}")
    print(response.json())
    print("\n" + "-"*50 + "\n")
