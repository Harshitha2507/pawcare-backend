from app import app
import json

def test_route():
    print("Testing /pets/ route...")
    try:
        client = app.test_client()
        response = client.get('/pets/')
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.data)
            print(f"Received {len(data)} pets.")
            if len(data) > 0:
                print("First pet sample:")
                print(data[0])
        else:
            print("Response Data:")
            print(response.data)
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_route()
