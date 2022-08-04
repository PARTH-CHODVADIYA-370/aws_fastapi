import motor.motor_asyncio
from bson.objectid import ObjectId


MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.My_Fiti

# Workout Collection
Workout_collection = database.get_collection("Workout")

# User_Details Collection
User_collection = database.get_collection("User_Registration")

# Exercise Collection
Exercise_collection = database.get_collection("Exercise")

# Bodyparts Collection
Bodyparts_collection = database.get_collection("Bodyparts")

# Recipes Collection
Recipes_collection = database.get_collection("Recipes")

# Equipments Collection
Equipments_collection = database.get_collection("Equipments")

# Equipments Collection
Levels_collection = database.get_collection("Levels")

# Levels Collection
Levels_collection = database.get_collection("Levels")

# Goals Collection
Goals_collection = database.get_collection("Goals")

# Categories Collection
Categories_collection = database.get_collection("Categories")

# Tags Collection
Tags_collection = database.get_collection("Tags")

# Post Collection
Post_collection = database.get_collection("Post")

# Subscription Collection
Subscription_collection = database.get_collection("Subscription")

# Razorpay Collection
Razorpay_collection = database.get_collection("Razorpay")

# Stripe Collection
Stripe_collection = database.get_collection("Stripe")

# Measurments Collection
Measurments_collection = database.get_collection("Measurments")
