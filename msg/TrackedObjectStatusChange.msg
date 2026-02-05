std_msgs/Header header
uint8 objtype                 # Object type (e.g., 0=person, 1=cup, etc.)
uint8 trackid                 # Track ID of the object
string name                   # Human-readable name if available
uint8 status                  # Status code (e.g., 0=detected, 1=lost, 2=updated)
float32 confidence            # Confidence score of the status change