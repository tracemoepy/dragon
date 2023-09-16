try:
    from pyrogram import Client
except Exception as e:
       print(e)
       exit(1)

with Client(
    name="string",
    api_id=2040,
    api_hash="b18441a1ff607e10a989891a5462e627",
    in_memory=True
) as app:
    print(app.export_session_string())
