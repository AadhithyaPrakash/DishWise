document.addEventListener('DOMContentLoaded', function () { 
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;

    function changeSlide() {
        slides.forEach(slide => slide.classList.remove('slide-active'));
        slides[currentSlide].classList.add('slide-active');
        currentSlide = (currentSlide + 1) % slides.length;
    }

    changeSlide(); // Set first slide as active initially
    setInterval(changeSlide, 6000); // Change slide every 6 seconds

    // Submit the form when the form is submitted
    const form = document.getElementById('commodity-form');
    form.addEventListener('submit', submitForm);

    // Update varieties based on selected commodity
    const commoditySelect = document.getElementById('commodity');
    commoditySelect.addEventListener('change', updateVarieties);
});

// Function to update varieties based on selected commodity
function updateVarieties() {
    const commodity = document.getElementById('commodity').value;
    const varietySelect = document.getElementById('variety');

    // Clear existing varieties
    varietySelect.innerHTML = '<option value="" disabled selected>Select a variety</option>';

    // Define varieties based on commodity
    const varieties = {
        "Amaranthus": ["Amaranthus"],
        "Apple": ["American"],
        "Ashgourd": ["Gourd"],
        "Banana": ["Besrai", "Other", "Poovan", "Red Banana", "Robusta"]
        'Beans': ['Beans (Whole)'],
         'Beetroot': ['Beetroot'], 
         'Bitter gourd': ['Bitter Gourd'],
          'Bottle gourd': ['Bottle Gourd'], 
          'Brinjal': ['Arkasheela Mattigulla', 'Brinjal', 'Round'], 
          'Cabbage': ['Cabbage'], 
          'Capsicum': ['Capsicum'], 
          'Carrot': ['Pusakesar'], 
          'Castor Seed': ['Caster', 'Castor seed', 'Other'], 
          'Cauliflower': ['Ranchi'], 
          'Chili Red': ['Bold', 'Other', 'Red'], 
          'Chow Chow': ['Chow Chow'], 
          'Cluster beans': ['Cluster Beans'], 
          'Coconut': ['Big', 'Coconut', 'Grade- II', 'Grade-I', 'Grade-III', 'Medium', 'Other', 'Small'], 
          'Coconut Seed': ['Coconut Seed', 'Other'], 
          'Copra': ['Ball', 'Copra', 'Medium', 'Milling Copra', 'Small', 'other'], 
          'Cotton': ['170-C2  (Ginned)', '170-CO2 (Unginned)', 'A-51-9 24mm. FIne', 'Bunny', 'Cotton (Ginned)', 'Cotton (Unginned)', 'DCH-32  (Ginned)', 'DCH-32(Unginned)', 'Desi', 'GCH', 'LD-491', 'LRA', 'LRA  (Ginned)', 'Local', 'MCU', 'MCU 5', 'MCU-7', 'Other', 'RCH-2', 'Surabi', 'Varalaxmi'], 
          'Cowpea (Lobia/Karamani)': ['Cowpea (W-S)', 'Cowpea (Whole)', 'Jawari/Local', 'Other'],
           'Custard Apple (Sharifa)': ['Custard Apple(Sharifa)'], 
           'Drumstick': ['Drumstick'], 'Dry Chillies': ['1st Sort', 'Dry Chillies', 'Fine 2', 'Local', 'Other', 'Red', 'Red Top'], 'Elephant Yam (Suran)': ['Elephant Yam (Suran)', 'Other'], 'Garlic': ['Average'], 'Gingelly Oil': ['Gingelly Oil', 'Other'], 'Grapes': ['Annabesahai'], 'Green Avare (W)': ['Avare (W)'], 'Green Chilli': ['Green Chilly'], 'Green Gram Dal (Moong Dal)': ['Green Gram Dal', 'Other'], 'Green Peas': ['Green Peas', 'Other'], 'Ground Nut Oil': ['Ground Nut Oil', 'Other'], 'Ground Nut Seed': ['Ground Nut Seed', 'Other'], 'Groundnut': ['Balli/Habbu', 'Big (With Shell)', 'Bold', 'Bold Kernel', 'DMV-7', 'Groundnut seed', 'Gungri (With Shell)', 'Hybrid', 'JL-24', 'Local', 'Other', 'Seed', 'TMV-2', 'VRI - 1'], 'Groundnut (Split)': ['Groundnut(Split)', 'Other'], 'Groundnut pods (raw)': ['Groundnut pods (raw)', 'Other'], 'Guava': ['Guava Alahabad'], 'Hybrid Cumbu': ['Hybrid Cumbu', 'Other'], 'Indian Beans (Seam)': ['Indian Beans (Seam)'], 'Jack Fruit': ['Jack Fruit'], 'Jasmine': ['Jasmine'], 'Kakada': ['Kakada'], 'Karamani': ['Karamani', 'Other'], 'Knool Khol': ['Knool Khol'], 'Lemon': ['Lemon'], 'Lime': ['Lime'], 'Maize': ['Deshi Red', 'Deshi White', 'Fine', 'Hybrid', 'Hybrid Red (Cattle Feed)', 'Hybrid Yellow (Cattle Feed)', 'Hybrid/Local', 'Local', 'Medium', 'Megha', 'Other', 'Prakash', 'Red', 'White Local', 'Yellow'], 'Mango': ['Safeda'], 'Mango (Raw-Ripe)': ['Mango - Raw-Ripe'], 'Moath Dal': ['Moath (W)'], 'Onion': ['Bellary', 'Medium', 'Nasik', 'Onion', 'Other', 'Small'], 'Onion Green': ['Onion Green'], 'Orange': ['Darjeeling'], 'Papaya': ['Papaya'], 'Pineapple': ['Pine Apple'], 'Pomegranate': ['Pomogranate'], 'Potato': ['(Red Nanital)', 'Badshah', 'Jyoti'], 'Pumpkin': ['Pumpkin'], 'Raddish': ['Other', 'Raddish'], 'Ragi (Finger Millet)': ['Feeds (Poultry Quality)', 'Fine', 'Local', 'Medium', 'Medium Fine', 'Other', 'Red'], 'Soyabean': ['Black', 'Local', 'Other'], 'Spinach': ['Spinach'], 'Sugarcane': ['Other', 'Sugarcane'], 'Sweet Potato': ['Hosur Red'], 'T.V. Cumbu': ['Other', 'T.V. Cumbu'], 'Tamarind Fruit': ['Chapathi', 'Other', 'Seedless 1Variety', 'Seedless 2Variety', 'Tamarind Fruit', 'With Seed 1Variety', 'With Seed 2Variety'], 'Tamarind Seed': ['Other'], 'Tapioca': ['Other', 'Tapioca'], 'Tender Coconut': ['Tender Coconut'], 'Thinai (Italian Millet)': ['Other', 'Thinai (Italian Millet)'], 'Thondekai': ['Thondekai'], 'Tobacco': ['Other', 'Verginia'], 'Tomato': ['Deshi', 'Other'], 
          'Tube Flower': ['Tube Flower'], 'Turmeric': ['Bulb', 'Finger', 'Other', 'Turmeric'], 'Turnip': ['Turnip'], 
          'Water Melon': ['Other', 'Water Melon'], 'Yam (Ratalu)': ['Yam (Ratalu)']
        }
        // Add other commodities and their varieties here
    };

    // Populate the variety dropdown based on the selected commodity
    if (varieties[commodity]) {
        varieties[commodity].forEach(variety => {
            const option = document.createElement('option');
            option.value = variety;
            option.textContent = variety;
            varietySelect.appendChild(option);
        });
    }
}

