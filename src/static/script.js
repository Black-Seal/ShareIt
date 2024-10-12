document.addEventListener("DOMContentLoaded", function () {
    let listingsContainer = document.querySelector(".listings-container");
    let isLoading = false;
    let page = 1;

    // Function to load more listings
    function loadMoreListings() {
        if (isLoading) return;

        isLoading = true;
        page += 1;

        fetch(`/load-more-listings?page=${page}`)
            .then(response => response.json())
            .then(data => {
                data.listings.forEach(item => {
                    let listingBox = document.createElement('div');
                    listingBox.className = 'listing-box';
                    listingBox.innerHTML = `<h3>${item.name}</h3><p>${item.description}</p><p>Price: $${item.price}</p>`;
                    listingsContainer.appendChild(listingBox);
                });
                isLoading = false;
            })
            .catch(() => {
                isLoading = false;
            });
    }

    // Listen to scroll event for infinite scrolling
    listingsContainer.addEventListener("scroll", function () {
        if (listingsContainer.scrollTop + listingsContainer.clientHeight >= listingsContainer.scrollHeight) {
            loadMoreListings();
        }
    });

    document.addEventListener("DOMContentLoaded", function () {
        let startDateInput = document.getElementById("StartDate");
        let endDateInput = document.getElementById("EndDate");
        let totalPriceInput = document.getElementById("total_price");

        if (startDateInput && endDateInput && totalPriceInput) {
            // Fetch the price per day from the page
            let pricePerDay = parseFloat(document.getElementById('price_per_day').textContent);

            function calculateTotalPrice() {
                const startDate = new Date(startDateInput.value);
                const endDate = new Date(endDateInput.value);

                if (startDate && endDate && startDate <= endDate) {
                    const timeDifference = endDate.getTime() - startDate.getTime();
                    const numDays = Math.ceil(timeDifference / (1000 * 3600 * 24)); // Convert ms to days
                    const totalPrice = numDays * pricePerDay;
                    totalPriceInput.value = totalPrice.toFixed(2);  // Update the total price in the input
                } else {
                    totalPriceInput.value = ""; // Clear the field if the dates are invalid
                }
            }

            // Attach event listeners to start and end date inputs
            startDateInput.addEventListener("change", calculateTotalPrice);
            endDateInput.addEventListener("change", calculateTotalPrice);
        }
    });
});