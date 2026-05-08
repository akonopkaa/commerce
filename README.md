# commerce #

This project is an e-commerce auction web application inspired by eBay. It allows users to create listings, place bids, comment on auctions, manage a watchlist, and browse items by category. It is built with Django on the backend and uses HTML, CSS, and Bootstrap on the frontend.

## Requirements: ##

### Backend: ###
- Python 3.14.0
- Django

### Frontend: ###
- HTML
- CSS
- Bootstrap

## Functionality: ##

### Models: ###
The application includes models for auction listings, bids, and comments, in addition to the default User model. The Django admin panel allows full management of listings, bids, and comments.

### Create Listing: ###
Signed-in users can create a new auction listing by providing a title, description, and starting bid. They can also optionally add an image URL and a category.

### Active Listings: ###
The home page displays all active auction listings. Each listing includes at least the title, description, current price, and image if one is available.

### Listing Page: ###
Each listing has its own page where users can view full details, place bids, add comments, and manage their watchlist. If the listing creator closes the auction, the highest bidder becomes the winner and the listing is no longer active.

### Watchlist and Categories: ###
Authenticated users can save listings to a personal watchlist and view them on a dedicated page. Users can also browse all categories and open pages showing active listings for each category.

## How to run: ##

1. Install dependencies: `pip install django`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Run server: `python manage.py runserver`
5. Open the local address shown in the terminal in your browser.
