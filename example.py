from pyryd import Ryd

ryd = Ryd("api_url", "my_email", "supersecretpassword")

ryd.fetch()
print(ryd._raw_data)
