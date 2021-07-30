import lcddriver
import time
from pycoingecko import CoinGeckoAPI
import onepinkeypad.onepinkeypad as opk

# Uncomment the line below if you are running this script on startup:
# time.sleep(15)

# Define One Pin Keypad Analog Pin:
pin = 0

# Variable to store keypad button being pressed:
key_value = '1'
cur_key_value = '\0'

# Create a keypad object:
keypad = opk.OnePinKeypad(pin)

# Insert your calibrated threholds array here:
my_thresholds = [558, 3730, 6438, 8810, 10530, 12390, 14045, 15540, 16620, 17861, 18970, 19970, 20750, 21615, 22430, 23150]

# If calibrated values are being used, use_calibrated_thresholds below:
keypad.use_calibrated_thresholds(my_thresholds)

# Initialize the CoinGeckoAPI and LCD driver
cg = CoinGeckoAPI()
lcd = lcddriver.lcd()

# Retrieve the program start_time
start_time = round(time.time())
cur_time = start_time

# print_pair is used to update the LCD with the crypto pair's price and 24 hour change
def print_pair(pair_name, pair_price, pair_24hr_change):
    # Clear the LCD
    lcd.lcd_clear()
 
    # Print the crypto name and price on line 1 its 24 hour change on line 2 
    lcd.lcd_display_string(f"{pair_name}: ${pair_price}", 1)
    lcd.lcd_display_string(f"24h chng: {pair_24hr_change}%", 2)

while True:
    # If 60 seconds has passed or a keypad button to change the currency has been pressed
    if (start_time - cur_time) % 60 == 0 or key_value == cur_key_value:
        # Retrieve the crypto prices relative to the us dollar and retrieve their 24 hour changes
        price_dict = cg.get_price(ids=['bitcoin', 'ethereum','litecoin'], vs_currencies='usd', include_24hr_change='true')
        
        # If button 1 has been pressed store the details of bitcoin
        if key_value == '1':
            pair_name = 'BTC/USD'
            pair_price = price_dict['bitcoin']['usd']
            pair_24hr_change = price_dict['bitcoin']['usd_24h_change']
        # If button 2 has been pressed store the details of bitcoin
        elif key_value == '2':
            pair_name = 'ETH/USD'
            pair_price = price_dict['ethereum']['usd']
            pair_24hr_change = price_dict['ethereum']['usd_24h_change']
        # If button 3 has been pressed store the details of litecoin
        else:
            pair_name = 'LTC/USD'
            pair_price = price_dict['litecoin']['usd']
            pair_24hr_change = price_dict['litecoin']['usd_24h_change']
        # Print the correct currency pair
        print_pair(pair_name, pair_price, round(pair_24hr_change, 2))
    # Run the read_keypad_instantaneous function to determine which button is pressed within the timeout, in milliseconds
    # Store that value in the cur_key_value
    cur_key_value = keypad.read_keypad_instantaneous()
    
    # If a new crypto button has been pressed, update key_value to reflect that
    if cur_key_value in ['1', '2', '3']:
        key_value = cur_key_value
    # Update cur_time
    cur_time = round(time.time())
