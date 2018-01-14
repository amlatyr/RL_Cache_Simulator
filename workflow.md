# Structure
Simulator is the main class.
* It initializes the Requester, the CacheManager and the policy
* When a new request is made by requester (following the zipf distribution), it passes it first to the policy, which figures out which objects to evict if needed. The CacheManager then performs the defined action.
