# MNToys Application Specification

## 1. Project Overview
- **Project Name:** MNToys
- **Deployment URL:** [https://mntoys.netlify.app](https://mntoys.netlify.app)
- **Hosting Platform:** Netlify
- **Base Architecture:** Derived from the app structure in `/home/fisk/github/nj-07demographics`. All dependencies and libraries in `package.json` will be updated to their current, modern versions.
- **Core Purpose:** An interactive map-based web application to help users locate MN Toy Library branches in the Minneapolis-St. Paul (MSP) area, find nearby community centers, plan public transit trips to the libraries, and place holds on available toys.

## 2. Map & Geographical Features
- **Base Map:** Interactive map centered on the Minneapolis-St. Paul metropolitan area.
- **MN Toy Library Locations:** Map markers prominently displaying the 3 official MN Toy Library locations.
- **Community Centers:** Map markers displaying "Community Centers" located within a 20-mile radius of any MN Toy Library location.
- **User Interaction:** Users can select Community Centers to set as a "base" for transit routing, or select Toy Library locations to view details and inventory.

## 3. Transit & Routing Features
- **Routing Modes:** Public transportation routing.
- **Origin Points (A):**
  - User's current location (via browser geolocation).
  - A user-designated "base" (selected from the mapped Community Centers).
- **Destination Points (B):**
  - One of the 3 MN Toy Library locations.
- **Time Configuration:**
  - **Default:** "Now" (immediate departure).
  - **Custom:** User can toggle between "Depart at" or "Arrive by" and specify an arbitrary future date and time.
- **Schedules:**
  - The app will display the outbound schedule based on the configured time.
  - The app will explicitly display the *return schedule* (from the Toy Library back to the origin) to ensure the user can easily plan a round trip.

## 4. User Interface (UI) Components
- **Transit Action Button:** A dedicated button that opens the public transportation sequence (origin selection, destination, and time/date configuration).
- **Database Action Button:** A dedicated button (available when interacting with a specific library location) that opens a connection to that location's toy database.
- **Configuration Modals/Panels:**
  - A transit planner panel to adjust "now", "arrive by", "depart at", date, and time.
  - A toy database view showing available inventory for the selected location.

## 5. Toy Database & Reservation System
- **Inventory Access:** Triggered via the Database Action Button for a specific library location.
- **Reservation Rules:**
  - Users can place a "hold" on specific toys.
  - **Hold Limit:** Maximum of 3 items per user.
  - **Hold Duration:** 1 week.

## 6. Required External Services / APIs (For Planning)
- **Mapping Provider:** (e.g., Mapbox, Leaflet, or Google Maps) to render the MSP area and plot coordinates.
- **Transit Routing API:** (e.g., Metro Transit API, Google Maps Directions API) to calculate transit routes and schedules.
- **Places API:** To query and retrieve "Community Centers" within the 20-mile radius.
- **Toy Database API / Backend:** To query location-specific toy inventory and manage user hold states (3 items, 1-week expiry).