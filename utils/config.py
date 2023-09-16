import environs


env = environs.Env()
env.read_env("./config.env")

api_id = 2040
api_hash = "b18441a1ff607e10a989891a5462e627"

session_string = env.str("SESSION_STRING", "")

db_url = env.str("MONGODB_URL", "")
db_name = "Dragon-Fork"

version = "[Selfbot] Dragon-Fork v1.1.0"
