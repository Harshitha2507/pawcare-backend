import mysql.connector
import config
from models import get_db_connection

def seed_pets():
    pets = [
        # 🐶 DOGS (6)
        {
            "name": "Buddy", "category": "Dogs", "breed": "Golden Retriever",
            "image": "https://images.unsplash.com/photo-1552053831-71594a27632d",
            "location": "Jubilee Hills, Hyderabad", "age": "2 years", "sex": "Male", "color": "Golden",
            "description": "Friendly and plays well with kids."
        },
        {
            "name": "Charlie", "category": "Dogs", "breed": "Labrador",
            "image": "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8",
            "location": "Banjara Hills, Hyderabad", "age": "1 year", "sex": "Male", "color": "Black",
            "description": "Energetic puppy looking for active owners."
        },
        {
            "name": "Luna", "category": "Dogs", "breed": "Husky",
            "image": "https://images.unsplash.com/photo-1605568427561-40dd23d2acca",
            "location": "Kondapur, Hyderabad", "age": "2 years", "sex": "Female", "color": "White & Grey",
            "description": "Loves the snow and running long distances."
        },
        {
            "name": "Bella", "category": "Dogs", "breed": "Beagle",
            "image": "https://images.unsplash.com/photo-1537151625747-768eb6cf92b2",
            "location": "Gachibowli, Hyderabad", "age": "3 years", "sex": "Female", "color": "Tricolor",
            "description": "Curious and loves following scent trails."
        },
        {
            "name": "Max", "category": "Dogs", "breed": "German Shepherd",
            "image": "https://images.unsplash.com/photo-1589941013453-ec89f33b5e95",
            "location": "Madhapur, Hyderabad", "age": "4 years", "sex": "Male", "color": "Black & Tan",
            "description": "Loyal, intelligent, and very protective."
        },
        {
            "name": "Daisy", "category": "Dogs", "breed": "Poodle",
            "image": "https://images.unsplash.com/photo-1598133894008-61f7fdb8cc3a",
            "location": "Kukatpally, Hyderabad", "age": "2 years", "sex": "Female", "color": "White",
            "description": "Elegant and highly trainable companion."
        },

        # 🐱 CATS (6)
        {
            "name": "Oliver", "category": "Cats", "breed": "British Shorthair",
            "image": "https://images.unsplash.com/photo-1573865526739-10659fec78a5",
            "location": "Secunderabad, Hyderabad", "age": "2 years", "sex": "Male", "color": "Grey",
            "description": "Calm and dignified."
        },
        {
            "name": "Milo", "category": "Cats", "breed": "Tabby",
            "image": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba",
            "location": "Ameerpet, Hyderabad", "age": "1 year", "sex": "Male", "color": "Striped",
            "description": "Adventurous and very playful."
        },
        {
            "name": "Lily", "category": "Cats", "breed": "Ragdoll",
            "image": "https://images.unsplash.com/photo-1543852786-1cf6624b9987",
            "location": "Hitech City, Hyderabad", "age": "2 years", "sex": "Female", "color": "White & Brown",
            "description": "Loves to be held like a baby and very docile."
        },
        {
            "name": "Simba", "category": "Cats", "breed": "Maine Coon",
            "image": "https://images.unsplash.com/photo-1533738363-b7f9aef128ce",
            "location": "Manikonda, Hyderabad", "age": "3 years", "sex": "Male", "color": "Ginger",
            "description": "A gentle giant with a magnificent coat."
        },
        {
            "name": "Chloe", "category": "Cats", "breed": "Siamese",
            "image": "https://images.unsplash.com/photo-1513245543132-31f507417b26",
            "location": "Begumpet, Hyderabad", "age": "2 years", "sex": "Female", "color": "Cream",
            "description": "Very vocal and loves human interaction."
        },
        {
            "name": "Nala", "category": "Cats", "breed": "Bengal",
            "image": "https://images.unsplash.com/photo-1511044568932-338cba0fb803",
            "location": "Miyapur, Hyderabad", "age": "1 year", "sex": "Female", "color": "Spotted",
            "description": "Highly energetic and loves to climb."
        },

        # 🦜 PARROT (6)
        {
            "name": "Rio", "category": "Parrot", "breed": "Macaw",
            "image": "https://images.unsplash.com/photo-1552728089-57bdde30ebd1",
            "location": "Himayatnagar, Hyderabad", "age": "5 years", "sex": "Male", "color": "Blue & Gold",
            "description": "Vibrant, loud, and very social."
        },
        {
            "name": "Kiwi", "category": "Parrot", "breed": "Budgerigar",
            "image": "https://images.unsplash.com/photo-1620101967262-12465e921509",
            "location": "Abids, Hyderabad", "age": "1 year", "sex": "Male", "color": "Green",
            "description": "Small, chatty, and loves whistles."
        },
        {
            "name": "Sunny", "category": "Parrot", "breed": "Cockatiel",
            "image": "https://images.unsplash.com/photo-1616782229566-513689cc647b",
            "location": "Kothapet, Hyderabad", "age": "2 years", "sex": "Female", "color": "Yellow",
            "description": "Whistles beautiful tunes and is very friendly."
        },
        {
            "name": "Mango", "category": "Parrot", "breed": "Lovebird",
            "image": "https://images.unsplash.com/photo-1551024641-28eb6a0af5a2",
            "location": "Dilsukhnagar, Hyderabad", "age": "2 years", "sex": "Male", "color": "Orange & Green",
            "description": "Very affectionate and needs a lot of attention."
        },
        {
            "name": "Blue", "category": "Parrot", "breed": "African Grey",
            "image": "https://images.unsplash.com/photo-1549420847-a419515915d3",
            "location": "Uppal, Hyderabad", "age": "4 years", "sex": "Male", "color": "Grey",
            "description": "Extremely intelligent and an amazing talker."
        },
        {
            "name": "Ruby", "category": "Parrot", "breed": "Eclectus",
            "image": "https://images.unsplash.com/photo-1620694157053-4886bce7263c",
            "location": "Nallakunta, Hyderabad", "age": "3 years", "sex": "Female", "color": "Red",
            "description": "Bright, calm, and very beautiful."
        },

        # 🐰 RABBITS (6)
        {
            "name": "Thumper", "category": "Rabbits", "breed": "Dutch Rabbit",
            "image": "https://images.unsplash.com/photo-1591382696684-38c427c7547a",
            "location": "Attapur, Hyderabad", "age": "1 year", "sex": "Male", "color": "Black & White",
            "description": "Loves to thump his foot when happy."
        },
        {
            "name": "Snowball", "category": "Rabbits", "breed": "Angora",
            "image": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308",
            "location": "Tolichowki, Hyderabad", "age": "2 years", "sex": "Female", "color": "White",
            "description": "Super fluffy and requires regular grooming."
        },
        {
            "name": "Cinnabun", "category": "Rabbits", "breed": "Mini Lop",
            "image": "https://images.unsplash.com/photo-1555181126-cf4c68161710",
            "location": "Mehdipatnam, Hyderabad", "age": "1 year", "sex": "Male", "color": "Brown",
            "description": "Small ears and a very big heart."
        },
        {
            "name": "Oreo", "category": "Rabbits", "breed": "Checkered Giant",
            "image": "https://images.unsplash.com/photo-1510300643789-224855964f40",
            "location": "LB Nagar, Hyderabad", "age": "2 years", "sex": "Male", "color": "Black & White",
            "description": "A larger rabbit with a very gentle personality."
        },
        {
            "name": "Hazel", "category": "Rabbits", "breed": "Wild Mix",
            "image": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee",
            "location": "Narsingi, Hyderabad", "age": "2 years", "sex": "Female", "color": "Agouti",
            "description": "Quick and alert, loves fresh greens."
        },
        {
            "name": "Cotton", "category": "Rabbits", "breed": "Lionhead",
            "image": "https://images.unsplash.com/photo-1589254064278-e026347102e8",
            "location": "Kokapet, Hyderabad", "age": "1 year", "sex": "Female", "color": "White",
            "description": "Has a unique mane like a lion."
        },

        # 🐠 FISH (6)
        {
            "name": "Nemo", "category": "Fish", "breed": "Clownfish",
            "image": "https://images.unsplash.com/photo-1535591273668-578e31182c4f",
            "location": "Sanjeeva Reddy Nagar, Hyderabad", "age": "1 year", "sex": "Male", "color": "Orange & White",
            "description": "Bright and active in the tank."
        },
        {
            "name": "Bubbles", "category": "Fish", "breed": "Goldfish",
            "image": "https://images.unsplash.com/photo-1522069169874-c58ec4b76be5",
            "location": "Somajiguda, Hyderabad", "age": "6 months", "sex": "Male", "color": "Gold",
            "description": "A very common and easy-to-care-for pet."
        },
        {
            "name": "Dory", "category": "Fish", "breed": "Blue Tang",
            "image": "https://images.unsplash.com/photo-1534043464124-3832c2a1215c",
            "location": "Balkampet, Hyderabad", "age": "2 years", "sex": "Female", "color": "Blue",
            "description": "Beautiful blue color and very peaceful."
        },
        {
            "name": "Finnegan", "category": "Fish", "breed": "Betta",
            "image": "https://images.unsplash.com/photo-1537029525281-7925e01784ca",
            "location": "Panjagutta, Hyderabad", "age": "1 year", "sex": "Male", "color": "Red & Blue",
            "description": "Stunning fins, should be kept alone."
        },
        {
            "name": "Salty", "category": "Fish", "breed": "Angelfish",
            "image": "https://images.unsplash.com/photo-1524704654690-b56c05c78a00",
            "location": "Koti, Hyderabad", "age": "2 years", "sex": "Female", "color": "Silver & Black",
            "description": "Elegant and graceful swimmer."
        },
        {
            "name": "Spike", "category": "Fish", "breed": "Pufferfish",
            "image": "https://images.unsplash.com/photo-1599488615731-7e512819a636",
            "location": "Charminar, Hyderabad", "age": "3 years", "sex": "Male", "color": "Tan",
            "description": "Fascinating creature, needs special care."
        },

        # 🐭 MICE (6)
        {
            "name": "Jerry", "category": "Mice", "breed": "House Mouse",
            "image": "https://images.unsplash.com/photo-1452723312111-3a7d0db0e024",
            "location": "Bolarum, Hyderabad", "age": "6 months", "sex": "Male", "color": "Brown",
            "description": "Very quick and clever."
        },
        {
            "name": "Minnie", "category": "Mice", "breed": "Fancy Mouse",
            "image": "https://images.unsplash.com/photo-1551632432-c7d419d0a4fb",
            "location": "Alwal, Hyderabad", "age": "4 months", "sex": "Female", "color": "White",
            "description": "Very social and loves to nest."
        },
        {
            "name": "Stuart", "category": "Mice", "breed": "White Mouse",
            "image": "https://images.unsplash.com/photo-1588612143003-889d1b0d2d31",
            "location": "Trimulgherry, Hyderabad", "age": "8 months", "sex": "Male", "color": "White",
            "description": "Small, friendly, and very curious."
        },
        {
            "name": "Gus", "category": "Mice", "breed": "Field Mouse",
            "image": "https://images.unsplash.com/photo-1628178877145-257a09f8747a",
            "location": "Marredpally, Hyderabad", "age": "5 months", "sex": "Male", "color": "Grey-Brown",
            "description": "Loves to forage and hide in tunnels."
        },
        {
            "name": "Pearl", "category": "Mice", "breed": "Albino Mouse",
            "image": "https://images.unsplash.com/photo-1616782229566-513689cc647b",
            "location": "Sainikpuri, Hyderabad", "age": "1 year", "sex": "Female", "color": "Pure White",
            "description": "Calm and very gentle."
        },
        {
            "name": "Rex", "category": "Mice", "breed": "Satin Mouse",
            "image": "https://images.unsplash.com/photo-1543852786-1cf6624b9987",
            "location": "Tarnaka, Hyderabad", "age": "7 months", "sex": "Male", "color": "Champagne",
            "description": "Has a beautiful shiny coat."
        },

        # 🐢 TURTLES (6)
        {
            "name": "Speedy", "category": "Turtle", "breed": "Red-Eared Slider",
            "image": "https://images.unsplash.com/photo-1541336032412-2048956132b7",
            "location": "Nacharam, Hyderabad", "age": "5 years", "sex": "Male", "color": "Green",
            "description": "Loves basking under the lamp."
        },
        {
            "name": "Shelly", "category": "Turtle", "breed": "Box Turtle",
            "image": "https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f",
            "location": "Mallapur, Hyderabad", "age": "12 years", "sex": "Female", "color": "Brown & Yellow",
            "description": "Slow, steady, and loves fresh fruit."
        },
        {
            "name": "Crush", "category": "Turtle", "breed": "Sea Turtle",
            "image": "https://images.unsplash.com/photo-1583095368688-6627cc7d4986",
            "location": "Ramanthapur, Hyderabad", "age": "50 years", "sex": "Male", "color": "Green",
            "description": "A true ocean wanderer, very peaceful."
        },
        {
            "name": "Franklin", "category": "Turtle", "breed": "Painted Turtle",
            "image": "https://images.unsplash.com/photo-1596489369873-1ec9413fd827",
            "location": "Amberpet, Hyderabad", "age": "4 years", "sex": "Male", "color": "Dark Green",
            "description": "Beautiful markings on the shell."
        },
        {
            "name": "Tank", "category": "Turtle", "breed": "Tortoise",
            "image": "https://images.unsplash.com/photo-1508493126422-959c8846bb32",
            "location": "Kachiguda, Hyderabad", "age": "30 years", "sex": "Male", "color": "Greyish",
            "description": "Huge and incredibly long-lived."
        },
        {
            "name": "Snap", "category": "Turtle", "breed": "Snapping Turtle",
            "image": "https://images.unsplash.com/photo-1574620021676-e916ea8fb520",
            "location": "Osman Sagar, Hyderabad", "age": "15 years", "sex": "Female", "color": "Muddy Brown",
            "description": "Hardy and very strong, best for experts."
        }
    ]

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Clear existing pets for fresh start
        cursor.execute("DELETE FROM pets")
        
        # Try to find a lender user to assign pets to
        cursor.execute("SELECT id FROM users WHERE role = 'lender' LIMIT 1")
        lender = cursor.fetchone()
        lender_id = lender['id'] if lender else None

        for pet in pets:
            sql = """INSERT INTO pets (name, category, breed, image, location, age, sex, color, description, lender_id) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (
                pet['name'], 
                pet['category'], 
                pet['breed'], 
                pet['image'], 
                pet['location'], 
                pet['age'], 
                pet['sex'], 
                pet['color'], 
                pet['description'],
                lender_id
            )
            cursor.execute(sql, values)

        conn.commit()
        print(f"✅ Successfully seeded {len(pets)} pets into the database!")
        if not lender_id:
            print("⚠️ WARNING: No lender found in database. Pets seeded without lender_id.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ DATABASE ERROR: {e}")
        print("Please check if your MySQL server is running and the password in config.py is correct.")

if __name__ == "__main__":
    seed_pets()
