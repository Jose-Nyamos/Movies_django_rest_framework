from rest_framework.throttling import UserRateThrottle,AnonRateThrottle


class ReviewCreateThrottle(UserRateThrottle):
    
    scope='create_review'
    
    
class ReviewListThrottle(UserRateThrottle):
    
    scope='review-list'
 