window.addEventListener("scroll", function() {
    // Get the slider element
    const slider = document.querySelector(".slider");
    // Get the height of the slider
    const sliderHeight = slider.offsetHeight;
    // Get the current scroll position
    const scrollPosition = window.scrollY;
    // Get all text elements inside the slider
    const textOverlayElements = document.querySelectorAll(".text-overlay");

    // Apply blur effect based on scroll position
    if (scrollPosition < sliderHeight) {
        const blurValue = (scrollPosition / sliderHeight) * 10; // Adjust the blur intensity
        textOverlayElements.forEach((element) => {
            element.style.filter = `blur(${blurValue}px)`;
        });
    } else {
        // Remove blur when scrolled past the slider
        textOverlayElements.forEach((element) => {
            element.style.filter = "none";
        });
    }
});

function submitForm(event) {
    event.preventDefault();

    // Get form data
    const district = document.getElementById('district').value;
    const commodity = document.getElementById('commodity').value;
    const variety = document.getElementById('variety').value; // Get the selected variety
    const amount = document.getElementById('amount').value;
    const month = document.getElementById('month').value;
    const year = document.getElementById('year').value;

    // Prepare the data to send
    const data = {
        district: district,
        commodity: commodity,
        variety: variety, // Include the variety in the data
        amount: amount,
        month: month,
        year: year
    };

    // Send data to Flask
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            console.error(result.error);
            alert('Error: ' + result.error);
            return;
        }

        // Populate predicted price using template literals
        document.getElementById('predicted-price').textContent = 
            `Predicted price for ${data.commodity} (${data.variety}) in ${data.district} for ${data.month}/${data.year}: ₹${result.predictedPrice.toFixed(2)} per quintal`;

        // Populate nearby districts
        const locationList = document.getElementById('location-list');
        locationList.innerHTML = ''; // Clear previous results
        result.nearbyDistricts.forEach(districtInfo => {
            const li = document.createElement('li');
            li.textContent = `${districtInfo.District} (${districtInfo.distance.toFixed(2)} km), Price: ₹${districtInfo.Modal_Price.toFixed(2)} per quintal`;
            locationList.appendChild(li);
        });

        // Show best buy month
        document.getElementById('best-buy-month').textContent = 
            `Best buy month for ${data.commodity} (${data.variety}) is ${result.bestBuyMonth}.`;

        // Update amount display
        document.getElementById('amount-display').textContent = `${amount} kg`;

        // Show results section
        document.getElementById('results-section').classList.remove('hidden');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error: ' + error.message);
    });
}
