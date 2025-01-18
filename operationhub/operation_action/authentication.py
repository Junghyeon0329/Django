from rest_framework import throttling 

class OneSecondThrottle(throttling.UserRateThrottle): 
    rate = '1/second'