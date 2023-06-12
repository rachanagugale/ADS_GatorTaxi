# ADS_GatorTaxi
Implemented a Gator Taxi application using red black tree and min heap.

The following operations are implemented in the project:
1. **Print(rideNumber):** Prints the triplet (rideNumber, rideCost, tripDuration).
2. **Print(rideNumber1, rideNumber2):** Prints all triplets (rx, rideCost, tripDuration) for which rideNumber1 <= rx <= rideNumber2.
3. **Insert(rideNumber, rideCost, tripDuration):** Inserts triplet where rideNumber differs from existing ride numbers.
4. **GetNextRide():** When this function is invoked, the ride with the lowest rideCost (ties are broken by selecting the ride with the lowest tripDuration) is output. This ride is then deleted from the data structure.
5. **CancelRide(rideNumber):** Deletes the triplet (rideNumber, rideCost, tripDuration) from the data structures, can be ignored if an entry for rideNumber doesn’t exist.
6. **UpdateTrip(rideNumber, new_tripDuration):** Where the rider wishes to change the destination, in this case, <br>
a) if the *new_tripDuration <= existing tripDuration*, there would be no action needed. <br>
b) if the *existing_tripDuration < new_tripDuration <= 2\*(existing tripDuration)*, the driver will cancel the existing ride and a new ride request would be created with a penalty of 10 on existing rideCost . We update the entry in the data structure with (rideNumber, rideCost+10, new_tripDuration) <br>
c) if the *new_tripDuration > 2*(existing tripDuration)*, the ride would be automatically declined and the ride would be removed from the data structure.
