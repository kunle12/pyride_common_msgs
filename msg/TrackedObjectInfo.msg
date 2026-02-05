uint8 objtype                 # Object type identifier (e.g., 0=person, 1=cup, etc.)
uint8 id                      # Unique instance ID for this object
ObjectBound bound             # 2D bounding box in image coordinates
geometry_msgs/Point32 est_pos # Estimated 3D position of the object
float32 confidence            # Detection confidence (0.0 to 1.0)