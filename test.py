import postmates as pm
import time

api = pm.PostmatesAPI("036a1197-aee9-4011-b759-b02d02bff6dc", "cus_Kh54mwFO1IKAfV")
pickup = pm.Location('Alice', '100 Main St, San Francisco, CA', '415-555-0000')
dropoff = pm.Location('Bob', '200 Main St, San Francisco, CA', '415-777-9999')

quote = pm.DeliveryQuote(api, pickup.address, dropoff.address)

delivery = pm.Delivery(api, 'a manifest', pickup, dropoff)
delivery.create()

for i in range(0,60):
    time.sleep(10)
    delivery.update_status()
    print (delivery)
